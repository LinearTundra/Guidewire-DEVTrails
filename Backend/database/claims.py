from database.Database import db
from models import Claims
from constants import ClaimStatus
from typing import Optional
from bson import ObjectId
from datetime import datetime, timezone


async def create_claim(claim: Claims) -> str:
    """
    Inserts a new claim document into the claims collection.
    Claims are always system-generated — never manually filed by workers.
    Called automatically when a trigger event fires in a worker's zone.
    
    Args:
        claim: Validated Claims pydantic model instance
        
    Returns:
        Inserted document ID as string
    """
    result = await db.get_database().claims.insert_one(claim.model_dump())
    return str(result.inserted_id)


async def get_claim(claim_id: str) -> Optional[dict]:
    """
    Fetches a single claim by its MongoDB ObjectId.
    
    Args:
        claim_id: MongoDB ObjectId string
        
    Returns:
        Claim document as dict or None if not found
    """
    return await db.get_database().claims.find_one({"_id": ObjectId(claim_id)})


async def get_claims_by_worker(worker_id: str, claimStatusList: list[ClaimStatus] = None) -> list[dict]:
    """
    Fetches all claims for a worker — current and historical.
    Used for payout history display in worker dashboard.
    
    Args:
        worker_id: MongoDB ObjectId string of the worker
        
    Returns:
        List of claim documents ordered by created_at descending
    """
    fields = {"worker_id": worker_id}
    if claimStatusList :
        fields["status"] = {"$in" : claimStatusList}
    return await db.get_database().claims.find(fields).sort("created_at", -1).to_list(length=None)


async def get_last_claim_by_worker(worker_id: str, claimStatusList: list[ClaimStatus] = None) -> list[dict]:
    """
    Fetches all claims for a worker — current and historical.
    Used for payout history display in worker dashboard.
    
    Args:
        worker_id: MongoDB ObjectId string of the worker
        
    Returns:
        List of claim documents ordered by created_at descending
    """
    fields = {"worker_id": worker_id}
    if claimStatusList :
        fields["status"] = {"$in" : claimStatusList}
    return await db.get_database().claims.find_one(
        fields,
        sort = [("created_at", -1)]
    )


async def get_claims_by_policy(policy_id: str) -> list[dict]:
    """
    Fetches all claims under a specific policy.
    Used to calculate total payout amount against max_payout cap for the week.
    
    Args:
        policy_id: MongoDB ObjectId string of the policy
        
    Returns:
        List of claim documents for that policy
    """
    return await db.get_database().claims.find(
        {"policy_id": policy_id}
    ).to_list(length=None)


async def get_claims_by_status(status: ClaimStatus) -> list[dict]:
    """
    Fetches all claims with a specific status.
    Used by admin dashboard to show flagged or manual review queues.
    
    Args:
        status: ClaimStatus enum value
        
    Returns:
        List of claim documents with matching status
    """
    return await db.get_database().claims.find(
        {"status": status.value}
    ).sort("created_at", -1).to_list(length=None)


async def get_weekly_payout_total(policy_id: str) -> float:
    """
    Calculates total payout amount for all approved claims under a policy.
    Used to check if worker has hit the max_payout cap for the week
    before initiating a new payout.
    
    Args:
        policy_id: MongoDB ObjectId string of the active policy
        
    Returns:
        Sum of claim_amount for all auto_approved claims under this policy
    """
    cursor = db.get_database().claims.find(
        {
            "policy_id": policy_id,
            "status": {"$in": [ClaimStatus.AUTO_APPROVED.value, ClaimStatus.APPROVED.value]}
        }
    )
    claims = await cursor.to_list(length=None)
    return sum(c["claim_amount"] for c in claims)


async def update_claim_status(claim_id: str, status: ClaimStatus) -> bool:
    """
    Updates the status of a claim.
    Used by fraud detection pipeline to move claim through its lifecycle:
    MONITORING → AUTO_APPROVED / FLAGGED → MANUAL_REVIEW / REJECTED
    
    Args:
        claim_id: MongoDB ObjectId string
        status: New ClaimStatus enum value
        
    Returns:
        True if update was successful, False if claim not found
    """
    result = await db.get_database().claims.update_one(
        {"_id": ObjectId(claim_id)},
        {"$set": {"status": status.value}}
    )
    return result.modified_count > 0


async def resolve_claim(claim_id: str, status: ClaimStatus) -> bool:
    """
    Marks a claim as resolved by setting status and resolved_at timestamp.
    Called when a claim reaches a terminal status — AUTO_APPROVED or REJECTED.
    
    Args:
        claim_id: MongoDB ObjectId string
        status: Terminal ClaimStatus — AUTO_APPROVED or REJECTED
        
    Returns:
        True if update was successful, False if claim not found
    """
    result = await db.get_database().claims.update_one(
        {"_id": ObjectId(claim_id)},
        {
            "$set": {
                "status": status.value,
                "resolved_at": datetime.now(timezone.utc)
            }
        }
    )
    return result.modified_count > 0