from datetime import datetime, timezone
from constants import ClaimStatus, ClaimType, EventType
from models import Claims
from database import claims
from services import gps_service, policy_service, ml_service, trigger_service, worker_service
import asyncio


RUNNING_TASKS: dict[str, asyncio.Task] = {}


async def insert_claim(worker_id: str, policy_id: str, trigger_event_id: str, trigger_event: EventType) -> str:
    """
    Creates a claim matching the Claims model.

    Args:
        worker_id: Unique id of the worker
        policy_id: Unique id of the active policy
        trigger_event_id: Unique id of the trigger event
        trigger_event: Type of event
    
    Returns:
        Unique claim_id of the newly created claim
    """

    print(f"Creating claim of {worker_id}")
    try :
        active_claim = await claims.get_active_claim_by_worker(worker_id)
        print(f"Last claim found {active_claim}")
    except Exception as e :
        print(e)
        return
    if active_claim is None :
        print("No active claim found")
        try :
            claim = Claims(
                worker_id=worker_id,
                policy_id=policy_id,
                trigger_event_id=[trigger_event_id],
                trigger_events=[trigger_event],
                claim_amount=0,
                claim_type=ClaimType.FULL_DAY,
                status=ClaimStatus.MONITORING,
            )
        except Exception as e :
            print(e)
            return
        print(f"Inserting claim of {worker_id}")
        claim_id = await claims.create_claim(claim)
        print(f"Inserted claim {claim_id}, Monitoring worker {worker_id}")
        task = asyncio.create_task(gps_service.monitor_worker_movement(worker_id, claim_id, datetime.now(timezone.utc)))
        store_task(claim_id, task)
    else :
        print("Fetched active claim")
        claim_id = active_claim.get("_id")
        if claim_id is None :
            return None
        await claims.add_trigger_to_claim(str(claim_id), trigger_event_id, trigger_event)
    print("Created and Inserted claims in db.")
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
    print(f"Inserting in claims bulk of {len(workers)} workers.")
    results = await asyncio.gather(*tasks, return_exceptions=True)

    success = [r for r in results if not isinstance(r, Exception)]
    print(f"Inserted {len(success)}")

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
    try :
        tasks = [
            asyncio.create_task(claims.remove_trigger_from_claim(claim_id, trigger_id))
            for claim_id in RUNNING_TASKS
        ]
        result = await asyncio.gather(*tasks, return_exceptions=True)
        print(f"\n-----\n{tasks}\n-----\n")
        print(f"\n-----\n{result}\n-----\n")
    except Exception as e :
        print(e)

async def evaluate_claim(claim: dict, result: dict) -> dict:
    gps_status = result["status"]
    distance = result.get("distance", 0)
    area = result.get("area", 0)
    gps_checks = result.get("fraud_checks", {})

    # ---- ML payload ----
    ml_payload = await build_ml_payload(claim["worker_id"], distance)

    ml_result = await ml_service.get_risk_score(ml_payload)

    final_status, payout = derive_final_status(gps_status, ml_result)

    fraud_checks = build_fraud_checks(
        distance,
        area,
        gps_checks,
        ml_result,
        final_status
    )

    return (
        {
            "final_status": final_status,
            "fraud_checks": fraud_checks
        },
        payout
    )

async def build_ml_payload(worker_id: str, distance: float) -> dict:
    try :
        worker, claims = await asyncio.gather(
            worker_service.worker_details(worker_id),
            get_claims_this_week(worker_id)
        )

        if not worker:
            raise ValueError("Worker not found")
    except Exception as e :
        print(e)
        worker = {}
        claims = {}
    print("DEBUG worker earnings:", worker.get("weekly_earnings"))
    return {
        "precip_mm": 0,
        "temperature_celsius": 25,
        "humidity": 50,
        "aqi": 100,

        "hours_worked": 10,
        "distance_km": distance / 1000,
        "orders_completed": 0,
        "avg_speed": (distance / 1000) / 8,

        "claims_last_week": len(claims),
        "weekly_earning": worker.get("weekly_earnings", 6000),
        "hours_inactive": 14,

        "base_price": 25
    }

def derive_final_status(gps_status: str, ml_result: dict | None) -> str:
    if not ml_result:
        return gps_status

    ml_flag = ml_result.get("fraud_status")

    if ml_flag == "fraud":
        return "fraud", 0

    payout = float(f"{ml_result.get("payout", 0):.02f}")
    if ml_flag == "suspicious" and gps_status == "clean":
        return "suspicious", payout
    return gps_status, payout

def build_fraud_checks(distance, area, gps_checks, ml_result, final_status):
    return {
        "gps": {
            "distance_m": distance,
            "area_m2": area,
            **gps_checks
        },
        "ml": ml_result,
        "final_status": final_status
    }

async def execute_claim_decision(claim_id: str, claim: dict, final_status: str, payout: float) :
    policy_id = claim["policy_id"]
    claim_type = claim.get("claim_type", ClaimType.FULL_DAY)

    if final_status == "clean":
        payout = await policy_service.process_claim_payout(
            policy_id,
            payout
        )
        print("DEBUG payout:", payout)

        if payout > 0:
            await claims.update_claim_amount(claim_id, payout)
            return await auto_approve_claim(claim_id)

        return await reject_claim(claim_id)

    if final_status == "suspicious":
        return await flag_claim(claim_id)

    return await reject_claim(claim_id)

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

        if claim.get("trigger_event_id"):
            continue

        task = RUNNING_TASKS.get(claim_id)
        remove_task(claim_id)

        if not task:
            continue

        task.cancel()

        try:
            result = await task

            evaluation, payout = await evaluate_claim(claim, result)

            await claims.update_fraud_checks(
                claim_id,
                evaluation["fraud_checks"]
            )

            tasks.append(
                execute_claim_decision(
                    claim_id,
                    claim,
                    evaluation["final_status"],
                    payout
                )
            )
            print(RUNNING_TASKS)

        except asyncio.CancelledError:
            continue

        except Exception as e:
            print(f"[ERROR] claim {claim_id}: {e}")
            tasks.append(flag_claim(claim_id))

    result = await asyncio.gather(*tasks, return_exceptions=True)
    return sum(1 for r in result if r is True)


def store_task(claim_id: str, task: asyncio.Task):
    RUNNING_TASKS[claim_id] = task


def remove_task(claim_id: str):
    RUNNING_TASKS.pop(claim_id, None)

async def recover_running_claims():
    print("Recovering Claims.")
    active_claims = await claims.get_all_active_claims()

    for claim in active_claims:
        claim_id = str(claim["_id"])
        if claim_id in RUNNING_TASKS:
            continue
        event_ids = claim.get("trigger_event_id", [])
        # -------------------------
        # Clean stale triggers
        # -------------------------
        for event_id in event_ids:
            try:
                trigger = await trigger_service.trigger_event_details(event_id)
                if trigger is None :
                    continue
                if not trigger.get("is_active", False):
                    await resolve_trigger_in_claims(event_id)
            except Exception:
                continue

        # -------------------------
        # Restart monitoring
        # -------------------------
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
    

async def get_claims_this_week(worker_id: str) :
    return await claims.get_worker_weekly_claims(worker_id)