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
    return [
        AgentInfo(name=name, type=AgentFactory._agents[name][0].__name__)
        for name in AgentFactory.list_available_agents()
    ]

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
        
        # Check if session_id is provided
        if not request.session_id:
            # If no session_id is provided, generate a new one
            # Generate a new session with an empty string (this will create a new session in the database)
            new_session_id = store._ensure_session_exists("", request.user_id, session_origin, session_name)
            request.session_id = new_session_id
            logger.info(f"Created new session with ID: {new_session_id}, name: {session_name}, and origin: {session_origin}")
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
                resolved_id = store.get_session_by_name(request.session_id)
                
                if resolved_id:
                    # Found a session with matching name
                    session_id = resolved_id
                    logger.info(f"Found session ID {session_id} for name {request.session_id}")
                else:
                    # Name doesn't exist yet, create a new session with this name
                    session_id = store.create_session(
                        user_id=request.user_id, 
                        session_origin=session_origin, 
                        session_name=request.session_id
                    )
                    logger.info(f"Created new session with ID: {session_id} and name: {request.session_id}")
                
                # Update the request.session_id with the actual UUID
                request.session_id = session_id
            
            # Check if the provided session exists, if not create it
            if not store.session_exists(request.session_id):
                # Create the session with the provided ID
                store._ensure_session_exists(request.session_id, request.user_id, session_origin, session_name)
                logger.info(f"Created session with provided ID: {request.session_id}, name: {session_name}, and origin: {session_origin}")
            else:
                # Update the session with the current session_origin if needed
                store._ensure_session_exists(request.session_id, request.user_id, session_origin, session_name)
                logger.info(f"Using existing session: {request.session_id}, name: {session_name}, with origin: {session_origin}")
        
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
            resolved_id = message_store.get_session_by_name(session_id_or_name)
            
            if not resolved_id:
                return SessionResponse(
                    session_id=session_id_or_name,
                    messages=[],
                    exists=False,
                    total_messages=0,
                    current_page=1,
                    total_pages=0
                )
            
            # Found a session with matching name
            session_id = resolved_id
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
            resolved_id = message_store.get_session_by_name(session_id_or_name)
            
            if not resolved_id:
                raise HTTPException(
                    status_code=404,
                    detail=f"Session with name '{session_id_or_name}' not found"
                )
            
            # Found a session with matching name
            session_id = resolved_id
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
            description="Creates a new user.\n\n**Requires Authentication**: This endpoint requires an API key.")
async def create_user(user: UserCreate):
    """Create a new user."""
    try:
        # Check if user with the same email already exists
        existing = execute_query("SELECT id FROM users WHERE email = %s", (user.email,))
        if existing:
            raise HTTPException(status_code=409, detail=f"User with email {user.email} already exists")
        
        # Prepare user_data
        now = datetime.utcnow()
        user_data = {
            "name": user.name or user.email.split("@")[0],
            "created_via": "api"
        }
        
        # Add channel_payload if provided
        if user.channel_payload:
            user_data["channel_payload"] = user.channel_payload
        
        # Insert new user
        result = execute_query(
            """
            INSERT INTO users (email, created_at, updated_at, user_data) 
            VALUES (%s, %s, %s, %s)
            RETURNING id, email, created_at, updated_at, user_data
            """,
            (
                user.email,
                now,
                now,
                json.dumps(user_data)
            )
        )
        
        if not result or len(result) == 0:
            raise HTTPException(status_code=500, detail="Failed to create user")
        
        created_user = result[0]
        
        # Parse user_data JSON
        parsed_user_data = {}
        if created_user.get('user_data'):
            if isinstance(created_user['user_data'], str):
                try:
                    parsed_user_data = json.loads(created_user['user_data'])
                except:
                    parsed_user_data = {}
            else:
                parsed_user_data = created_user['user_data']
        
        return UserInfo(
            id=created_user['id'],
            email=created_user['email'],
            created_at=created_user.get('created_at'),
            updated_at=created_user.get('updated_at'),
            name=parsed_user_data.get('name'),
            channel_payload=parsed_user_data.get('channel_payload')
        )
    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/users/{user_id}", response_model=UserInfo, tags=["Users"],
            summary="Get User",
            description="Returns details for a specific user.\n\n**Requires Authentication**: This endpoint requires an API key.")
