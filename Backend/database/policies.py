from database.Database import db
from typing import Optional
from bson import ObjectId
from datetime import datetime, timezone
from models import Policies


async def create_policy(policy: Policies) -> str:
    """
    Inserts a new weekly policy document into the policies collection.
    Called every Monday when a worker's premium is debited.
    A new policy document is created each week — previous ones are
    deactivated but kept for history, streak calculation and payout records.
    
    Args:
        policy: Validated Policies pydantic model instance
        
    Returns:
        Inserted document ID as string
    """
    result = await db.get_database().policies.insert_one(policy.model_dump())
    return str(result.inserted_id)


async def get_policy(policy_id: str) -> Optional[dict]:
    """
    Fetches a single policy by its MongoDB ObjectId.
    
    Args:
        policy_id: MongoDB ObjectId string
        
    Returns:
        Policy document as dict or None if not found
    """
    return await db.get_database().policies.find_one({"_id": ObjectId(policy_id)})


async def get_active_policy(worker_id: str) -> Optional[dict]:
    """
    Fetches the currently active policy for a worker.
    A worker should only have one active policy at a time.
    
    Args:
        worker_id: MongoDB ObjectId string of the worker
        
    Returns:
        Active policy document as dict or None if no active policy found
    """
    return await db.get_database().policies.find_one(
        {
            "worker_id": worker_id,
            "is_active": True
        }
    )


async def get_policies_by_worker(worker_id: str) -> list[dict]:
    """
    Fetches all policies for a worker — current and historical.
    Used for subscription history display, similar to Netflix billing history.
    
    Args:
        worker_id: MongoDB ObjectId string of the worker
        
    Returns:
        List of policy documents ordered by created_at descending
    """
    return await db.get_database().policies.find(
        {"worker_id": worker_id}
    ).sort("created_at", -1).to_list(length=None)


async def get_active_policies_by_zone(zone: str) -> list[dict]:
    """
    Fetches all active policies for workers in a specific zone.
    Used by trigger monitoring to identify affected policyholders.
    
    Args:
        zone: Zone name e.g. "Lajpat Nagar"
        
    Returns:
        List of active policy documents
    """
    return await db.get_database().policies.find(
        {
            "zone": zone,
            "is_active": True
        }
    ).to_list(length=None)


async def deactivate_policy(policy_id: str) -> bool:
    """
    Marks a policy as inactive.
    Called at end of policy week or when worker cancels subscription.
    
    Args:
        policy_id: MongoDB ObjectId string
        
    Returns:
        True if update was successful, False if policy not found
    """
    result = await db.get_database().policies.update_one(
        {"_id": ObjectId(policy_id)},
        {"$set":
            {
                "is_active": False,
                "end_date": datetime.now(timezone.utc)
            }
        }
    )
    return result.modified_count > 0


async def complete_waiting_period(policy_id: str) -> bool:
    """
    Marks the waiting period as complete for a policy.
    Called after 2 weeks from first policy activation.
    
    Args:
        policy_id: MongoDB ObjectId string
        
    Returns:
        True if update was successful, False if policy not found
    """
    result = await db.get_database().policies.update_one(
        {"_id": ObjectId(policy_id)},
        {"$set": {"waiting_period_complete": True}}
    )
    return result.modified_count > 0