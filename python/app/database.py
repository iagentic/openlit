from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import logging

# Configure logging
logger = logging.getLogger(__name__)

load_dotenv()

# Get ClickHouse connection details from environment variables
CLICKHOUSE_HOST = os.getenv("INIT_DB_HOST", "localhost")
CLICKHOUSE_PORT = os.getenv("INIT_DB_PORT", "8123")
CLICKHOUSE_DATABASE = os.getenv("INIT_DB_DATABASE", "openlit")
CLICKHOUSE_USER = os.getenv("INIT_DB_USERNAME", "default")
CLICKHOUSE_PASSWORD = os.getenv("INIT_DB_PASSWORD", "OPENLIT")

# Construct ClickHouse connection URL
SQLALCHEMY_DATABASE_URL = f"clickhouse://{CLICKHOUSE_USER}:{CLICKHOUSE_PASSWORD}@{CLICKHOUSE_HOST}:{CLICKHOUSE_PORT}/{CLICKHOUSE_DATABASE}"

logger.debug(f"Creating database engine for ClickHouse at {CLICKHOUSE_HOST}:{CLICKHOUSE_PORT}")
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "secure": False,
        "verify": False
    }
)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative models
Base = declarative_base()

def get_db():
    logger.debug("Creating new database session")
    db = SessionLocal()
    try:
        logger.debug("Yielding database session")
        yield db
    finally:
        logger.debug("Closing database session")
        db.close() 