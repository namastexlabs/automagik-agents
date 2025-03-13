import logging
import json
import math
import uuid
from uuid import UUID
from datetime import datetime
from fastapi import APIRouter, HTTPException, Query, Path
from typing import Optional, List

from src.api.memory_models import (
    MemoryCreate,
    MemoryUpdate,
    MemoryResponse,
    MemoryListResponse
)
from src.utils.db import execute_query

# Create API router for memory endpoints
memory_router = APIRouter()

# Get our module's logger
logger = logging.getLogger(__name__)

@memory_router.get("/memories", response_model=MemoryListResponse, tags=["Memories"],
            summary="List Memories",
            description="List all memories with optional filters and pagination.")
async def list_memories(
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    agent_id: Optional[int] = Query(None, description="Filter by agent ID"),
    session_id: Optional[str] = Query(None, description="Filter by session ID"),
    page: int = Query(1, description="Page number (1-based)"),
    page_size: int = Query(50, description="Number of memories per page"),
    sort_desc: bool = Query(True, description="Sort by most recent first if True")
):
    # Validate and parse session_id as UUID if provided
    session_uuid = None
    if session_id:
        try:
            session_uuid = uuid.UUID(session_id)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid session_id format: {session_id}")
    
    # Build the query conditions
    conditions = []
    params = []
    
    if user_id is not None:
        conditions.append("user_id = %s")
        params.append(user_id)
    
    if agent_id is not None:
        conditions.append("agent_id = %s")
        params.append(agent_id)
    
    if session_uuid is not None:
        conditions.append("session_id = %s")
        params.append(str(session_uuid))
    
    # Construct the WHERE clause if conditions exist
    where_clause = ""
    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)
    
    # Get the total count
    count_query = f"SELECT COUNT(*) as count FROM memories {where_clause}"
    count_result = execute_query(count_query, params)
    total_count = count_result[0]["count"] if count_result else 0
    
    # Calculate pagination
    pages = math.ceil(total_count / page_size) if total_count > 0 else 0
    offset = (page - 1) * page_size
    
    # Order by clause
    order_by = "updated_at DESC" if sort_desc else "updated_at ASC"
    
    # Fetch memories with pagination
    query = f"SELECT * FROM memories {where_clause} ORDER BY {order_by} LIMIT %s OFFSET %s"
    params.extend([page_size, offset])
    memory_results = execute_query(query, params)
    
    # Convert to Pydantic models
    memories = []
    for memory in memory_results:
        memories.append(MemoryResponse(**memory))
    
    return MemoryListResponse(
        memories=memories,
        count=total_count,
        page=page,
        page_size=page_size,
        pages=pages
    )

@memory_router.post("/memories", response_model=MemoryResponse, tags=["Memories"],
             summary="Create Memory",
             description="Create a new memory with the provided details.")
async def create_memory(memory: MemoryCreate):
    try:
        # Generate a UUID for the memory if not provided
        memory_id = uuid.uuid4()
        
        # Get current timestamp
        now = datetime.utcnow()
        
        # Prepare metadata if provided, otherwise use an empty object
        metadata = memory.metadata if memory.metadata is not None else {}
        
        # Insert the memory into the database
        query = """
        INSERT INTO memories (
            id, name, description, content, session_id, user_id, agent_id,
            read_mode, access, metadata, created_at, updated_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING *
        """
        
        # Convert UUID objects to strings for PostgreSQL
        memory_id_str = str(memory_id)
        # Handle the session_id
        session_id_str = None
        if memory.session_id:
            # Since we changed the model to use str type, we can use it directly
            # However, we'll validate it's a proper UUID if possible
            try:
                # Try to convert to UUID to validate format, then back to string
                session_id_str = str(UUID(memory.session_id))
            except ValueError:
                # If not a valid UUID, just use the original string value
                session_id_str = memory.session_id
                logging.warning(f"Non-UUID session_id received: {session_id_str}")
        
        params = (
            memory_id_str, memory.name, memory.description, memory.content,
            session_id_str, memory.user_id, memory.agent_id, memory.read_mode,
            memory.access, json.dumps(metadata) if metadata else None, now, now
        )
        
        result = execute_query(query, params)
        
        if not result:
            raise HTTPException(status_code=500, detail="Failed to create memory")
        
        # Return the created memory
        return MemoryResponse(**result[0])
    except Exception as e:
        logger.error(f"Error creating memory: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating memory: {str(e)}")

@memory_router.post("/memories/batch", response_model=List[MemoryResponse], tags=["Memories"],
             summary="Create Multiple Memories",
             description="Create multiple memories in a single batch operation.")
async def create_memories_batch(memories: List[MemoryCreate]):
    try:
        results = []
        now = datetime.utcnow()
        
        # Prepare the query
        query = """
        INSERT INTO memories (
            id, name, description, content, session_id, user_id, agent_id,
            read_mode, access, metadata, created_at, updated_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING *
        """
        
        for memory in memories:
            # Generate a UUID for the memory
            memory_id = uuid.uuid4()
            memory_id_str = str(memory_id)
            
            # Prepare metadata if provided, otherwise use an empty object
            metadata = memory.metadata if memory.metadata is not None else {}
            
            # Handle the session_id
            session_id_str = None
            if memory.session_id:
                try:
                    # Try to convert to UUID to validate format, then back to string
                    session_id_str = str(UUID(memory.session_id))
                except ValueError:
                    # If not a valid UUID, just use the original string value
                    session_id_str = memory.session_id
                    logging.warning(f"Non-UUID session_id received: {session_id_str}")
            
            params = (
                memory_id_str, memory.name, memory.description, memory.content,
                session_id_str, memory.user_id, memory.agent_id, memory.read_mode,
                memory.access, json.dumps(metadata) if metadata else None, now, now
            )
            
            result = execute_query(query, params)
            
            if not result:
                # If this memory fails, continue with the others but log it
                logger.warning(f"Failed to create memory: {memory.name}")
                continue
            
            # Add the created memory to results
            results.append(MemoryResponse(**result[0]))
        
        # Return all successfully created memories
        return results
    except Exception as e:
        logger.error(f"Error creating memories in batch: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating memories in batch: {str(e)}")

