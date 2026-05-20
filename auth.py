from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
import os

SECRET_KEY = os.getenv("SECRET_KEY")
JWT_ISSUER = os.getenv("JWT_ISSUER")
JWT_AUDIENCE = os.getenv("JWT_AUDIENCE")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configures bcrypt as the hashing algorithm for passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Tells FastAPI where the login endpoint is so it can extract bearer tokens from requests
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    # Encodes the provided data into a signed JWT token with an expiry time
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
    "exp": expire,
    "iss": JWT_ISSUER,
    "aud": JWT_AUDIENCE
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    # Decodes and verifies the token. Returns the payload dict or None if invalid or expired
    try:
        payload = jwt.decode(
            token, 
            SECRET_KEY, 
            algorithms=[ALGORITHM],
            audience=JWT_AUDIENCE,
            issuer=JWT_ISSUER
        )
        return payload
    except JWTError:
        return None
    
def get_current_user(token: str = Depends(oauth2_scheme)):
    # FastAPI dependency that extracts the token from the request and returns the decoded payload.
    # Raises 401 if the token is missing, invalid or expired.
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload