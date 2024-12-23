from fastapi import Depends, HTTPException
from .auth import jwt

def get_current_user(token: str = Depends(jwt.get_current_token)):
    if token:
        return token
    raise HTTPException(status_code=401, detail="Not authenticated")