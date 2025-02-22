import logging
import os
from datetime import datetime
from typing import Dict, Type, List

import logfire
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.agents.simple_agent.agent import SimpleAgent
from src.agents.notion_agent.agent import NotionAgent
from src.config import settings
from src.utils.logging import configure_logging
from src.version import SERVICE_INFO

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

# API Key authentication
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

async def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != settings.AM_API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key"
        )
    return api_key

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
    uvicorn.run(app, host=settings.AM_HOST, port=settings.AM_PORT)
