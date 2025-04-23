from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
from . import models, schemas, auth
from .database import engine, get_db
import logging
from typing import Optional, List
import json

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

# Metrics Routes
@app.post("/metrics/request/total")
async def get_total_requests(
    params: schemas.MetricParams,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    logger.debug(f"Getting total requests for time limit: {params.timeLimit}")
    # Implementation for getting total requests
    return {"total": 0}  # Placeholder

@app.post("/metrics/request/time")
async def get_requests_per_time(
    params: schemas.MetricParams,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    logger.debug(f"Getting requests per time for time limit: {params.timeLimit}")
    # Implementation for getting requests per time
    return {"data": []}  # Placeholder

@app.post("/metrics/request/duration/average")
async def get_average_request_duration(
    params: schemas.MetricParams,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    logger.debug(f"Getting average request duration for time limit: {params.timeLimit}")
    # Implementation for getting average request duration
    return {"average": 0}  # Placeholder

# GPU Metrics Routes
@app.post("/metrics/gpu/utilization/average")
async def get_average_gpu_utilization(
    params: schemas.MetricParams,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    logger.debug(f"Getting average GPU utilization for time limit: {params.timeLimit}")
    # Implementation for getting average GPU utilization
    return {"average": 0}  # Placeholder

@app.post("/metrics/gpu/utilization/time")
async def get_gpu_utilization_per_time(
    params: schemas.MetricParams,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    logger.debug(f"Getting GPU utilization per time for time limit: {params.timeLimit}")
    # Implementation for getting GPU utilization per time
    return {"data": []}  # Placeholder

@app.post("/metrics/gpu/temperature/average")
async def get_average_gpu_temperature(
    params: schemas.MetricParams,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    logger.debug(f"Getting average GPU temperature for time limit: {params.timeLimit}")
    # Implementation for getting average GPU temperature
    return {"average": 0}  # Placeholder

# Vector Metrics Routes
@app.post("/metrics/vector/environment")
async def get_vector_metrics_by_environment(
    params: schemas.MetricParams,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    logger.debug(f"Getting vector metrics by environment for time limit: {params.timeLimit}")
    # Implementation for getting vector metrics by environment
    return {"data": []}  # Placeholder

@app.post("/metrics/vector/system")
async def get_vector_metrics_by_system(
    params: schemas.MetricParams,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    logger.debug(f"Getting vector metrics by system for time limit: {params.timeLimit}")
    # Implementation for getting vector metrics by system
    return {"data": []}  # Placeholder

@app.post("/metrics/vector/application")
async def get_vector_metrics_by_application(
    params: schemas.MetricParams,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    logger.debug(f"Getting vector metrics by application for time limit: {params.timeLimit}")
    # Implementation for getting vector metrics by application
    return {"data": []}  # Placeholder

# LLM Metrics Routes
@app.post("/metrics/llm/endpoint")
async def get_llm_metrics_by_endpoint(
    params: schemas.MetricParams,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    logger.debug(f"Getting LLM metrics by endpoint for time limit: {params.timeLimit}")
    # Implementation for getting LLM metrics by endpoint
    return {"data": []}  # Placeholder

@app.post("/metrics/llm/token/request/average")
async def get_average_tokens_per_request(
    params: schemas.MetricParams,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    logger.debug(f"Getting average tokens per request for time limit: {params.timeLimit}")
    # Implementation for getting average tokens per request
    return {"average": 0}  # Placeholder

# Vault Routes
@app.post("/vault/get-secrets")
async def get_vault_secrets(
    key: Optional[str] = None,
    tags: Optional[List[str]] = None,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    logger.debug(f"Getting vault secrets for key: {key}, tags: {tags}")
    query = db.query(models.VaultSecret).filter(models.VaultSecret.user_id == current_user.id)
    
    if key:
        query = query.filter(models.VaultSecret.key == key)
    if tags:
        # Assuming tags are stored as JSON string
        for tag in tags:
            query = query.filter(models.VaultSecret.tags.contains(tag))
    
    secrets = query.all()
    return {"secrets": [{"key": s.key, "value": s.value} for s in secrets]}

@app.post("/vault/set-secret")
async def set_vault_secret(
    secret: schemas.VaultSecretCreate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    logger.debug(f"Setting vault secret for key: {secret.key}")
    db_secret = models.VaultSecret(
        **secret.dict(),
        user_id=current_user.id,
        tags=json.dumps(secret.tags) if secret.tags else None
    )
    db.add(db_secret)
    db.commit()
    db.refresh(db_secret)
    return {"key": db_secret.key, "value": db_secret.value} 