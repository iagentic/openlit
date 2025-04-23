from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base
import uuid
import logging

# Configure logging
logger = logging.getLogger(__name__)

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    email_verified = Column(DateTime, nullable=True)
    password = Column(String, nullable=True)
    image = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    accounts = relationship("Account", back_populates="user")
    sessions = relationship("Session", back_populates="user")
    db_configs = relationship("DatabaseConfigUser", back_populates="user")
    created_db_configs = relationship("DatabaseConfig", back_populates="created_by_user")
    open_grounds = relationship("OpenGround", back_populates="created_by_user")
    created_api_keys = relationship("APIKeys", back_populates="created_by_user", foreign_keys="APIKeys.created_by_user_id")
    deleted_api_keys = relationship("APIKeys", back_populates="deleted_by_user", foreign_keys="APIKeys.deleted_by_user_id")
    metrics = relationship("Metrics", back_populates="user")
    gpu_metrics = relationship("GPUMetrics", back_populates="user")
    vector_metrics = relationship("VectorMetrics", back_populates="user")
    llm_metrics = relationship("LLMMetrics", back_populates="user")
    vault_secrets = relationship("VaultSecret", back_populates="user")

    def __init__(self, **kwargs):
        logger.debug(f"Creating new User instance with email: {kwargs.get('email')}")
        super().__init__(**kwargs)

class Account(Base):
    __tablename__ = "accounts"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"))
    type = Column(String, nullable=True)
    provider = Column(String, nullable=False)
    provider_account_id = Column(String, nullable=False)
    token_type = Column(String, nullable=True)
    refresh_token = Column(String, nullable=True)
    access_token = Column(String, nullable=True)
    expires_at = Column(Integer, nullable=True)
    scope = Column(String, nullable=True)
    id_token = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="accounts")

class Session(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    session_token = Column(String, unique=True, nullable=False)
    access_token = Column(String, nullable=True)
    expires = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="sessions")

class DatabaseConfig(Base):
    __tablename__ = "databaseconfig"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, unique=True, nullable=False)
    environment = Column(String, default="production")
    username = Column(String, default="admin")
    password = Column(String, nullable=True)
    host = Column(String, default="127.0.0.1")
    port = Column(String, default="8123")
    database = Column(String, default="openlit")
    query = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(String, ForeignKey("users.id"))

    created_by_user = relationship("User", back_populates="created_db_configs")
    db_users = relationship("DatabaseConfigUser", back_populates="database_config")
    open_grounds = relationship("OpenGround", back_populates="database_config")
    db_invited_users = relationship("DatabaseConfigInvitedUser", back_populates="database_config")
    api_keys = relationship("APIKeys", back_populates="database_config")
    metrics = relationship("Metrics", back_populates="database_config")
    gpu_metrics = relationship("GPUMetrics", back_populates="database_config")
    vector_metrics = relationship("VectorMetrics", back_populates="database_config")
    llm_metrics = relationship("LLMMetrics", back_populates="database_config")

class DatabaseConfigUser(Base):
    __tablename__ = "databaseconfiguser"

    database_config_id = Column(String, ForeignKey("databaseconfig.id"), primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), primary_key=True)
    is_current = Column(Boolean, default=False)
    can_edit = Column(Boolean, default=False)
    can_share = Column(Boolean, default=False)
    can_delete = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)

    user = relationship("User", back_populates="db_configs")
    database_config = relationship("DatabaseConfig", back_populates="db_users")

class OpenGround(Base):
    __tablename__ = "openground"

    id = Column(String, primary_key=True, default=generate_uuid)
    request_meta = Column(String, nullable=False)
    response_meta = Column(String, nullable=False)
    stats = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(String, ForeignKey("users.id"))
    database_config_id = Column(String, ForeignKey("databaseconfig.id"))

    created_by_user = relationship("User", back_populates="open_grounds")
    database_config = relationship("DatabaseConfig", back_populates="open_grounds")

