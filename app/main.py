from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
from . import models, schemas, auth
from .database import engine, get_db
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="OpenLit API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3003"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add middleware to log all requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.debug(f"Request: {request.method} {request.url}")
    logger.debug(f"Headers: {request.headers}")
    
    response = await call_next(request)
    
    logger.debug(f"Response status: {response.status_code}")
    return response

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    logger.debug(f"Login attempt for user: {form_data.username}")
    
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        logger.debug(f"Authentication failed for user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    logger.debug(f"Authentication successful for user: {form_data.username}")
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        password=hashed_password,
        name=user.name,
        image=user.image
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(auth.get_current_active_user)):
    return current_user

@app.put("/users/me/", response_model=schemas.User)
async def update_user(
    user_update: schemas.UserUpdate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    if user_update.current_password and user_update.new_password:
        if not auth.verify_password(user_update.current_password, current_user.password):
            raise HTTPException(status_code=400, detail="Incorrect password")
        current_user.password = auth.get_password_hash(user_update.new_password)
    
    if user_update.name is not None:
        current_user.name = user_update.name
    
    db.commit()
    db.refresh(current_user)
    return current_user

# Database Config Routes
@app.post("/database-configs/", response_model=schemas.DatabaseConfig)
async def create_database_config(
    config: schemas.DatabaseConfigCreate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    db_config = models.DatabaseConfig(**config.dict(), user_id=current_user.id)
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    return db_config

@app.get("/database-configs/", response_model=list[schemas.DatabaseConfig])
async def list_database_configs(
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    return db.query(models.DatabaseConfig).filter(
        models.DatabaseConfig.user_id == current_user.id
    ).all()

# API Key Routes
@app.post("/api-keys/", response_model=schemas.APIKey)
async def create_api_key(
    api_key: schemas.APIKeyCreate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    import secrets
    db_api_key = models.APIKeys(
        **api_key.dict(),
        api_key=f"olit_{secrets.token_urlsafe(32)}",
        created_by_user_id=current_user.id
    )
    db.add(db_api_key)
    db.commit()
    db.refresh(db_api_key)
    return db_api_key

@app.get("/api-keys/", response_model=list[schemas.APIKey])
async def list_api_keys(
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    return db.query(models.APIKeys).filter(
        models.APIKeys.created_by_user_id == current_user.id,
        models.APIKeys.is_deleted == False
    ).all() 