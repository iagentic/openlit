from sqlalchemy.orm import Session
from . import models
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)

def get_secrets(db: Session, user_id: str, key: Optional[str] = None, tags: Optional[List[str]] = None):
    query = db.query(models.VaultSecret).filter(
        models.VaultSecret.user_id == user_id,
        models.VaultSecret.is_deleted == False
    )
    
    if key:
        query = query.filter(models.VaultSecret.key == key)
    
    if tags:
        for tag in tags:
            query = query.filter(models.VaultSecret.tags.contains([tag]))
    
    return query.all()

def set_secret(db: Session, user_id: str, key: str, value: str, tags: Optional[List[str]] = None):
    # Check if secret already exists
    existing_secret = db.query(models.VaultSecret).filter(
        models.VaultSecret.user_id == user_id,
        models.VaultSecret.key == key,
        models.VaultSecret.is_deleted == False
    ).first()
    
    if existing_secret:
        # Update existing secret
        existing_secret.value = value
        if tags:
            existing_secret.tags = tags
        db.commit()
        logger.debug(f"Updated secret for key: {key}")
        return existing_secret
    
    # Create new secret
    new_secret = models.VaultSecret(
        user_id=user_id,
        key=key,
        value=value,
        tags=tags or []
    )
    db.add(new_secret)
    db.commit()
    db.refresh(new_secret)
    logger.debug(f"Created new secret for key: {key}")
    return new_secret

def delete_secret(db: Session, user_id: str, key: str):
    secret = db.query(models.VaultSecret).filter(
        models.VaultSecret.user_id == user_id,
        models.VaultSecret.key == key,
        models.VaultSecret.is_deleted == False
    ).first()
    
    if secret:
        secret.is_deleted = True
        db.commit()
        logger.debug(f"Soft deleted secret for key: {key}")
        return True
    
    return False 