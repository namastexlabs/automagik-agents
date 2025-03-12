import logging
from datetime import datetime
from typing import List, Optional
import json
import math
import uuid

from fastapi import APIRouter, HTTPException, Query, Path, Depends
from src.agents.models.agent_factory import AgentFactory
from src.config import settings
from src.memory.message_history import MessageHistory
from src.api.models import (
    AgentRunRequest,
    AgentInfo,
    DeleteSessionResponse,
    MessageModel,
    SessionResponse,
    SessionListResponse,
    SessionInfo,
    UserCreate,
    UserUpdate,
    UserInfo,
    UserListResponse
)
from src.memory.pg_message_store import PostgresMessageStore
from src.utils.db import execute_query

# Create API router for v1 endpoints
router = APIRouter()

# Get our module's logger
logger = logging.getLogger(__name__)

@router.get("/agent/list", response_model=List[AgentInfo], tags=["Agents"], 
           summary="List Available Agents",
           description="Returns a list of all available agent templates that can be used.")
async def list_agents():
    """List all available agents."""
    agent_list = []
    for name in AgentFactory.list_available_agents():
        # Get agent type from factory
        agent_type = AgentFactory._agents[name][0].__name__
        
        # Get model and description from database if available
        model = "unknown"
        description = None
        
        try:
            from src.agents.models.agent_db import get_agent_by_name
            db_agent = get_agent_by_name(name)
            if db_agent:
                model = db_agent.get("model", "unknown")
                description = db_agent.get("description")
        except Exception as e:
            logger.warning(f"Error getting agent details from database: {str(e)}")
        
        # Create agent info object with all fields
        agent_info = AgentInfo(
            name=name,
            type=agent_type,
            model=model,
            description=description
        )
        agent_list.append(agent_info)
    
    return agent_list

@router.post("/agent/{agent_name}/run", tags=["Agents"],
            summary="Run Agent",
            description="Execute an agent with the specified name. Optionally provide a session ID or name to maintain conversation context.")
