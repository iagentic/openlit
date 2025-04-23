from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import logging

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")

def run_migration():
    logger.info("Starting migration to add is_active column to users table")
    
    # Create engine
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    
    # Check if the column already exists
    with engine.connect() as conn:
        # For SQLite, we need to check the table info
        result = conn.execute(text("PRAGMA table_info(users)"))
        columns = [row[1] for row in result.fetchall()]
        
        if "is_active" in columns:
            logger.info("Column 'is_active' already exists in users table")
            return
        
        # Add the column
        logger.info("Adding 'is_active' column to users table")
        conn.execute(text("ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT 1"))
        conn.commit()
        
        logger.info("Migration completed successfully")

if __name__ == "__main__":
    run_migration() 