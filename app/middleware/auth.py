from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from jose import JWTError

OPEN_PATHS = ["/api/v1/auth/register", "/api/v1/auth/login", "/docs", "/openapi.json", "/redoc"]


async def auth_middleware(request: Request, call_next):
    if any(request.url.path.startswith(p) for p in OPEN_PATHS):
        return await call_next(request)
    return await call_next(request)
