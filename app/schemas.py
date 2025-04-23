from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime
import re
import logging

# Configure logging
logger = logging.getLogger(__name__)

class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    image: Optional[str] = None

    def __init__(self, **kwargs):
        logger.debug(f"Creating new UserBase instance with email: {kwargs.get('email')}")
        super().__init__(**kwargs)

    @validator('email')
    def validate_email(cls, v):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", v):
            raise ValueError('Invalid email format')
        return v

class UserCreate(UserBase):
    password: str

    def __init__(self, **kwargs):
        logger.debug(f"Creating new UserCreate instance with email: {kwargs.get('email')}")
        super().__init__(**kwargs)

class UserUpdate(BaseModel):
    current_password: Optional[str] = None
    new_password: Optional[str] = None
    name: Optional[str] = None

class User(UserBase):
    id: str
    email_verified: Optional[datetime] = None
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    def __init__(self, **kwargs):
        logger.debug(f"Creating new User instance with id: {kwargs.get('id')}")
        super().__init__(**kwargs)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class DatabaseConfigBase(BaseModel):
    name: str
    environment: str = "production"
    username: str = "admin"
    password: Optional[str] = None
    host: str = "127.0.0.1"
    port: str = "8123"
    database: str = "openlit"
    query: Optional[str] = None

class DatabaseConfigCreate(DatabaseConfigBase):
    pass

class DatabaseConfig(DatabaseConfigBase):
    id: str
    created_at: datetime
    updated_at: datetime
    user_id: str

    class Config:
        from_attributes = True

class DatabaseConfigUserBase(BaseModel):
    is_current: bool = False
    can_edit: bool = False
    can_share: bool = False
    can_delete: bool = False

class DatabaseConfigUserCreate(DatabaseConfigUserBase):
    database_config_id: str
    user_id: str

class DatabaseConfigUser(DatabaseConfigUserBase):
    database_config_id: str
    user_id: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class APIKeyBase(BaseModel):
    name: str = "default"
    database_config_id: str

class APIKeyCreate(APIKeyBase):
    pass

class APIKey(APIKeyBase):
    id: str
    api_key: str
    is_deleted: bool
    created_at: datetime
    created_by_user_id: str
    deleted_at: Optional[datetime] = None
    deleted_by_user_id: Optional[str] = None

    class Config:
        from_attributes = True 