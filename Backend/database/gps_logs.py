from database.Database import db
from models import GpsLogs
from datetime import datetime


async def log_gps(gps_log: GpsLogs) -> str:
    """
    Inserts a single GPS reading for a worker.
    Called by the mobile app background service every few minutes.
    High volume collection — one document per reading per active worker.
    
    Args:
        gps_log: Validated GpsLogs pydantic model instance
        
    Returns:
        Inserted document ID as string
    """
    result = await db.get_database().gps_logs.insert_one(gps_log.model_dump())
    return str(result.inserted_id)


async def log_gps_many(gps_logs: list[GpsLogs]) -> int:
    """
    Batch inserts multiple GPS readings at once.
    More efficient than log_gps() when syncing buffered readings
    after the device reconnects.
    
    Args:
        gps_logs: List of validated GpsLogs pydantic model instances
        
    Returns:
        Number of inserted documents
    """
    result = await db.get_database().gps_logs.insert_many(
        [log.model_dump() for log in gps_logs]
    )
    return len(result.inserted_ids)


async def get_logs_by_worker(worker_id: str) -> list[dict]:
    """
    Fetches all GPS logs for a worker.
    Used for heatmap generation of worker's operating zones.
    
    Args:
        worker_id: MongoDB ObjectId string
        
    Returns:
        List of GPS log documents ordered by timestamp ascending
    """
    return await db.get_database().gps_logs.find(
        {"worker_id": worker_id}
    ).sort("timestamp", 1).to_list(length=None)


async def get_logs_in_window(worker_id: str, start: datetime, end: datetime) -> list[dict]:
    """
    Fetches GPS logs for a worker within a specific time window.
    Core function for fraud detection — used to verify GPS inactivity
    during a trigger event window.
    
    Args:
        worker_id: MongoDB ObjectId string
        start: Window start datetime in UTC
        end: Window end datetime in UTC
        
    Returns:
        List of GPS log documents within the time window
    """
    return await db.get_database().gps_logs.find(
        {
            "worker_id": worker_id,
            "timestamp": {
                "$gte": start,
                "$lte": end
            }
        }
    ).sort("timestamp", 1).to_list(length=None)


async def get_mocked_logs_in_window(worker_id: str, start: datetime, end: datetime) -> list[dict]:
    """
    Fetches GPS logs flagged as mocked for a worker within a time window.
    Used by fraud detection to check if mock location was active
    during the claim window.
    
    Args:
        worker_id: MongoDB ObjectId string
        start: Window start datetime in UTC
        end: Window end datetime in UTC
        
    Returns:
        List of mocked GPS log documents within the time window
    """
    return await db.get_database().gps_logs.find(
        {
            "worker_id": worker_id,
            "is_mocked": True,
            "timestamp": {
                "$gte": start,  # $gte = >=
                "$lte": end     # $lte = <=
            }
        }
    ).sort("timestamp", 1).to_list(length=None)


async def count_logs_in_window(worker_id: str, start: datetime, end: datetime) -> int:
    """
    Fetches the number of GPS logs of a worker within a time window.
    
    Args:
        worker_id: MongoDB ObjectId string
        start: Window start datetime in UTC
        end: Window end datetime in UTC
        
    Returns:
        Number of documents
    """
    return await db.get_database().gps_logs.count_documents(
        {
            "worker_id": worker_id,
            "timestamp": {
                "$gte": start,
                "$lte": end
            }
        }
    )

async def get_last_log(worker_id: str) -> dict | None:
    '''
    Fetches the last entered GPS log of a worker.
    
    Args:
        worker_id: MongoDB ObjectId string
        
    Returns:
        Last entered log or None
    '''
    return await db.get_database().gps_logs.find_one(
        {"worker_id" : worker_id},
        sort = [("timestamp", -1)]
    )