from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import logging
from app.database import SessionLocal
from app.models import User
from app.auth import get_password_hash

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

load_dotenv()

def create_initial_user():
    logger.info("Creating initial user")
    db = SessionLocal()
    try:
        # Check if user already exists
        user = db.query(User).filter(User.email == "user@openlit.io").first()
        if user:
            logger.info("User already exists")
            return
        
        # Create new user
        hashed_password = get_password_hash("OPENLIT")
        new_user = User(
            email="user@openlit.io",
            password=hashed_password,
            name="OpenLit User",
            is_active=True
        )
        
        db.add(new_user)
        db.commit()
        logger.info("Initial user created successfully")
        
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_initial_user() 