async def run_agent(agent_name: str, request: AgentRunRequest):
    """Run an agent with the given name."""
    try:
        # Get the pre-initialized agent
        agent = AgentFactory.get_agent(agent_name)
        
        # Get session_origin from request
        session_origin = request.session_origin
        
        # Extract session_name if provided
        session_name = request.session_name
        
        # Create message store instance
        from src.memory.pg_message_store import PostgresMessageStore
        store = PostgresMessageStore()
        
        # Get the agent database ID if available
        agent_id = getattr(agent, "db_id", None)
        
        # If agent_id is not set, try to get it from the database
        if agent_id is None:
            from src.agents.models.agent_db import get_agent_by_name
            db_agent = get_agent_by_name(f"{agent_name}_agent" if not agent_name.endswith('_agent') else agent_name)
            if db_agent:
                agent_id = db_agent["id"]
                # Save it back to the agent instance for future use
                agent.db_id = agent_id
                logging.info(f"Found agent ID {agent_id} for agent {agent_name}")
            else:
                logging.warning(f"Could not find agent ID for agent {agent_name}")
        
        # Check if session name is provided, use it to lookup existing sessions
        if session_name:
            # Look up the session by name
            existing_session = store.get_session_by_name(session_name)
            if existing_session:
                # Found an existing session with this name
                session_id = existing_session["id"]
                existing_agent_id = existing_session["agent_id"]
                
                # Check if the session is already associated with a different agent
                if existing_agent_id is not None and existing_agent_id != agent_id:
                    logger.error(f"Session name '{session_name}' is already associated with agent ID {existing_agent_id}, cannot use with agent ID {agent_id}")
                    raise HTTPException(
                        status_code=409,
                        detail=f"Session name '{session_name}' is already associated with a different agent. Please use a different session name."
                    )
                
                # Found an existing session with this name, use it
                request.session_id = session_id
                logger.info(f"Found existing session with name '{session_name}', using ID: {session_id}")
        
        # Check if session_id is provided
        if not request.session_id:
            # If no session_id is provided or no session found with the provided name
            # Create a new session with the session_name if provided
            try:
                new_session_id = store.create_session(
                    user_id=request.user_id,
                    session_origin=session_origin,
                    session_name=session_name,
                    agent_id=agent_id
                )
                request.session_id = new_session_id
                logger.info(f"Created new session with ID: {new_session_id}, name: {session_name}, and origin: {session_origin}")
            except Exception as e:
                # Check for unique constraint violation
                if "duplicate key value violates unique constraint" in str(e) and "sessions_name_key" in str(e):
                    logger.error(f"Session name '{session_name}' already exists")
                    raise HTTPException(
                        status_code=409,
                        detail=f"Session name '{session_name}' already exists. Please use a different session name."
                    )
                # Re-raise other exceptions
                logger.error(f"Error creating session: {str(e)}")
                raise
        else:
            # Check if request.session_id is a session name instead of a UUID
            session_id = request.session_id
            try:
                # Validate if it's a UUID
                uuid.UUID(request.session_id)
            except ValueError:
                # Not a UUID, try to look up by name
                logger.info(f"Looking up session by name: {request.session_id}")
                
                # Use the PostgresMessageStore method to get session by name
                resolved_session = store.get_session_by_name(request.session_id)
                
                if resolved_session:
                    # Found a session with matching name
                    session_id = resolved_session["id"]
                    existing_agent_id = resolved_session["agent_id"]
                    
                    # Check if the session is already associated with a different agent
                    if existing_agent_id is not None and existing_agent_id != agent_id:
                        logger.error(f"Session name '{request.session_id}' is already associated with agent ID {existing_agent_id}, cannot use with agent ID {agent_id}")
                        raise HTTPException(
                            status_code=409,
                            detail=f"Session name '{request.session_id}' is already associated with a different agent. Please use a different session name."
                        )
                    
                    logger.info(f"Found session ID {session_id} for name {request.session_id}")
                else:
                    # Name doesn't exist yet, create a new session with this name
                    try:
                        session_id = store.create_session(
                            user_id=request.user_id, 
                            session_origin=session_origin, 
                            session_name=request.session_id,
                            agent_id=agent_id
                        )
                        logger.info(f"Created new session with ID: {session_id} and name: {request.session_id}")
                    except Exception as e:
                        # Check for unique constraint violation
                        if "duplicate key value violates unique constraint" in str(e) and "sessions_name_key" in str(e):
                            logger.error(f"Session name '{request.session_id}' already exists")
                            raise HTTPException(
                                status_code=409,
                                detail=f"Session name '{request.session_id}' already exists. Please use a different session name."
                            )
                        # Re-raise other exceptions
                        logger.error(f"Error creating session: {str(e)}")
                        raise
                
                # Update the request.session_id with the actual UUID
                request.session_id = session_id
            
            # Check if the provided session exists, if not create it
            if not store.session_exists(request.session_id):
                # Create the session with the provided ID
                try:
                    store._ensure_session_exists(request.session_id, request.user_id, session_origin, session_name, agent_id)
                    logger.info(f"Created session with provided ID: {request.session_id}, name: {session_name}, and origin: {session_origin}")
                except ValueError as e:
                    # Handle agent ID mismatch error
                    logger.error(f"Session agent mismatch error: {str(e)}")
                    raise HTTPException(
                        status_code=409,
                        detail=f"Session ID {request.session_id} is already associated with a different agent. Please use a different session."
                    )
            else:
                # Session exists - update the session with the current session_origin and session_name if provided
                try:
                    store._ensure_session_exists(request.session_id, request.user_id, session_origin, session_name, agent_id)
                    
                    # If a session name is provided but the session has no name, update it
                    if session_name:
                        # Get the current session details to check if it has a name
                        session_details = execute_query(
                            "SELECT name FROM sessions WHERE id = %s::uuid", 
                            (request.session_id,)
                        )
                        
                        if session_details and (session_details[0].get('name') is None or session_details[0].get('name') == ''):
                            # Session has no name, update it
                            execute_query(
                                "UPDATE sessions SET name = %s WHERE id = %s::uuid",
                                (session_name, request.session_id),
                                fetch=False
                            )
                            logger.info(f"Updated existing session {request.session_id} with name: {session_name}")
                    
                    logger.info(f"Using existing session: {request.session_id}, name: {session_name}, with origin: {session_origin}")
                except ValueError as e:
                    # Handle agent ID mismatch error
                    logger.error(f"Session agent mismatch error: {str(e)}")
                    raise HTTPException(
                        status_code=409,
                        detail=f"Session ID {request.session_id} is already associated with a different agent. Please use a different session."
                    )
        
        # Store channel_payload in the users table if provided
        if request.channel_payload:
            try:
                # Use the user_id directly as an integer
                numeric_user_id = request.user_id if request.user_id is not None else 1
                
                # Update the user record with the channel_payload
                execute_query(
                    """
                    UPDATE users 
                    SET channel_payload = %s
                    WHERE id = %s
                    """,
                    (
                        json.dumps(request.channel_payload),
                        numeric_user_id
                    ),
                    fetch=False
                )
                logger.info(f"Updated channel_payload for user {numeric_user_id}")
            except Exception as e:
                logger.error(f"Error updating channel_payload for user {request.user_id}: {str(e)}")
        
        # Get message history with user_id
        message_history = MessageHistory(request.session_id, user_id=request.user_id)
        
        # Link the agent to the session in the database
        AgentFactory.link_agent_to_session(agent_name, request.session_id)
        
        if message_history and message_history.messages:
            # Get filtered messages up to the limit for agent processing
            # No need to update the database - just filter for memory purposes
            filtered_messages = message_history.get_filtered_messages(
                message_limit=request.message_limit,
                sort_desc=False  # Sort chronologically for agent processing
            )

        # Process the message with additional metadata if available
        message_metadata = {
            "message_type": request.message_type,
            "media_url": request.mediaUrl, 
            "mime_type": request.mime_type
        }
        
        # Create a combined context with all available information
        combined_context = {**request.context, **message_metadata}
        
        # Add channel_payload to context if available
        if request.channel_payload:
            combined_context["channel_payload"] = request.channel_payload
        
        # Log incoming message details
        logger.info(f"Processing message from user {request.user_id} with type: {request.message_type}")
        if request.mediaUrl:
            logger.info(f"Media URL: {request.mediaUrl}, MIME type: {request.mime_type}")
        
        response = await agent.process_message(
            request.message_content,  # Use message_content instead of message_input
            session_id=request.session_id,
            agent_id=agent_id,  # Pass the agent ID to be stored with the messages
            user_id=request.user_id,  # Pass the user ID
            context=combined_context  # Include all context information
        )
        
        # Log the tool call and output counts more safely
        messages = response.history.get('messages', [])
        if messages:  # Only try to access if there are messages
            last_message = messages[-1]
            tool_call_count = len(last_message.get('tool_calls', []))
            tool_output_count = len(last_message.get('tool_outputs', []))
            logging.info(f"Agent run completed. Tool calls: {tool_call_count}, Tool outputs: {tool_output_count}")
        else:
            logging.info("Agent run completed. No messages in history.")
        
        return response
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.exception(f"Error running agent {agent_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions", response_model=SessionListResponse, tags=["Sessions"],
            summary="List All Sessions",
            description="Retrieve a list of all sessions with pagination options.")
