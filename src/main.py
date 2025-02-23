import logging
import os
from datetime import datetime
from typing import Dict, Type, List, Optional

import logfire
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pydantic_ai.messages import SystemPromptPart, UserPromptPart

from src.agents.models.agent import AgentBaseResponse
from src.agents.simple_agent.agent import SimpleAgent
from src.agents.notion_agent.agent import NotionAgent
from src.config import settings, load_settings, Settings
from src.utils.logging import configure_logging
from src.version import SERVICE_INFO
from src.auth import verify_api_key, API_KEY_NAME, api_key_header
from src.memory.message_history import MessageHistory, ToolCallPart, ToolOutputPart

# Configure logging
configure_logging()

# Get our module's logger
logger = logging.getLogger(__name__)

app = FastAPI(
    title=SERVICE_INFO["name"],
    description=SERVICE_INFO["description"],
    version=SERVICE_INFO["version"]
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class AgentRunRequest(BaseModel):
    message_input: str
    context: dict = {}
    session_id: Optional[str] = None

class AgentInfo(BaseModel):
    name: str
    type: str

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str
    environment: str

class DeleteSessionResponse(BaseModel):
    status: str
    session_id: str
    message: str

class MessageModel(BaseModel):
    role: str
    content: str
    assistant_name: Optional[str] = None
    tool_calls: Optional[List[Dict]] = None
    tool_outputs: Optional[List[Dict]] = None

class SessionResponse(BaseModel):
    session_id: str
    messages: List[MessageModel]
    exists: bool

@app.get("/")
async def root():
    return {
        "status": "online",
        **SERVICE_INFO
    }

@app.get("/health")
async def health_check():
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        version=SERVICE_INFO["version"],
        environment=settings.AM_ENV
    )

@app.get("/agents", response_model=List[AgentInfo])
async def list_agents():
    return [
        AgentInfo(name=name, type=agent_class.__name__)
        for name, agent_class in {"simple": SimpleAgent, "notion": NotionAgent}.items()
    ]

@app.post("/agent/{agent_name}/run")
async def run_agent(agent_name: str, request: AgentRunRequest, api_key: str = Depends(verify_api_key)):
    if agent_name not in ["simple", "notion"]:
        raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")
    
    try:
        agent_class = {"simple": SimpleAgent, "notion": NotionAgent}[agent_name]
        agent = agent_class({})
        response = await agent.process_message(
            request.message_input,
            session_id=request.session_id
        )
        return response
    except Exception as e:
        logger.error(f"Error running agent {agent_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/session/{session_id}")
async def delete_session(session_id: str, api_key: str = Depends(verify_api_key)):
    """Delete a session's message history.
    
    Args:
        session_id: The ID of the session to delete.
        
    Returns:
        Status of the deletion operation.
    """
    try:
        # Get the message store from MessageHistory
        message_store = MessageHistory._store
        
        # Check if session exists
        if not message_store.session_exists(session_id):
            raise HTTPException(
                status_code=404,
                detail=f"Session {session_id} not found"
            )
        
        # Clear the session
        message_store.clear_session(session_id)
        
        logger.info(f"Successfully deleted session: {session_id}")
        
        return DeleteSessionResponse(
            status="success",
            session_id=session_id,
            message="Session history deleted successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting session {session_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete session: {str(e)}"
        )

@app.get("/session/{session_id}", response_model=SessionResponse)
async def get_session(session_id: str, api_key: str = Depends(verify_api_key)):
    """Get a session's message history.
    
    Args:
        session_id: The ID of the session to retrieve.
        
    Returns:
        The session's message history.
    """
    try:
        # Get the message store from MessageHistory
        message_store = MessageHistory._store
        
        # Check if session exists
        exists = message_store.session_exists(session_id)
        
        if not exists:
            # Return empty message history if session doesn't exist
            return SessionResponse(
                session_id=session_id,
                messages=[],
                exists=False
            )
        
        # Get messages from store
        messages = message_store.get_messages(session_id)
        
        # Convert messages to response format
        formatted_messages = [
            MessageModel(
                role="system" if any(isinstance(p, SystemPromptPart) for p in msg.parts)
                else "user" if any(isinstance(p, UserPromptPart) for p in msg.parts)
                else "assistant",
                content=msg.parts[0].content if msg.parts else "",
                assistant_name=msg.parts[0].assistant_name if msg.parts else None,
                tool_calls=[part.tool_call for part in msg.parts if isinstance(part, ToolCallPart)] if msg.parts else None,
                tool_outputs=[part.tool_output for part in msg.parts if isinstance(part, ToolOutputPart)] if msg.parts else None
            )
            for msg in messages
        ]
        
        logger.info(f"Retrieved session {session_id} with {len(formatted_messages)} messages")
        
        return SessionResponse(
            session_id=session_id,
            messages=formatted_messages,
            exists=True
        )
    except Exception as e:
        logger.error(f"Error retrieving session {session_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve session: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host=settings.AM_HOST,
        port=int(settings.AM_PORT),
        reload=True
    )
