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
from src.db import (
    Memory, 
    get_memory, 
    create_memory as repo_create_memory,
    update_memory as repo_update_memory,
    list_memories as repo_list_memories,
    delete_memory as repo_delete_memory
)

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
    
    # Use the repository pattern to list memories
    memories = repo_list_memories(
        agent_id=agent_id,
        user_id=user_id,
        session_id=session_uuid
    )
    
    # Total number of memories
    total_count = len(memories)
    
    # Calculate total pages
    total_pages = math.ceil(total_count / page_size)
    
    # Apply sorting
    if sort_desc:
        memories.sort(key=lambda x: x.created_at or datetime.min, reverse=True)
    else:
        memories.sort(key=lambda x: x.created_at or datetime.min)
    
    # Apply pagination
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_memories = memories[start_idx:end_idx]
    
    # Convert to response format
    memory_responses = []
    for memory in paginated_memories:
        memory_responses.append({
            "id": str(memory.id),
            "name": memory.name,
            "description": memory.description,
            "content": memory.content,
            "session_id": str(memory.session_id) if memory.session_id else None,
            "user_id": memory.user_id,
            "agent_id": memory.agent_id,
            "read_mode": memory.read_mode,
            "access": memory.access,
            "metadata": memory.metadata,
            "created_at": memory.created_at,
            "updated_at": memory.updated_at
        })
    
    return {
        "items": memory_responses,
        "page": page,
        "page_size": page_size,
        "total_count": total_count,
        "total_pages": total_pages
    }

@memory_router.post("/memories", response_model=MemoryResponse, tags=["Memories"],
             summary="Create Memory",
             description="Create a new memory with the provided details.")
async def create_memory(memory: MemoryCreate):
    try:
        # Convert session_id to UUID if provided
        session_uuid = None
        if memory.session_id:
            try:
                session_uuid = uuid.UUID(memory.session_id)
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid session_id format: {memory.session_id}")
        
        # Create a Memory model for the repository
        memory_model = Memory(
            id=None,  # Will be generated
            name=memory.name,
            description=memory.description,
            content=memory.content,
            session_id=session_uuid,
            user_id=memory.user_id,
            agent_id=memory.agent_id,
            read_mode=memory.read_mode,
            access=memory.access,
            metadata=memory.metadata,
            created_at=None,  # Will be set by DB
            updated_at=None   # Will be set by DB
        )
        
        # Create the memory using the repository
        memory_id = repo_create_memory(memory_model)
        
        if memory_id is None:
            raise HTTPException(status_code=500, detail="Failed to create memory")
        
        # Retrieve the created memory to get all fields
        created_memory = get_memory(memory_id)
        
        if not created_memory:
            raise HTTPException(status_code=404, detail=f"Memory created but not found with ID {memory_id}")
        
        # Convert to response format
        return {
            "id": str(created_memory.id),
            "name": created_memory.name,
            "description": created_memory.description,
            "content": created_memory.content,
            "session_id": str(created_memory.session_id) if created_memory.session_id else None,
            "user_id": created_memory.user_id,
            "agent_id": created_memory.agent_id,
            "read_mode": created_memory.read_mode,
            "access": created_memory.access,
            "metadata": created_memory.metadata,
            "created_at": created_memory.created_at,
            "updated_at": created_memory.updated_at
        }
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
