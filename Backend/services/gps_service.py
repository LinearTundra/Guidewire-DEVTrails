from datetime import datetime
from database import gps_logs


# threshold can be tuned later
MIN_LOG_COUNT = 10


async def is_worker_inactive(worker_id: str, start: datetime, end: datetime) -> bool:
    """
    Checks if worker was inactive in a given time window.
    
    Logic:
        Fetch logs in window
        If logs < threshold → inactive

    Args:
        worker_id: unique identifier of the worker
        start: start datetime of the claim process
        end: end datetime of the claim process
    
    Returns:
        True if no of logs < minimum log count

    """
    logs = await gps_logs.get_logs_in_window(worker_id, start, end)
    return len(logs) < MIN_LOG_COUNT