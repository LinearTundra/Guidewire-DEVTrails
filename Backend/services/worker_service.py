from datetime import datetime
from database.workers import get_workers_by_zone, get_worker
from models import TriggerEvents
from services.policy_service import get_worker_active_policy


policies_covering = {
    "rainfall" : ("Basic", "Standard", "Premium"),
    "flood" : ("Basic", "Standard", "Premium"),
    "aqi" : ("Standard", "Premium"),
    "heat" : ("Premium"),
    "bandh" : ("Premium"),
    "curfew" : ("Premium")
}

async def get_workers_covered_from_trigger(trigger: TriggerEvents) -> dict[str, str]:
    zone = trigger.zone

    workers = await get_workers_by_zone(zone)
    result = {}
    for worker in workers :
        policy = await get_worker_active_policy(str(worker["_id"]))
        if policy == None :
            continue
        if policy.get("plan", "") in policies_covering[trigger.event_type] :
            result[worker["_id"]] = policy["_id"]

    return result

async def worker_details(worker_id: str) :
    worker = await get_worker(worker_id)
    if worker is None :
        return None
    worker["_id"] = str(worker["_id"])
    return worker