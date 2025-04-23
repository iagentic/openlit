from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models
from app.auth import get_password_hash

def create_test_user():
    db = SessionLocal()
    try:
        # Check if user already exists
        user = db.query(models.User).filter(models.User.email == "user@openlit.io").first()
        if user:
            print("User already exists")
            return

        # Create new user
        hashed_password = get_password_hash("openlituser")
        db_user = models.User(
            email="user@openlit.io",
            password=hashed_password,
            name="Test User"
        )
        db.add(db_user)
        db.commit()
        print("Test user created successfully")
    finally:
        db.close()

if __name__ == "__main__":
    # Create tables
    models.Base.metadata.create_all(bind=engine)
    # Create test user
    create_test_user() 