from datetime import datetime, timezone
from services import gps_service, claim_service
from constants import EventType, Severity
from database import trigger_events
from models import TriggerEvents


# TEMP: hardcoded workers
DUMMY_WORKERS = {
    "69c02315a762ca801b7c810d":"69c029cc2331847984fa7c5c",
    "69c02315a762ca801b7c810e":"69c029cc2331847984fa7c5d",
    "69c02315a762ca801b7c810f":"69c029cc2331847984fa7c5e"
}

async def create_trigger(event_type: EventType, source: str="Mocked") :
    event = TriggerEvents(
        event_type=event_type,
        source=source,
        state="Delhi",
        city="Delhi",
        zone="Zone-1",
        threshold_value="50",
        severity=Severity.RED,
        start_time=datetime.now(timezone.utc),
        is_active=True,
        affected_workers=list(DUMMY_WORKERS.keys())
    )

    return await trigger_events.create_trigger_event(event)

async def simulate_trigger(trigger_event: EventType) -> int:
    """
    Simulates a disruption event.
    
    Flow:
    - define time window
    - check inactivity
    - create claims
    """
    # now = datetime.utcnow()
    # start = now - timedelta(hours=2)

    trigger_id = await create_trigger(trigger_event)
    info = []

    for worker_id, policy_id in DUMMY_WORKERS.items():
        # inactive = await gps_service.is_worker_inactive(worker_id, start, now)

        # if inactive:
        info.append(
            {
                "worker_id" : worker_id,
                "policy_id" : policy_id
            }
        )


    return await claim_service.create_claim_bulk(info, trigger_id)