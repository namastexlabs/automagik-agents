import logging
import os
from datetime import datetime
from typing import Dict, Type, List, Optional

import logfire
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.agents.models.agent import AgentBaseResponse
from src.agents.simple_agent.agent import SimpleAgent
from src.agents.notion_agent.agent import NotionAgent
from src.config import settings, load_settings, Settings
from src.utils.logging import configure_logging
from src.version import SERVICE_INFO
from src.auth import verify_api_key, API_KEY_NAME, api_key_header

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

class AgentInfo(BaseModel):
    name: str
    type: str

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str
    environment: str

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
        response = await agent.process_message(request.message_input)
        return response
    except Exception as e:
        logger.error(f"Error running agent {agent_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host=settings.AM_HOST,
        port=int(settings.AM_PORT),
        reload=True
    )
