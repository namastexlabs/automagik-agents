from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from src.config import settings

API_KEY_NAME = "X-API-Key"

class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip auth for health check and root endpoints
        if request.url.path in ["/health", "/"]:
            return await call_next(request)

        api_key = request.headers.get(API_KEY_NAME)
        if api_key is None:
            raise HTTPException(status_code=401, detail="API Key is missing")
        if api_key != settings.AM_API_KEY:
            raise HTTPException(status_code=401, detail="Invalid API Key")
            
        return await call_next(request) 