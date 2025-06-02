from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os

# Load secret from .env
load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET", "your-fallabck-secret-key")

OAuth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str = Depends(OAuth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        username: str = payload.get("username")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token: username missing")
        
        # check expiration (Optional)
        exp = payload.get("exp")
        if exp and datetime.now(timezone.utc).timestamp() > exp:
            raise HTTPException(status_code=401, detail="Token expired")
        
        return payload
    
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
