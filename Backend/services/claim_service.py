from datetime import datetime, timezone
from constants import ClaimStatus, ClaimType
from models import Claims
from database import claims
from services import gps_service
import asyncio


RUNNING_TASKS: dict[str, asyncio.Task] = {}


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

    active_claim = await claims.get_active_claim_by_worker(worker_id)
    if active_claim is None :
        claim = Claims(
            worker_id=worker_id,
            policy_id=policy_id,
            trigger_event_id=[trigger_event_id],
            claim_amount=100,
            claim_type=ClaimType.FULL_DAY,
            status=ClaimStatus.MONITORING,
            fraud_checks={}
        )
        claim_id = await claims.create_claim(claim)
        task = asyncio.create_task(gps_service.monitor_worker_movement(worker_id, claim_id, datetime.now(timezone.utc)))
        store_task(claim_id, task)
    else :
        claim_id = active_claim.get("_id")
        if claim_id is None :
            return None
        await claims.add_trigger_to_claim(str(claim_id), trigger_event_id)

    return claim_id


async def create_claim_bulk(workers: list[dict], trigger_event_id: str) -> int:
    """
    Creates claims in bulk of maching event types.

    Args:
        workers: [{"worker_id": ..., "policy_id": ...}, ...]
        trigger_event_id: Unique id of the trigger event
    
    Returns:
        Number of claims created

    """
    tasks = [
        insert_claim(
            worker_id=w["worker_id"],
            policy_id=w["policy_id"],
            trigger_event_id=trigger_event_id
        )
        for w in workers
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    success = [r for r in results if not isinstance(r, Exception)]

    return len(success)


async def stop_monitoring_by_trigger(trigger_id: str):
    active_claims = await claims.get_claims_by_trigger(trigger_id)

    for claim in active_claims:
        claim_id = claim["_id"]

        task = RUNNING_TASKS.get(claim_id)
        remove_task(claim_id)
        
        if task is None :
            continue
        task.cancel()

        try :
            result = await task
        except asyncio.CancelledError as e :
            print(e)

async def auto_approve_claim(claim_id: str) -> bool:
    return await claims.resolve_claim(claim_id, ClaimStatus.AUTO_APPROVED)
async def manual_approve_claim(claim_id: str) -> bool:
    return await claims.resolve_claim(claim_id, ClaimStatus.APPROVED)
async def reject_claim(claim_id: str) -> bool:
    return await claims.resolve_claim(claim_id, ClaimStatus.REJECTED)
async def flag_claim(claim_id: str) -> bool:
    return await claims.update_claim_status(claim_id, ClaimStatus.FLAGGED)


def store_task(claim_id: str, task: asyncio.Task):
    RUNNING_TASKS[claim_id] = task


def remove_task(claim_id: str):
    RUNNING_TASKS.pop(claim_id, None)