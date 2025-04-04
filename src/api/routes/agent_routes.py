import logging
from typing import List
from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse
from src.api.models import AgentInfo, AgentRunRequest
from src.api.controllers.agent_controller import list_agent_templates, handle_agent_run

# Create router for agent endpoints
agent_router = APIRouter()

# Get our module's logger
logger = logging.getLogger(__name__)

@agent_router.get("/agent/list", response_model=List[AgentInfo], tags=["Agents"], 
           summary="List Available Agents",
           description="Returns a list of all available agent templates that can be used.")
async def list_agents():
    """
    Get a list of all available agent templates
    """
    return await list_agent_templates()

@agent_router.post("/agent/{agent_name}/run", tags=["Agents"],
            summary="Run Agent",
            description="Execute an agent with the specified name. Optionally provide a session ID or name to maintain conversation context.")
async def run_agent(agent_name: str, request: AgentRunRequest):
    """
    Run an agent with the specified parameters
    """
    try:
        return await handle_agent_run(agent_name, request)
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error running agent {agent_name}: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Error running agent: {str(e)}"}
        ) 