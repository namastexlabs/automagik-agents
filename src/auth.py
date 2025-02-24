from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from src.config import settings

API_KEY_NAME = "x-api-key"

class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip auth for health check, root, and documentation endpoints
        no_auth_paths = [
            "/health", 
            "/",
            "/api/v1/docs",
            "/api/v1/redoc",
            "/api/v1/openapi.json"
        ]
        
        # Check if this path should bypass authentication
        if request.url.path in no_auth_paths:
            return await call_next(request)

        api_key = request.headers.get(API_KEY_NAME) or request.query_params.get(API_KEY_NAME)
        if api_key is None:
            return JSONResponse(status_code=401, content={"detail": "x-api-key is missing in headers or query parameters"})
        if api_key != settings.AM_API_KEY:
            return JSONResponse(status_code=401, content={"detail": "Invalid API Key"})
            
        return await call_next(request) 