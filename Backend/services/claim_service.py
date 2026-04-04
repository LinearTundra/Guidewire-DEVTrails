from constants import ClaimStatus, ClaimType
from models import Claims
from database import claims


async def insert_claim(worker_id: str, policy_id: str, trigger_event_id: str) -> str:
    """
    Creates a claim matching the Claims model.

    Args:
        worker_id: Unique id of the worker
        policy_id: Unique id of the active policy
        trigger_event_id: Unique id of the trigger event
    
    Returns:
        Unique claim_id of the newly created claim
    """

    claim = Claims(
        worker_id=worker_id,
        policy_id=policy_id,
        trigger_event_id=trigger_event_id,
        claim_amount=100,
        claim_type=ClaimType.FULL_DAY,
        status=ClaimStatus.MONITORING,
        fraud_checks={}
    )

    result = await claims.create_claim(claim)
    return result


async def create_claim_bulk(workers: list[dict], trigger_event_id: str) -> int:
    """
    Creates claims in bulk of maching event types.

    Args:
        workers: [{"worker_id": ..., "policy_id": ...}, ...]
        trigger_event_id: Unique id of the trigger event
    
    Returns:
        Number of claims created

    """
    count = 0
    for w in workers:
        await insert_claim(
            worker_id=w["worker_id"],
            policy_id=w["policy_id"],
            trigger_event_id=trigger_event_id
        )
        count += 1

    return count