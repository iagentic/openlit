from sqlalchemy import Boolean, Column, Integer, String, DateTime, Float, MetaData
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid
import logging
import json
from clickhouse_sqlalchemy import Table, engines

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# Create a metadata object
metadata = MetaData()

# Create a base class for declarative models
Base = declarative_base(metadata=metadata)

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    __table__ = Table(
        "users",
        metadata,
        Column("id", String, primary_key=True, default=generate_uuid),
        Column("name", String, nullable=True),
        Column("email", String, nullable=False),
        Column("email_verified", DateTime, nullable=True),
        Column("password", String, nullable=True),
        Column("image", String, nullable=True),
        Column("is_active", Boolean, default=True),
        Column("created_at", DateTime, default=datetime.utcnow),
        Column("updated_at", DateTime, default=datetime.utcnow),
        engines.MergeTree(order_by='id')
    )

    def __init__(self, **kwargs):
        logger.debug(f"Creating new User instance with email: {kwargs.get('email')}")
        super().__init__(**kwargs)

class Account(Base):
    __tablename__ = "accounts"
    __table__ = Table(
        "accounts",
        metadata,
        Column("id", String, primary_key=True, default=generate_uuid),
        Column("user_id", String, nullable=False),
        Column("type", String, nullable=True),
        Column("provider", String, nullable=False),
        Column("provider_account_id", String, nullable=False),
        Column("token_type", String, nullable=True),
        Column("refresh_token", String, nullable=True),
        Column("access_token", String, nullable=True),
        Column("expires_at", Integer, nullable=True),
        Column("scope", String, nullable=True),
        Column("id_token", String, nullable=True),
        Column("created_at", DateTime, default=datetime.utcnow),
        Column("updated_at", DateTime, default=datetime.utcnow),
        engines.MergeTree(order_by='id')
    )

class Session(Base):
    __tablename__ = "sessions"
    __table__ = Table(
        "sessions",
        metadata,
        Column("id", String, primary_key=True, default=generate_uuid),
        Column("user_id", String, nullable=True),
        Column("session_token", String, nullable=False),
        Column("access_token", String, nullable=True),
        Column("expires", DateTime, nullable=False),
        Column("created_at", DateTime, default=datetime.utcnow),
        Column("updated_at", DateTime, default=datetime.utcnow),
        engines.MergeTree(order_by='id')
    )

class DatabaseConfig(Base):
    __tablename__ = "databaseconfig"
    __table__ = Table(
        "databaseconfig",
        metadata,
        Column("id", String, primary_key=True, default=generate_uuid),
        Column("name", String, nullable=False),
        Column("environment", String, default="production"),
        Column("username", String, default="admin"),
        Column("password", String, nullable=True),
        Column("host", String, default="127.0.0.1"),
        Column("port", String, default="8123"),
        Column("database", String, default="openlit"),
        Column("query", String, nullable=True),
        Column("created_at", DateTime, default=datetime.utcnow),
        Column("updated_at", DateTime, default=datetime.utcnow),
        Column("user_id", String, nullable=False),
        engines.MergeTree(order_by='id')
    )

class DatabaseConfigUser(Base):
    __tablename__ = "databaseconfiguser"
    __table__ = Table(
        "databaseconfiguser",
        metadata,
        Column("database_config_id", String, primary_key=True),
        Column("user_id", String, primary_key=True),
        Column("is_current", Boolean, default=False),
        Column("can_edit", Boolean, default=False),
        Column("can_share", Boolean, default=False),
        Column("can_delete", Boolean, default=False),
        Column("created_at", DateTime, default=datetime.utcnow, nullable=True),
        Column("updated_at", DateTime, default=datetime.utcnow, nullable=True),
        engines.MergeTree(order_by=['database_config_id', 'user_id'])
    )

class OpenGround(Base):
    __tablename__ = "openground"
    __table__ = Table(
        "openground",
        metadata,
        Column("id", String, primary_key=True, default=generate_uuid),
        Column("request_meta", String, nullable=False),
        Column("response_meta", String, nullable=False),
        Column("stats", String, nullable=False),
        Column("created_at", DateTime, default=datetime.utcnow),
        Column("user_id", String, nullable=False),
        Column("database_config_id", String, nullable=False),
        engines.MergeTree(order_by='id')
    )

class DatabaseConfigInvitedUser(Base):
    __tablename__ = "databaseconfiginviteduser"
    __table__ = Table(
        "databaseconfiginviteduser",
        metadata,
        Column("database_config_id", String, primary_key=True),
        Column("email", String, primary_key=True),
        Column("can_edit", Boolean, default=False),
        Column("can_share", Boolean, default=False),
        Column("can_delete", Boolean, default=False),
        engines.MergeTree(order_by=['database_config_id', 'email'])
    )