async def list_sessions(
    page: int = 1, 
    page_size: int = 50, 
    sort_desc: bool = True
):
    """List all sessions with pagination.
    
    Args:
        page: Page number (1-based).
        page_size: Number of sessions per page.
        sort_desc: Sort by most recent first if True.
        
    Returns:
        List of sessions with pagination info.
    """
    try:
        # Get message store
        message_store = PostgresMessageStore()
        
        # Get all sessions
        result = message_store.get_all_sessions(
            page=page,
            page_size=page_size,
            sort_desc=sort_desc
        )
        
        # Convert to session info objects
        sessions = [SessionInfo(**session) for session in result['sessions']]
        
        # Create response
        response = SessionListResponse(
            sessions=sessions,
            total_count=result['total_count'],
            page=result['page'],
            page_size=result['page_size'],
            total_pages=result['total_pages']
        )
        
        return response
    except Exception as e:
        logger.error(f"Error listing sessions: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list sessions: {str(e)}"
        )

@router.get("/sessions/{session_id_or_name}", response_model=SessionResponse, response_model_exclude_none=True, 
           tags=["Sessions"],
           summary="Get Session History",
           description="Retrieve a session's message history with pagination options. You can use either the session ID (UUID) or a session name.")
async def get_session(
    session_id_or_name: str,
    page: int = 1,
    page_size: int = 50,
    sort_desc: bool = True,
    hide_tools: bool = False
):
    """Get a session's message history with pagination.
    
    Args:
        session_id_or_name: The ID or name of the session to retrieve.
        page: Page number (1-based).
        page_size: Number of messages per page.
        sort_desc: Sort by most recent first if True.
        hide_tools: If True, excludes tool calls and outputs from the response.
        
    Returns:
        The session's message history with pagination info.
    """
    try:
        # Get the message store
        message_store = PostgresMessageStore()
        
        # Determine if the input is a UUID or session name
        session_id = session_id_or_name
        try:
            # Validate if it's a UUID
            uuid.UUID(session_id_or_name)
        except ValueError:
            # Not a UUID, try to look up by name
            logger.info(f"Looking up session by name: {session_id_or_name}")
            
            # Use the PostgresMessageStore method to get session by name
            session_info = message_store.get_session_by_name(session_id_or_name)
            
            if not session_info:
                return SessionResponse(
                    session_id=session_id_or_name,
                    messages=[],
                    exists=False,
                    total_messages=0,
                    current_page=1,
                    total_pages=0
                )
            
            # Found a session with matching name
            session_id = session_info["id"]
            logger.info(f"Found session ID {session_id} for name {session_id_or_name}")

        # Get message history with the resolved ID
        message_history = MessageHistory(session_id)
        
        # Check if session exists
        exists = message_history._store.session_exists(session_id)
        
        if not exists:
            session_response = SessionResponse(
                session_id=session_id_or_name,
                messages=[],
                exists=False,
                total_messages=0,
                current_page=1,
                total_pages=0
            )
        else:
            # Get paginated messages
            paginated_messages, total_messages, current_page, total_pages = message_history.get_paginated_messages(
                page=page,
                page_size=page_size,
                sort_desc=sort_desc
            )
            
            # Format messages for API response
            formatted_messages = [
                message for message in (
                    message_history.format_message_for_api(msg, hide_tools=hide_tools)
                    for msg in paginated_messages
                )
                if message is not None
            ]
            
            # Wrap each formatted message dict into a MessageModel to ensure Pydantic processing
            clean_messages = [MessageModel(**msg) for msg in formatted_messages]
            
            session_response = SessionResponse(
                session_id=session_id,
                messages=clean_messages,
                exists=True,
                total_messages=total_messages,
                current_page=current_page,
                total_pages=total_pages
            )
        
        return session_response
    except Exception as e:
        logger.error(f"Error retrieving session {session_id_or_name}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve session: {str(e)}"
        )

@router.delete("/sessions/{session_id_or_name}", tags=["Sessions"],
              summary="Delete Session",
              description="Delete a session's message history by its ID or name.")
async def delete_session(session_id_or_name: str):
    """Delete a session's message history.
    
    Args:
        session_id_or_name: The ID or name of the session to delete.
        
    Returns:
        Status of the deletion operation.
    """
    try:
        # Get the message store
        message_store = PostgresMessageStore()
        
        # Determine if the input is a UUID or session name
        session_id = session_id_or_name
        try:
            # Validate if it's a UUID
            uuid.UUID(session_id_or_name)
        except ValueError:
            # Not a UUID, try to look up by name
            logger.info(f"Looking up session by name: {session_id_or_name}")
            
            # Use the PostgresMessageStore method to get session by name
            session_info = message_store.get_session_by_name(session_id_or_name)
            
            if not session_info:
                raise HTTPException(
                    status_code=404,
                    detail=f"Session with name '{session_id_or_name}' not found"
                )
            
            # Found a session with matching name
            session_id = session_info["id"]
            logger.info(f"Found session ID {session_id} for name {session_id_or_name}")
        
        # Check if session exists
        if not message_store.session_exists(session_id):
            raise HTTPException(
                status_code=404,
                detail=f"Session {session_id_or_name} not found"
            )
        
        # Clear the session messages
        message_store.clear_session(session_id)
        
        # Also delete the session from the sessions table
        execute_query(
            "DELETE FROM sessions WHERE id = %s",
            (session_id,),
            fetch=False
        )
        
        logger.info(f"Successfully deleted session: {session_id_or_name}")
        
        return DeleteSessionResponse(
            status="success",
            session_id=session_id,
            message="Session history deleted successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting session {session_id_or_name}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete session: {str(e)}"
        )

# User management endpoints
@router.get("/users", response_model=UserListResponse, tags=["Users"],
            summary="List Users",
            description="Returns a list of all users with pagination options.\n\n**Requires Authentication**: This endpoint requires an API key.")
