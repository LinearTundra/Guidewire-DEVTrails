from datetime import datetime, timezone
from constants import ClaimStatus, ClaimType, EventType
from models import Claims
from database import claims
from services import gps_service, policy_service
import asyncio


RUNNING_TASKS: dict[str, asyncio.Task] = {}


async def insert_claim(worker_id: str, policy_id: str, trigger_event_id: str, trigger_event: EventType) -> str:
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
            trigger_events=[trigger_event],
            claim_amount=0,
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
        await claims.add_trigger_to_claim(str(claim_id), trigger_event_id, trigger_event)

    return claim_id


async def create_claim_bulk(workers: list[dict], trigger_event_id: str, trigger_event: EventType) -> int:
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
            trigger_event_id=trigger_event_id,
            trigger_event=trigger_event
        )
        for w in workers
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    success = [r for r in results if not isinstance(r, Exception)]

    return len(success)


async def auto_approve_claim(claim_id: str) -> bool:
    return await claims.resolve_claim(claim_id, ClaimStatus.AUTO_APPROVED)
async def manual_approve_claim(claim_id: str) -> bool:
    return await claims.resolve_claim(claim_id, ClaimStatus.APPROVED)
async def reject_claim(claim_id: str) -> bool:
    return await claims.resolve_claim(claim_id, ClaimStatus.REJECTED)
async def flag_claim(claim_id: str) -> bool:
    return await claims.update_claim_status(claim_id, ClaimStatus.FLAGGED)


async def resolve_trigger_in_claims(trigger_id) :
    tasks = [
        claims.remove_trigger_from_claim(claim_id, trigger_id) 
        for claim_id in RUNNING_TASKS
    ]
    await asyncio.gather(*tasks, return_exceptions=True)

async def close_resolved_claims():
    claim_ids = list(RUNNING_TASKS.keys())

    claim_docs = await asyncio.gather(
        *[claims.get_claim(cid) for cid in claim_ids],
        return_exceptions=True
    )

    tasks = []

    for claim_id, claim in zip(claim_ids, claim_docs):
        if not claim or isinstance(claim, Exception):
            continue

        triggers = claim.get("trigger_event_ids", [])
        if triggers:
            continue

        # stop monitoring
        task = RUNNING_TASKS.get(claim_id)
        remove_task(claim_id)

        if not task:
            continue

        task.cancel()

        try:
            result = await task

            # --- extract ---
            status = result["status"]
            distance = result.get("distance", 0)
            area = result.get("area", 0)

            policy_id = claim["policy_id"]
            claim_type = claim.get("claim_type", ClaimType.FULL_DAY)

            # --- store fraud checks ---
            fraud_checks = {
                "distance_meters": distance,
                "area_m2": area,
                "status": status
            }

            await claims.update_fraud_checks(claim_id, fraud_checks)

            # --- decision logic ---
            if status == "clean":
                payout = await policy_service.process_claim_payout(
                    policy_id=policy_id,
                    claim_type=claim_type
                )

                if payout > 0:
                    await claims.update_claim_amount(claim_id, payout)
                    tasks.append(auto_approve_claim(claim_id))
                else:
                    tasks.append(reject_claim(claim_id))

            elif status == "suspicious":
                tasks.append(flag_claim(claim_id))

            else:
                tasks.append(reject_claim(claim_id))

        except asyncio.CancelledError:
            # expected path — ignore
            continue
        except Exception as e:
            # don't silently fail
            print(f"Error resolving claim {claim_id}: {e}")
            tasks.append(flag_claim(claim_id))

    result = await asyncio.gather(*tasks, return_exceptions=True)

    success = [r for r in result if r is True]
    return len(success) 


def store_task(claim_id: str, task: asyncio.Task):
    RUNNING_TASKS[claim_id] = task


def remove_task(claim_id: str):
    RUNNING_TASKS.pop(claim_id, None)


async def recover_running_claims():
    active_claims = await claims.get_all_active_claims()

    for claim in active_claims:
        claim_id = str(claim["_id"])

        if claim_id in RUNNING_TASKS:
            continue

        worker_id = claim["worker_id"]
        start_time = claim.get("created_at")

        task = asyncio.create_task(
            gps_service.monitor_worker_movement(
                worker_id,
                claim_id,
                start_time
            )
        )

        store_task(claim_id, task)