class DatabaseConfigInvitedUser(Base):
    __tablename__ = "databaseconfiginviteduser"

    database_config_id = Column(String, ForeignKey("databaseconfig.id"), primary_key=True)
    email = Column(String, primary_key=True)
    can_edit = Column(Boolean, default=False)
    can_share = Column(Boolean, default=False)
    can_delete = Column(Boolean, default=False)

    database_config = relationship("DatabaseConfig", back_populates="db_invited_users")

class APIKeys(Base):
    __tablename__ = "apikeys"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, default="default")
    api_key = Column(String, unique=True, nullable=False)
    database_config_id = Column(String, ForeignKey("databaseconfig.id"))
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by_user_id = Column(String, ForeignKey("users.id"))
    deleted_at = Column(DateTime, nullable=True)
    deleted_by_user_id = Column(String, ForeignKey("users.id"), nullable=True)

    database_config = relationship("DatabaseConfig", back_populates="api_keys")
    created_by_user = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_api_keys")
    deleted_by_user = relationship("User", foreign_keys=[deleted_by_user_id], back_populates="deleted_api_keys")

class ClickhouseMigrations(Base):
    __tablename__ = "clickhousemigrations"

    id = Column(String, primary_key=True, default=generate_uuid)
    database_config_id = Column(String, nullable=False)
    clickhouse_migration_id = Column(String, nullable=False)

class EvaluationConfigs(Base):
    __tablename__ = "evaluationconfigs"

    id = Column(String, primary_key=True, default=generate_uuid)
    database_config_id = Column(String, unique=True, nullable=False)
    provider = Column(String, nullable=False)
    model = Column(String, nullable=False)
    vault_id = Column(String, nullable=False)
    auto = Column(Boolean, default=False)
    recurring_time = Column(String, nullable=False)
    meta = Column(String, nullable=False)

class Metrics(Base):
    __tablename__ = "metrics"

    id = Column(String, primary_key=True, default=generate_uuid)
    type = Column(String, nullable=False)  # request, gpu, vector, llm
    operation_type = Column(String, nullable=True)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    database_config_id = Column(String, ForeignKey("databaseconfig.id"))
    user_id = Column(String, ForeignKey("users.id"))

    database_config = relationship("DatabaseConfig", back_populates="metrics")
    user = relationship("User", back_populates="metrics")

class GPUMetrics(Base):
    __tablename__ = "gpu_metrics"

    id = Column(String, primary_key=True, default=generate_uuid)
    utilization = Column(Float, nullable=False)
    temperature = Column(Float, nullable=False)
    power = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    database_config_id = Column(String, ForeignKey("databaseconfig.id"))
    user_id = Column(String, ForeignKey("users.id"))

    database_config = relationship("DatabaseConfig", back_populates="gpu_metrics")
    user = relationship("User", back_populates="gpu_metrics")

class VectorMetrics(Base):
    __tablename__ = "vector_metrics"

    id = Column(String, primary_key=True, default=generate_uuid)
    operation = Column(String, nullable=False)
    environment = Column(String, nullable=False)
    system = Column(String, nullable=False)
    application = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    database_config_id = Column(String, ForeignKey("databaseconfig.id"))
    user_id = Column(String, ForeignKey("users.id"))

    database_config = relationship("DatabaseConfig", back_populates="vector_metrics")
    user = relationship("User", back_populates="vector_metrics")

class LLMMetrics(Base):
    __tablename__ = "llm_metrics"

    id = Column(String, primary_key=True, default=generate_uuid)
    endpoint = Column(String, nullable=False)
    token_count = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    database_config_id = Column(String, ForeignKey("databaseconfig.id"))
    user_id = Column(String, ForeignKey("users.id"))

    database_config = relationship("DatabaseConfig", back_populates="llm_metrics")
    user = relationship("User", back_populates="llm_metrics")

class VaultSecret(Base):
    __tablename__ = "vault_secrets"

    id = Column(String, primary_key=True, default=generate_uuid)
    key = Column(String, unique=True, nullable=False)
    value = Column(String, nullable=False)
    tags = Column(String, nullable=True)  # Stored as JSON string
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(String, ForeignKey("users.id"))

    user = relationship("User", back_populates="vault_secrets") 