from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import logging
from app.database import SessionLocal
from app.models import User

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

load_dotenv()

def delete_user():
    logger.info("Deleting existing user")
    db = SessionLocal()
    try:
        # Delete user if exists
        user = db.query(User).filter(User.email == "user@openlit.io").first()
        if user:
            db.delete(user)
            db.commit()
            logger.info("User deleted successfully")
        else:
            logger.info("User not found")
    except Exception as e:
        logger.error(f"Error deleting user: {str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    delete_user() 