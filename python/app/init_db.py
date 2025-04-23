from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import logging
from app.models import Base, metadata

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

load_dotenv()

# Get ClickHouse connection details from environment variables
CLICKHOUSE_HOST = os.getenv("INIT_DB_HOST", "localhost")
CLICKHOUSE_PORT = os.getenv("INIT_DB_PORT", "8123")
CLICKHOUSE_DATABASE = os.getenv("INIT_DB_DATABASE", "openlit")
CLICKHOUSE_USER = os.getenv("INIT_DB_USERNAME", "default")
CLICKHOUSE_PASSWORD = os.getenv("INIT_DB_PASSWORD", "OPENLIT")

# Construct ClickHouse connection URL
SQLALCHEMY_DATABASE_URL = f"clickhouse://{CLICKHOUSE_USER}:{CLICKHOUSE_PASSWORD}@{CLICKHOUSE_HOST}:{CLICKHOUSE_PORT}/{CLICKHOUSE_DATABASE}"

def test_connection(engine):
    try:
        with engine.connect() as conn:
            logger.debug("Testing connection to ClickHouse...")
            result = conn.execute(text("SELECT 1"))
            logger.debug("Connection test successful")
            return True
    except Exception as e:
        logger.error(f"Connection test failed: {str(e)}")
        return False

def init_db():
    logger.info(f"Connecting to ClickHouse at {CLICKHOUSE_HOST}:{CLICKHOUSE_PORT}")
    logger.debug(f"Using database URL: {SQLALCHEMY_DATABASE_URL}")
    
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={
            "secure": False,
            "verify": False
        }
    )
    
    # Test connection first
    if not test_connection(engine):
        logger.error("Failed to connect to ClickHouse. Please check if the server is running and accessible.")
        return
    
    # Create database if it doesn't exist
    with engine.connect() as conn:
        logger.info(f"Creating database {CLICKHOUSE_DATABASE} if it doesn't exist")
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {CLICKHOUSE_DATABASE}"))
    
    # Create tables
    logger.info("Creating tables")
    try:
        metadata.create_all(engine)
        logger.info("Database initialization complete")
    except Exception as e:
        logger.error(f"Error creating tables: {str(e)}")
        raise

if __name__ == "__main__":
    init_db() 