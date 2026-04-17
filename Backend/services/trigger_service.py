from datetime import datetime, timezone, timedelta
from services import claim_service, worker_service
from constants import EventType, Severity
from database import trigger_events
from models import TriggerEvents
import asyncio



def make_trigger_object(event_type: EventType, zone: str, source: str="Mocked") :
    return TriggerEvents(
        event_type=event_type,
        source=source,  
        state="Delhi",
        city="Delhi",
        zone=zone,
        threshold_value="50",
        severity=Severity.RED,
        start_time=datetime.now(timezone.utc),
        is_active=True,
        affected_workers=[]
    )


async def create_trigger(event: TriggerEvents) :
    return await trigger_events.create_trigger_event(event)

async def simulate_trigger(event: EventType, zone: str="Dwarka") -> int:
    """
    Simulates a disruption event.
    
    Flow:
    - define time window
    - check inactivity
    - create claims
    """
    # now = datetime.utcnow()
    # start = now - timedelta(hours=2)
    trigger_event = make_trigger_object(event, zone)
    print("Trigger object created.")
    
    trigger_id, affected_workers = await asyncio.gather(
        create_trigger(trigger_event),
        worker_service.get_workers_covered_from_trigger(trigger_event)
    )
    info = []
    print("Trigger stored.\nWorkers fetched.")

    for worker_id, policy_id in affected_workers.items():
        # inactive = await gps_service.is_worker_inactive(worker_id, start, now)

        # if inactive:
        info.append(
            {
                "worker_id" : worker_id,
                "policy_id" : policy_id
            }
        )
    print("Creating claims")
    await claim_service.create_claim_bulk(info, trigger_id, event)
    return trigger_id

async def resolve_trigger(trigger_id: str) :
    return await trigger_events.deactivate_event(trigger_id)

async def end_trigger(trigger_id: str):
    """
    Ends a trigger:
    1. mark trigger inactive
    2. remove trigger from all claims
    3. stop monitoring where no triggers left
    4. resolve claims based on GPS result
    """

    # 1. deactivate trigger
    await resolve_trigger(trigger_id)
    print("Resolved trigger event")

    # 2. remove trigger from all running claims
    await claim_service.resolve_trigger_in_claims(trigger_id)

    # 3 & 4. stop + resolve eligible claims
    return await claim_service.close_resolved_claims()

async def recover_triggers(TRIGGER_TTL: timedelta):
    print("Recovering Triggers.")
    active_triggers = await trigger_events.get_active_events()

    now = datetime.now(timezone.utc)

    for trig in active_triggers:
        trigger_id = str(trig["_id"])
        created_at = trig["created_at"]
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)
        try :
            if now - created_at > TRIGGER_TTL:
                await end_trigger(trigger_id)
        except Exception as e :
            print("Error closing trigger", trigger_id, f"\n{e}")
    
    print("Closing Resolved Claims.")
    await claim_service.close_resolved_claims()

async def trigger_event_details(event_id: str) :
    return await trigger_events.get_trigger_event(str(event_id))