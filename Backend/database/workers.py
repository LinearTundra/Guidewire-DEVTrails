from database.Database import db
from models import Worker, Plan
from typing import Optional
from bson import ObjectId


async def create_worker(worker: Worker) -> Optional[str]:
    """
    Inserts a new worker document into the workers collection
    if the mobile number is not already inserted.
    
    Args:
        worker: Validated Worker pydantic model instance
        
    Returns:
        Inserted document ID as string
    """
    if await get_worker_by_mobile(worker.mobile) != None :
        return None
    result = await db.get_database().workers.insert_one(worker.model_dump())
    return str(result.inserted_id)


async def get_worker(worker_id: str) -> Optional[dict]:
    """
    Fetches a single worker by their MongoDB ObjectId.
    
    Args:
        worker_id: MongoDB ObjectId string
        
    Returns:
        Worker document as dict or None if not found
    """
    return await db.get_database().workers.find_one({"_id": ObjectId(worker_id)})


async def get_worker_by_mobile(mobile: str) -> Optional[dict]:
    """
    Fetches a single worker by mobile number.
    Used during login and duplicate registration checks.
    
    Args:
        mobile: Worker mobile number as string
        
    Returns:
        Worker document as dict or None if not found
    """
    return await db.get_database().workers.find_one({"mobile": mobile})


async def get_workers_by_zone(zone: str) -> list[dict]:
    """
    Fetches all workers operating in a specific zone.
    Used by trigger monitoring to find affected workers when a threshold is crossed.
    
    Args:
        zone: Zone name e.g. "Lajpat Nagar"
        
    Returns:
        List of worker documents
    """
    result = await db.get_database().workers.find({"zone": zone}).to_list(length=None)
    for worker in result :
        if worker is None :
            continue
        if "_id" not in worker :
            continue
        worker["_id"] = str(worker["_id"])
    return result


async def update_worker_streak(worker_id: str, streak: int) -> bool:
    """
    Updates the streak count for a worker.
    Called every Monday when a new policy is created.
    
    Args:
        worker_id: MongoDB ObjectId string
        streak: New streak value
        
    Returns:
        True if update was successful, False if worker not found
    """
    result = await db.get_database().workers.update_one(
        {"_id": ObjectId(worker_id)},
        {"$set": {"streak": streak}}
    )
    return result.modified_count > 0


async def update_worker_plan(worker_id: str, plan: Plan) -> bool:
    """
    Updates the active plan tier for a worker.
    
    Args:
        worker_id: MongoDB ObjectId string
        plan: New plan name from Plan enum
        
    Returns:
        True if update was successful, False if worker not found
    """
    result = await db.get_database().workers.update_one(
        {"_id": ObjectId(worker_id)},
        {"$set": {"plan": plan}}
    )
    return result.modified_count > 0


async def set_kyc_verified(worker_id: str) -> bool:
    """
    Marks a worker's KYC as verified.
    Called after successful Aadhaar verification via IDfy/Karza.
    
    Args:
        worker_id: MongoDB ObjectId string
        
    Returns:
        True if update was successful, False if worker not found
    """
    result = await db.get_database().workers.update_one(
        {"_id": ObjectId(worker_id)},
        {"$set": {"kyc_verified": True}}
    )
    return result.modified_count > 0


async def delete_worker(worker_id: str) -> bool:
    """
    Deletes a worker document. 
    Use with caution — also clean up related policies, claims and auth documents.
    
    Args:
        worker_id: MongoDB ObjectId string
        
    Returns:
        True if deletion was successful, False if worker not found
    """
    result = await db.get_database().workers.delete_one({"_id": ObjectId(worker_id)})
    return result.deleted_count > 0