from datetime import datetime
from pydantic_ai import RunContext
from .deps import Deps
async def get_current_date(ctx: RunContext[Deps]) -> str:
    """Get the current date in ISO format (YYYY-MM-DD)."""
    return datetime.now().date().isoformat()
