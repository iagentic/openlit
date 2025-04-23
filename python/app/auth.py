from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import models, schemas
from .database import get_db
import os
from dotenv import load_dotenv
import logging

load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configure password hashing with SHA256
pwd_context = CryptContext(
    schemes=["sha256_crypt"],
    deprecated="auto",
    sha256_crypt__rounds=100000
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    logger.debug("Verifying password")
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    logger.debug("Hashing password")
    return pwd_context.hash(password)

def authenticate_user(db: Session, email: str, password: str):
    logger.debug(f"Attempting to authenticate user: {email}")
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        logger.debug(f"User not found: {email}")
        return None
    if not verify_password(password, user.password):
        logger.debug(f"Invalid password for user: {email}")
        return None
    logger.debug(f"User authenticated successfully: {email}")
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    logger.debug("Creating access token")
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logger.debug("Access token created successfully")
    return encoded_jwt

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> models.User:
    logger.debug("Getting current user from token")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            logger.debug("Token payload missing 'sub' field")
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError as e:
        logger.debug(f"JWT decode error: {str(e)}")
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.email == token_data.email).first()
    if user is None:
        logger.debug(f"User not found for email: {email}")
        raise credentials_exception
    logger.debug(f"Current user retrieved successfully: {email}")
    return user

async def get_current_active_user(
    current_user: models.User = Depends(get_current_user)
) -> models.User:
    logger.debug(f"Checking if user is active: {current_user.email}")
    if not current_user.is_active:
        logger.debug(f"User is not active: {current_user.email}")
        raise HTTPException(status_code=400, detail="Inactive user")
    logger.debug(f"User is active: {current_user.email}")
    return current_user 