async def list_users(
    page: int = Query(1, description="Page number (1-based)"),
    page_size: int = Query(50, description="Number of users per page"),
    sort_desc: bool = Query(True, description="Sort by most recent first if True")
):
    """List all users with pagination."""
    try:
        # Get total count first for pagination
        count_result = execute_query("SELECT COUNT(*) as count FROM users")
        total_count = count_result[0]['count'] if count_result else 0
        
        # Calculate offset based on page and page_size
        offset = (page - 1) * page_size
        
        # Build the query with sorting
        order_direction = "DESC" if sort_desc else "ASC"
        query = f"""
            SELECT id, email, created_at, updated_at, user_data 
            FROM users 
            ORDER BY created_at {order_direction} 
            LIMIT %s OFFSET %s
        """
        
        # Execute the paginated query
        users_data = execute_query(query, (page_size, offset))
        
        # Process the results
        users = []
        for user in users_data:
            # Parse user_data JSON if it exists
            user_data = {}
            if user.get('user_data'):
                if isinstance(user['user_data'], str):
                    try:
                        user_data = json.loads(user['user_data'])
                    except:
                        user_data = {}
                else:
                    user_data = user['user_data']
            
            # Create UserInfo object
            user_info = UserInfo(
                id=user['id'],
                email=user['email'],
                created_at=user.get('created_at'),
                updated_at=user.get('updated_at'),
                name=user_data.get('name'),
                channel_payload=user_data.get('channel_payload')
            )
            users.append(user_info)
        
        # Calculate total pages
        total_pages = math.ceil(total_count / page_size) if total_count > 0 else 1
        
        return UserListResponse(
            users=users,
            total_count=total_count,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
    except Exception as e:
        logger.error(f"Error listing users: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/users", response_model=UserInfo, tags=["Users"],
            summary="Create User",
            description="Creates a new user with email, phone_number, and/or user_data fields.\n\n**Requires Authentication**: This endpoint requires an API key.")
async def create_user(user: UserCreate):
    """Create a new user."""
    try:
        # Need at least one identifier - email or phone_number
        if not user.email and not user.phone_number:
            raise HTTPException(status_code=400, detail="At least one of email or phone_number must be provided")

        # Check if user already exists
        existing_conditions = []
        existing_params = []
        
        if user.email:
            existing_conditions.append("email = %s")
            existing_params.append(user.email)
            
        if user.phone_number:
            existing_conditions.append("phone_number = %s")
            existing_params.append(user.phone_number)
            
        query = f"SELECT id FROM users WHERE {' OR '.join(existing_conditions)}"
        existing = execute_query(query, tuple(existing_params))
        
        if existing and len(existing) > 0:
            raise HTTPException(status_code=409, detail=f"User already exists with the provided email or phone number")
        
        # Construct the insert query
        now = datetime.now()
        result = execute_query(
            """
            INSERT INTO users (email, phone_number, user_data, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, email, phone_number, user_data, created_at, updated_at
            """,
            (user.email, user.phone_number, json.dumps(user.user_data) if user.user_data else None, now, now)
        )
        
        new_user = result[0]
        
        return UserInfo(
            id=new_user["id"],
            email=new_user.get("email"),
            phone_number=new_user.get("phone_number"),
            user_data=new_user.get("user_data"),
            created_at=new_user.get("created_at"),
            updated_at=new_user.get("updated_at")
        )
    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/users/{user_identifier}", response_model=UserInfo, tags=["Users"],
            summary="Get User",
            description="Returns details for a specific user by ID, email, or phone number.\n\n**Requires Authentication**: This endpoint requires an API key.")
async def get_user(user_identifier: str = Path(..., description="The user ID, email, or phone number")):
    """Get user details by ID, email, or phone number."""
    # Check if user_identifier is an integer (ID)
    if user_identifier.isdigit():
        # It's an ID, use it directly
        user_id = int(user_identifier)
        user = execute_query("SELECT * FROM users WHERE id = %s", (user_id,))
    else:
        # Try email or phone number
        user = execute_query("SELECT * FROM users WHERE email = %s OR phone_number = %s", (user_identifier, user_identifier,))
    
    # Check if user exists
    if not user or len(user) == 0:
        raise HTTPException(status_code=404, detail=f"User not found with identifier: {user_identifier}")
    
    # Convert the first user to a UserInfo model
    user_data = user[0]
    return UserInfo(
        id=user_data["id"],
        email=user_data.get("email"),
        phone_number=user_data.get("phone_number"),
        user_data=user_data.get("user_data"),
        created_at=user_data.get("created_at"),
        updated_at=user_data.get("updated_at")
    )