@memory_router.get("/memories/{memory_id}", response_model=MemoryResponse, tags=["Memories"],
            summary="Get Memory",
            description="Get a memory by its ID.")
async def get_memory(memory_id: str = Path(..., description="The memory ID")):
    try:
        # Validate UUID format
        try:
            uuid.UUID(memory_id)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid memory ID format: {memory_id}")
        
        # Query the database - convert UUID to string
        memory_id_str = str(memory_id)
        query = "SELECT * FROM memories WHERE id = %s"
        result = execute_query(query, (memory_id_str,))
        
        if not result:
            raise HTTPException(status_code=404, detail=f"Memory {memory_id} not found")
        
        # Return the memory
        return MemoryResponse(**result[0])
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving memory: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving memory: {str(e)}")

@memory_router.put("/memories/{memory_id}", response_model=MemoryResponse, tags=["Memories"],
            summary="Update Memory",
            description="Update an existing memory with the provided details.")
async def update_memory(
    memory_update: MemoryUpdate,
    memory_id: str = Path(..., description="The memory ID")
):
    try:
        # Validate UUID format
        try:
            uuid.UUID(memory_id)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid memory ID format: {memory_id}")
        
        # Check if memory exists - convert UUID to string
        memory_id_str = str(memory_id)
        query = "SELECT * FROM memories WHERE id = %s"
        existing_memory = execute_query(query, (memory_id_str,))
        
        if not existing_memory:
            raise HTTPException(status_code=404, detail=f"Memory {memory_id} not found")
        
        # Get current timestamp
        now = datetime.utcnow()
        
        # Build update query dynamically based on provided fields
        update_fields = []
        params = []
        
        # Helper function to add fields to the update
        def add_field(field_name, value):
            if value is not None:
                update_fields.append(f"{field_name} = %s")
                params.append(value)
        
        # Add each field if it's provided
        add_field("name", memory_update.name)
        add_field("description", memory_update.description)
        add_field("content", memory_update.content)
        add_field("session_id", memory_update.session_id)
        add_field("user_id", memory_update.user_id)
        add_field("agent_id", memory_update.agent_id)
        add_field("read_mode", memory_update.read_mode)
        add_field("access", memory_update.access)
        
        # Handle metadata update - need to convert to JSON
        if memory_update.metadata is not None:
            update_fields.append("metadata = %s")
            params.append(json.dumps(memory_update.metadata))
        
        # Always update the updated_at timestamp
        update_fields.append("updated_at = %s")
        params.append(now)
        
        # If no fields to update, return the existing memory
        if len(update_fields) == 1:  # Only updated_at
            return MemoryResponse(**existing_memory[0])
        
        # Convert session_id to string if present
        if memory_update.session_id is not None:
            session_id_str = None
            try:
                # If it's a UUID object, convert to string
                if isinstance(memory_update.session_id, UUID):
                    session_id_str = str(memory_update.session_id)
                # If it's already a string, use it directly
                elif isinstance(memory_update.session_id, str):
                    # Validate it's a proper UUID string
                    session_id_str = str(UUID(memory_update.session_id))
                else:
                    # Try to convert to UUID first, then to string
                    session_id_str = str(UUID(str(memory_update.session_id)))
            except ValueError:
                # If conversion fails, use the original value as string
                session_id_str = str(memory_update.session_id)
                
            # Find and replace the session_id param with the string version
            for i, field in enumerate(update_fields):
                if field == "session_id = %s":
                    params[i] = session_id_str
                    break
                    
        # Build and execute the update query
        fields_str = ", ".join(update_fields)
        query = f"UPDATE memories SET {fields_str} WHERE id = %s RETURNING *"
        params.append(memory_id_str)
        
        result = execute_query(query, params)
        
        if not result:
            raise HTTPException(status_code=500, detail="Failed to update memory")
        
        # Return the updated memory
        return MemoryResponse(**result[0])
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating memory: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating memory: {str(e)}")

@memory_router.delete("/memories/{memory_id}", response_model=MemoryResponse, tags=["Memories"],
               summary="Delete Memory",
               description="Delete a memory by its ID.")
async def delete_memory(memory_id: str = Path(..., description="The memory ID")):
    try:
        # Validate UUID format
        try:
            uuid.UUID(memory_id)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid memory ID format: {memory_id}")
        
        # Check if memory exists and get its details for the response
        memory_id_str = str(memory_id)
        query = "SELECT * FROM memories WHERE id = %s"
        existing_memory = execute_query(query, (memory_id_str,))
        
        if not existing_memory:
            raise HTTPException(status_code=404, detail=f"Memory {memory_id} not found")
        
        # Delete the memory
        delete_query = "DELETE FROM memories WHERE id = %s"
        execute_query(delete_query, (memory_id_str,), fetch=False)
        
        # Return the deleted memory details
        return MemoryResponse(**existing_memory[0])
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting memory: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting memory: {str(e)}")
