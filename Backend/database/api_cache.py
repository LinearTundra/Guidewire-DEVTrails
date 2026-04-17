from database.Database import db
from models import ExternalAPIResponse
from typing import Optional
from datetime import datetime, timezone, timedelta


async def cache_result(cache: ExternalAPIResponse) -> str:
    """
    Inserts a new API response into the cache collection.
    Called after every successful external API call —
    IMD, NDMA, AQICN, Tomorrow.io.
    
    Args:
        cache: Validated ExternalAPIResponse pydantic model instance
        
    Returns:
        Inserted document ID as string
    """
    result = await db.get_database().api_cache.insert_one(cache.model_dump())
    return str(result.inserted_id)


async def get_cached_result(source: str, zone: str, requested_date: datetime) -> Optional[dict]:
    """
    Fetches a cached API result for a specific source, zone and date.
    Check this before making any external API call.
    If result exists and is fresh, use it. If not, call the API and cache it.
    
    Args:
        source: API source name e.g. "IMD", "AQICN", "NDMA"
        zone: Zone the data is for
        requested_date: The date the data is about
        
    Returns:
        Cache document as dict or None if not found
    """
    return await db.get_database().api_cache.find_one(
        {
            "source": source,
            "zone": zone,
            "requested_date": requested_date
        }
    )


async def get_all_cached_by_date(source: str, zone: str, date: datetime) -> list[dict]:
    """
    Fetches all cached results for a source and zone on a specific date.
    Used for ML training data and historical disruption analysis.

    Args:
        source: API source name e.g. "IMD", "AQICN", "NDMA"
        zone: Zone the data is for
        date: The date the data is about
        
    Returns:
        Cache document as list of dict
    """
    start = date.replace(hour=0, minute=0, second=0, microsecond=0)
    end = date.replace(hour=23, minute=59, second=59)
    return await db.get_database().api_cache.find(
        {
            "source": source,
            "zone": zone,
            "fetched_at": {"$gte": start, "$lte": end}
        }
    ).sort("fetched_at", 1).to_list(length=None)


async def is_cache_fresh(source: str, zone: str, requested_date: datetime, max_age_minutes: int = 60) -> bool:
    """
    Checks if a cached result exists and is within the acceptable age.
    Use this before deciding whether to call the external API or use cache.
    Default max age is 60 minutes — APIs are polled hourly.
    
    Args:
        source: API source name
        zone: Zone the data is for
        requested_date: The date the data is about
        max_age_minutes: Maximum acceptable cache age in minutes, default 60
        
    Returns:
        True if cache exists and is fresh, False if stale or not found
    """
    cache = await get_cached_result(source, zone, requested_date)
    if not cache:
        return False
    age = datetime.now(timezone.utc) - cache["fetched_at"].replace(tzinfo=timezone.utc)
    return age < timedelta(minutes=max_age_minutes)


async def get_latest_cached_result(source: str, zone: str) -> Optional[dict]:
    """
    Fetches the most recently cached result for a source and zone
    regardless of requested_date.
    Used when you need the latest available data without caring about
    a specific date — e.g. current AQI or current weather conditions.
    
    Args:
        source: API source name
        zone: Zone the data is for
        
    Returns:
        Most recent cache document as dict or None if not found
    """
    return await db.get_database().api_cache.find_one(
        {"source": source, "zone": zone},
        sort=[("fetched_at", -1)]
    )


async def delete_stale_cache(max_age_hours: int = 24) -> int:
    """
    Deletes all cache entries older than max_age_hours.
    Call periodically to keep the collection size manageable.
    Default clears anything older than 24 hours.
    
    Args:
        max_age_hours: Age threshold in hours, default 24
        
    Returns:
        Number of deleted documents
    """
    cutoff = datetime.now(timezone.utc) - timedelta(hours=max_age_hours)
    result = await db.get_database().api_cache.delete_many({
        "fetched_at": {"$lt": cutoff}
    })
    return result.deleted_count