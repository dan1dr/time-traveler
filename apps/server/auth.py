"""
Authentication and JWT token management.
"""

import os
import secrets
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Header, Depends
from typing import Dict, Optional

# JWT Configuration
JWT_SECRET = os.getenv("JWT_SECRET", secrets.token_urlsafe(32))
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS", "1"))  # 1 hour default


def create_jwt_token(user_id: str = "demo-user", session_id: str = None) -> str:
    """Create a JWT token for authentication"""
    if not session_id:
        session_id = secrets.token_urlsafe(16)
    
    payload = {
        "user_id": user_id,
        "session_id": session_id,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        "iat": datetime.utcnow(),
        "iss": "time-traveler-api"
    }
    
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def validate_jwt_token(token: str) -> Dict:
    """Validate a JWT token and return payload if valid"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user(authorization: str = Header(None)) -> Dict:
    """Dependency to get current user from JWT token"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    token = authorization.split(" ")[1]
    return validate_jwt_token(token)


def get_jwt_config() -> Dict:
    """Get JWT configuration for debugging/monitoring"""
    return {
        "algorithm": JWT_ALGORITHM,
        "expiration_hours": JWT_EXPIRATION_HOURS,
        "secret_configured": bool(JWT_SECRET)
    }
