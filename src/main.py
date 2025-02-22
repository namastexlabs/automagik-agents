import logging
import os
from datetime import datetime, timezone
from typing import Dict, Type, List

import logfire
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.agents.simple_agent.agent import SimpleAgent
from src.agents.notion_agent.agent import NotionAgent
from src.config import init_config
from src.utils.logging import configure_logging
from src.version import SERVICE_INFO

# Configure logging
configure_logging()

# Get our module's logger
logger = logging.getLogger(__name__)

# Initialize config
config = init_config()

# Available agents
AGENTS: Dict[str, Type] = {
    "simple": SimpleAgent,
    "notion": NotionAgent
}

app = FastAPI(
    title=SERVICE_INFO["name"],
    description=SERVICE_INFO["description"],
    version=SERVICE_INFO["version"]
)

class AgentRunRequest(BaseModel):
    message_input: str
    context: dict = {}

class AgentInfo(BaseModel):
    name: str
    type: str

@app.get("/")
async def root():
    return {
        "status": "online",
        **SERVICE_INFO
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": SERVICE_INFO["version"]
    }

@app.get("/agents", response_model=List[AgentInfo])
async def list_agents():
    return [
        AgentInfo(name=name, type=agent_class.__name__)
        for name, agent_class in AGENTS.items()
    ]

@app.post("/agent/{agent_name}/run")
async def run_agent(agent_name: str, request: AgentRunRequest):
    if agent_name not in AGENTS:
        raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")
    
    try:
        agent_class = AGENTS[agent_name]
        agent = agent_class(config)
        response = await agent.process_message(request.message_input)
        return response
    except Exception as e:
        logger.error(f"Error running agent {agent_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