async def get_user(user_id: int = Path(..., description="The user ID")):
    """Get a specific user by ID."""
    try:
        user_data = execute_query("SELECT id, email, created_at, updated_at, user_data FROM users WHERE id = %s", (user_id,))
        if not user_data or len(user_data) == 0:
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
        
        user = user_data[0]
        
        # Parse user_data JSON
        parsed_user_data = {}
        if user.get('user_data'):
            if isinstance(user['user_data'], str):
                try:
                    parsed_user_data = json.loads(user['user_data'])
                except:
                    parsed_user_data = {}
            else:
                parsed_user_data = user['user_data']
        
        return UserInfo(
            id=user['id'],
            email=user['email'],
            created_at=user.get('created_at'),
            updated_at=user.get('updated_at'),
            name=parsed_user_data.get('name'),
            channel_payload=parsed_user_data.get('channel_payload')
        )
    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error getting user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.put("/users/{user_id}", response_model=UserInfo, tags=["Users"],
            summary="Update User",
            description="Updates an existing user.\n\n**Requires Authentication**: This endpoint requires an API key.")
async def update_user(user_update: UserUpdate, user_id: int = Path(..., description="The user ID")):
    """Update an existing user."""
    try:
        # Check if user exists
        existing = execute_query("SELECT id, email, user_data FROM users WHERE id = %s", (user_id,))
        if not existing or len(existing) == 0:
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
        
        # Get current user data
        current_user = existing[0]
        
        # Parse existing user_data
        current_user_data = {}
        if current_user.get('user_data'):
            if isinstance(current_user['user_data'], str):
                try:
                    current_user_data = json.loads(current_user['user_data'])
                except:
                    current_user_data = {}
            else:
                current_user_data = current_user['user_data']
        
        # Prepare updated fields
        now = datetime.utcnow()
        update_fields = []
        update_values = []
        
        # Handle email update
        if user_update.email:
            update_fields.append("email = %s")
            update_values.append(user_update.email)
        
        # Handle user_data updates
        updated_user_data = current_user_data.copy()
        
        # Update name if provided
        if user_update.name is not None:
            updated_user_data["name"] = user_update.name
        
        # Update channel_payload if provided
        if user_update.channel_payload is not None:
            updated_user_data["channel_payload"] = user_update.channel_payload
        
        # Only update user_data if changed
        if updated_user_data != current_user_data:
            update_fields.append("user_data = %s")
            update_values.append(json.dumps(updated_user_data))
        
        # Build query
        if not update_fields:
            # No changes to make
            return await get_user(user_id)
        
        query = f"""
            UPDATE users 
            SET {", ".join(update_fields)} 
            WHERE id = %s
            RETURNING id, email, created_at, updated_at, user_data
        """
        
        # Add user_id to values
        update_values.append(user_id)
        
        # Execute update
        result = execute_query(query, tuple(update_values))
        
        if not result or len(result) == 0:
            raise HTTPException(status_code=500, detail="Failed to update user")
        
        updated_user = result[0]
        
        # Parse user_data JSON
        parsed_user_data = {}
        if updated_user.get('user_data'):
            if isinstance(updated_user['user_data'], str):
                try:
                    parsed_user_data = json.loads(updated_user['user_data'])
                except:
                    parsed_user_data = {}
            else:
                parsed_user_data = updated_user['user_data']
        
        return UserInfo(
            id=updated_user['id'],
            email=updated_user['email'],
            created_at=updated_user.get('created_at'),
            updated_at=updated_user.get('updated_at'),
            name=parsed_user_data.get('name'),
            channel_payload=parsed_user_data.get('channel_payload')
        )
    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error updating user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.delete("/users/{user_id}", response_model=DeleteSessionResponse, tags=["Users"],
               summary="Delete User",
               description="Deletes a user account.\n\n**Requires Authentication**: This endpoint requires an API key.")
async def delete_user(user_id: int = Path(..., description="The user ID")):
    """Delete a user account."""
    try:
        # Check if user exists
        existing = execute_query("SELECT id FROM users WHERE id = %s", (user_id,))
        if not existing or len(existing) == 0:
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
        
        # Delete the user
        execute_query("DELETE FROM users WHERE id = %s", (user_id,), fetch=False)
        
        return DeleteSessionResponse(
            status="success",
            session_id=str(user_id),  # Reusing DeleteSessionResponse model
            message=f"User with ID {user_id} was deleted successfully"
        )
    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error deleting user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}") 