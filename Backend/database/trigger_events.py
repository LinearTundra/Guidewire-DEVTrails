from database.Database import db
from models import TriggerEvents
from constants import EventType
from typing import Optional
from bson import ObjectId
from datetime import datetime, timezone


async def create_trigger_event(event: TriggerEvents) -> str:
    """
    Inserts a new trigger event document into the trigger_events collection.
    Called automatically when an external API threshold is crossed.
    
    Args:
        event: Validated TriggerEvents pydantic model instance
        
    Returns:
        Inserted document ID as string
    """
    result = await db.get_database().trigger_events.insert_one(event.model_dump())
    return str(result.inserted_id)


async def get_trigger_event(event_id: str) -> Optional[dict]:
    """
    Fetches a single trigger event by its MongoDB ObjectId.
    
    Args:
        event_id: MongoDB ObjectId string
        
    Returns:
        Trigger event document as dict or None if not found
    """
    return await db.get_database().trigger_events.find_one({"_id": ObjectId(event_id)})


async def get_active_events() -> list[dict]:
    """
    Fetches all currently active trigger events across all zones.
    Used by admin dashboard live disruption map.
    
    Returns:
        List of active trigger event documents
    """
    return await db.get_database().trigger_events.find(
        {"is_active": True}
    ).sort("created_at", -1).to_list(length=None)


async def get_active_events_by_zone(zone: str) -> list[dict]:
    """
    Fetches all active trigger events in a specific zone.
    Used by trigger monitoring loop to check if a worker's zone
    has an active disruption before initiating claims.
    
    Args:
        zone: Zone name e.g. "Lajpat Nagar"
        
    Returns:
        List of active trigger event documents for that zone
    """
    return await db.get_database().trigger_events.find(
        {"zone": zone, "is_active": True}
    ).sort("created_at", -1).to_list(length=None)


async def get_events_by_type(event_type: EventType) -> list[dict]:
    """
    Fetches all trigger events of a specific type — active and historical.
    Used for historical disruption analysis and zone risk scoring.
    
    Args:
        event_type: EventType enum value
        
    Returns:
        List of trigger event documents of that type
    """
    return await db.get_database().trigger_events.find(
        {"event_type": event_type.value}
    ).sort("created_at", -1).to_list(length=None)


async def get_events_by_zone(zone: str) -> list[dict]:
    """
    Fetches all trigger events for a zone — active and historical.
    Used for zone risk scoring and premium calculation.
    
    Args:
        zone: Zone name e.g. "Lajpat Nagar"
        
    Returns:
        List of all trigger event documents for that zone
    """
    return await db.get_database().trigger_events.find(
        {"zone": zone}
    ).sort("created_at", -1).to_list(length=None)


async def add_affected_worker(event_id: str, worker_id: str) -> bool:
    """
    Appends a worker_id to the affected_workers list on a trigger event.
    Called when zone matching identifies a worker in the affected zone.
    Uses $addToSet to prevent duplicate entries.
    
    Args:
        event_id: MongoDB ObjectId string of the trigger event
        worker_id: MongoDB ObjectId string of the affected worker
        
    Returns:
        True if update was successful, False if event not found
    """
    result = await db.get_database().trigger_events.update_one(
        {"_id": ObjectId(event_id)},
        {"$addToSet": {"affected_workers": worker_id}}
    )
    return result.modified_count > 0


async def deactivate_event(event_id: str) -> bool:
    """
    Marks a trigger event as inactive and sets its end time.
    Called when the external API reports the disruption has ended.
    
    Args:
        event_id: MongoDB ObjectId string
        
    Returns:
        True if update was successful, False if event not found
    """
    result = await db.get_database().trigger_events.update_one(
        {"_id": ObjectId(event_id)},
        {
            "$set": {
                "is_active": False,
                "end_time": datetime.now(timezone.utc)
            }
        }
    )
    return result.modified_count > 0