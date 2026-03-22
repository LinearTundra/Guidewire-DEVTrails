from database.Database import db
from models import Auth
from typing import Optional
from datetime import datetime, timezone
import bcrypt


async def create_auth(auth: Auth) -> str:
    """
    Inserts a new auth document for a worker.
    Password is automatically hashed by the Auth pydantic model
    before reaching this function — never store plain passwords.
    Called once during worker onboarding after KYC verification.
    
    Args:
        auth: Validated Auth pydantic model instance
        
    Returns:
        Inserted document ID as string
    """
    result = await db.get_database().auth.insert_one(auth.model_dump())
    return str(result.inserted_id)


async def get_auth(id: str) -> Optional[dict]:
    """
    Fetches auth document by id.
    Used during login to retrieve stored hash for verification.
    
    Args:
        id: Worker's mobile or email
        
    Returns:
        Auth document as dict or None if not found
    """
    if '@' in id :
        return await db.get_database().auth.find_one({"email": id})
    else :
        return await db.get_database().auth.find_one({"mobile": id})


async def verify_password(id: str, plain_password: str) -> bool:
    """
    Verifies a plain password against the stored bcrypt hash.
    Fetches the auth document and uses bcrypt.checkpw() to compare.
    The bcrypt hash contains the salt so no separate salt lookup needed.
    
    Args:
        id: Worker's email or mobile
        plain_password: Plain password string from login request
        
    Returns:
        True if password matches, False if wrong password or user not found
    """
    auth = await get_auth(id)
    if not auth:
        return False
    
    if not bcrypt.checkpw(plain_password.encode(), auth["password"].encode()) :
        return False
    
    await update_last_login(auth["mobile"])
    return True


async def update_last_login(mobile: str) -> bool:
    """
    Updates the last_login timestamp for a worker after successful login.
    
    Args:
        mobile: Worker's unique mobile number
        
    Returns:
        True if update was successful, False if user not found
    """
    result = await db.get_database().auth.update_one(
        {"mobile": mobile},
        {"$set": {"last_login": datetime.now(timezone.utc)}}
    )
    return result.modified_count > 0


async def update_password(id: str, new_password: str) -> bool:
    """
    Updates the password for a worker.
    Hashes the new password before storing.
    
    Args:
        id: Worker's mobile or email
        new_password: New plain password string — hashed before storing
        
    Returns:
        True if update was successful, False if user not found
    """
    field = "mobile"
    if '@' in id :
        field = 'email'
    hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
    result = await db.get_database().auth.update_one(
        {field: id},
        {"$set": {"hashed_password": hashed}}
    )
    return result.modified_count > 0


async def delete_auth(worker_id: str) -> bool:
    """
    Deletes the auth document for a worker.
    Called when a worker account is permanently deleted.
    Always delete auth alongside the worker document.
    
    Args:
        worker_id: MongoDB ObjectId string of the worker
        
    Returns:
        True if deletion was successful, False if not found
    """
    result = await db.get_database().auth.delete_one({"worker_id": worker_id})
    return result.deleted_count > 0