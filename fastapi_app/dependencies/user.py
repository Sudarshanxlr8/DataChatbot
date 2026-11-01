from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi_app.auth.security import decode_access_token
from fastapi_app.services.auth_service import get_user_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    """
    FastAPI dependency to extract and validate the authenticated user's identity from JWT bearer token.
    Decodes token, validates expiration, extracts 'sub' (user_id), and checks database user existence.
    Returns authenticated user_id string.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials or token expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = decode_access_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception

    user = get_user_by_id(user_id)
    if user is None:
        raise credentials_exception

    return user_id
