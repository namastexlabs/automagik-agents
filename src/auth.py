from fastapi import HTTPException, Depends
from fastapi.security import APIKeyHeader
from src.config import settings

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key is None:
        raise HTTPException(status_code=401, detail="API Key is missing")
    if api_key != settings.AM_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return api_key 