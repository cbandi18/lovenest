from jose import jwt
from datetime import datetime, timedelta, timezone
from decouple import config

#Secret key for signing the token
JWT_SECRET = config("JWT_SECRET", default="your-fallback-secret-key") #default="your-temp-fallback-secret-key" if it can't find or not defined the actual JWT_SECRET in .env
JWT_ALGORITHM = "HS256"

def create_access_token(data: dict, expires_in: int=30):
    """
    Generates a JWT token.
    :param data: Dictionary to encode (e.g., {"username": "cbandi"})
    :param expires_in: Token expiry in minutes
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_in)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt
    