class APIKeys(Base):
    __tablename__ = "apikeys"
    __table__ = Table(
        "apikeys",
        metadata,
        Column("id", String, primary_key=True, default=generate_uuid),
        Column("name", String, default="default"),
        Column("api_key", String, nullable=False),
        Column("database_config_id", String, nullable=False),
        Column("is_deleted", Boolean, default=False),
        Column("created_at", DateTime, default=datetime.utcnow),
        Column("created_by_user_id", String, nullable=False),
        Column("deleted_at", DateTime, nullable=True),
        Column("deleted_by_user_id", String, nullable=True),
        engines.MergeTree(order_by='id')
    )

class ClickhouseMigrations(Base):
    __tablename__ = "clickhousemigrations"
    __table__ = Table(
        "clickhousemigrations",
        metadata,
        Column("id", String, primary_key=True, default=generate_uuid),
        Column("database_config_id", String, nullable=False),
        Column("clickhouse_migration_id", String, nullable=False),
        engines.MergeTree(order_by='id')
    )

class EvaluationConfigs(Base):
    __tablename__ = "evaluationconfigs"
    __table__ = Table(
        "evaluationconfigs",
        metadata,
        Column("id", String, primary_key=True, default=generate_uuid),
        Column("database_config_id", String, nullable=False),
        Column("provider", String, nullable=False),
        Column("model", String, nullable=False),
        Column("vault_id", String, nullable=False),
        Column("auto", Boolean, default=False),
        Column("recurring_time", String, nullable=False),
        Column("meta", String, nullable=False),
        engines.MergeTree(order_by='id')
    )

class Metrics(Base):
    __tablename__ = "metrics"
    __table__ = Table(
        "metrics",
        metadata,
        Column("id", String, primary_key=True, default=generate_uuid),
        Column("type", String, nullable=False),  # request, gpu, vector, llm
        Column("operation_type", String, nullable=True),
        Column("value", Float, nullable=False),
        Column("timestamp", DateTime, default=datetime.utcnow),
        Column("database_config_id", String, nullable=False),
        Column("user_id", String, nullable=False),
        engines.MergeTree(order_by='id')
    )

class GPUMetrics(Base):
    __tablename__ = "gpu_metrics"
    __table__ = Table(
        "gpu_metrics",
        metadata,
        Column("id", String, primary_key=True, default=generate_uuid),
        Column("utilization", Float, nullable=False),
        Column("temperature", Float, nullable=False),
        Column("power", Float, nullable=False),
        Column("timestamp", DateTime, default=datetime.utcnow),
        Column("database_config_id", String, nullable=False),
        Column("user_id", String, nullable=False),
        engines.MergeTree(order_by='id')
    )

class VectorMetrics(Base):
    __tablename__ = "vector_metrics"
    __table__ = Table(
        "vector_metrics",
        metadata,
        Column("id", String, primary_key=True, default=generate_uuid),
        Column("operation", String, nullable=False),
        Column("environment", String, nullable=False),
        Column("system", String, nullable=False),
        Column("application", String, nullable=False),
        Column("timestamp", DateTime, default=datetime.utcnow),
        Column("database_config_id", String, nullable=False),
        Column("user_id", String, nullable=False),
        engines.MergeTree(order_by='id')
    )

class LLMMetrics(Base):
    __tablename__ = "llm_metrics"
    __table__ = Table(
        "llm_metrics",
        metadata,
        Column("id", String, primary_key=True, default=generate_uuid),
        Column("endpoint", String, nullable=False),
        Column("token_count", Integer, nullable=False),
        Column("timestamp", DateTime, default=datetime.utcnow),
        Column("database_config_id", String, nullable=False),
        Column("user_id", String, nullable=False),
        engines.MergeTree(order_by='id')
    )

class VaultSecret(Base):
    __tablename__ = "vault_secrets"
    __table__ = Table(
        "vault_secrets",
        metadata,
        Column("id", String, primary_key=True, default=generate_uuid),
        Column("key", String, nullable=False),
        Column("value", String, nullable=False),
        Column("tags", String, nullable=True),  # Stored as JSON string
        Column("created_at", DateTime, default=datetime.utcnow),
        Column("updated_at", DateTime, default=datetime.utcnow),
        Column("user_id", String, nullable=False),
        engines.MergeTree(order_by='id')
    )

# Create tables with ClickHouse engine
for table in metadata.tables.values():
    table.dialect_options['clickhouse'] = {
        'engine': engines.MergeTree(),
        'cluster': None,  # No cluster for local development
        'order_by': 'id'  # Order by primary key
    } 