@router.put("/users/{user_identifier}", response_model=UserInfo, tags=["Users"],
            summary="Update User",
            description="Updates an existing user identified by ID, email, or phone number.\n\n**Requires Authentication**: This endpoint requires an API key.")
async def update_user(user_update: UserUpdate, user_identifier: str = Path(..., description="The user ID, email, or phone number")):
    """Update an existing user."""
    try:
        # First, find the user
        if user_identifier.isdigit():
            # It's an ID, use it directly
            user_id = int(user_identifier)
            user = execute_query("SELECT * FROM users WHERE id = %s", (user_id,))
        else:
            # Try email or phone number
            user = execute_query("SELECT * FROM users WHERE email = %s OR phone_number = %s", 
                              (user_identifier, user_identifier,))
        
        # Check if user exists
        if not user or len(user) == 0:
            raise HTTPException(status_code=404, detail=f"User not found with identifier: {user_identifier}")
        
        # Get the user ID from the query result
        user_id = user[0]["id"]
        
        # Build the update query dynamically based on what fields are provided
        set_parts = []
        params = []
        
        if user_update.email is not None:
            set_parts.append("email = %s")
            params.append(user_update.email)
            
        if user_update.phone_number is not None:
            set_parts.append("phone_number = %s")
            params.append(user_update.phone_number)
            
        if user_update.user_data is not None:
            set_parts.append("user_data = %s")
            params.append(json.dumps(user_update.user_data))
        
        # Always update the updated_at timestamp
        set_parts.append("updated_at = %s")
        now = datetime.now()
        params.append(now)
        
        # Add the user_id as the last parameter
        params.append(user_id)
        
        # If there's nothing to update, return the current user data
        if not set_parts:
            current_user = user[0]
            return UserInfo(
                id=current_user["id"],
                email=current_user.get("email"),
                phone_number=current_user.get("phone_number"),
                user_data=current_user.get("user_data"),
                created_at=current_user.get("created_at"),
                updated_at=current_user.get("updated_at")
            )
        
        # Execute the update query
        query = f"""
            UPDATE users
            SET {", ".join(set_parts)}
            WHERE id = %s
            RETURNING id, email, phone_number, user_data, created_at, updated_at
        """
        
        result = execute_query(query, tuple(params))
        updated_user = result[0]
        
        return UserInfo(
            id=updated_user["id"],
            email=updated_user.get("email"),
            phone_number=updated_user.get("phone_number"),
            user_data=updated_user.get("user_data"),
            created_at=updated_user.get("created_at"),
            updated_at=updated_user.get("updated_at")
        )
    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error updating user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.delete("/users/{user_identifier}", response_model=DeleteSessionResponse, tags=["Users"],
               summary="Delete User",
               description="Deletes a user account by ID, email, or phone number.\n\n**Requires Authentication**: This endpoint requires an API key.")
async def delete_user(user_identifier: str = Path(..., description="The user ID, email, or phone number")):
    """Delete a user account by ID, email, or phone number."""
    # Check if user_identifier is an integer (ID)
    if user_identifier.isdigit():
        # It's an ID, use it directly
        user_id = int(user_identifier)
        user = execute_query("SELECT id FROM users WHERE id = %s", (user_id,))
    else:
        # Try email or phone number
        user = execute_query("SELECT id FROM users WHERE email = %s OR phone_number = %s", (user_identifier, user_identifier,))
    
    # Check if user exists
    if not user or len(user) == 0:
        raise HTTPException(status_code=404, detail=f"User not found with identifier: {user_identifier}")
    
    # Get the user ID from the query result
    user_id = user[0]["id"]
    
    # Now delete the user
    execute_query("DELETE FROM users WHERE id = %s", (user_id,), fetch=False)
    
    # Return a successful response
    return DeleteSessionResponse(
        status="success",
        session_id=str(user_id),  # Use the session_id field to return the user_id
        message=f"User with ID {user_id} deleted successfully"
    ) 