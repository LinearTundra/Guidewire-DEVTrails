from datetime import datetime, timezone
from database import gps_logs
from models import GpsLogs
import asyncio
import math

MONITERED_WORKERS = {}

async def insert_log(log: GpsLogs) :
    result = await gps_logs.log_gps(log)
    if log.worker_id in MONITERED_WORKERS :
        MONITERED_WORKERS[log.worker_id]["update available"] = True
    return result

async def insert_log_multiple(logs: list[GpsLogs]) :
    inserted = await gps_logs.log_gps_many(logs)
    log = logs[0]
    if log.worker_id in MONITERED_WORKERS :
        MONITERED_WORKERS[log.worker_id]["update available"] = True
    return inserted

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # meters

    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def compute_total_distance(logs):
    if len(logs) < 2:
        return 0

    distance = 0

    for i in range(1, len(logs)):
        lon1, lat1 = logs[i-1]["location"]["coordinates"]
        lon2, lat2 = logs[i]["location"]["coordinates"]

        distance += haversine(lat1, lon1, lat2, lon2)

    return distance

def get_minmax_coordinate(logs):
    if not logs:
        return None, None

    lats = []
    lons = []

    for p in logs:
        lon, lat = p["location"]["coordinates"]
        lats.append(lat)
        lons.append(lon)

    return (min(lats), min(lons)), (max(lats), max(lons))


def compute_area(min_coordinate, max_coordinate):
    min_lat, min_lon = min_coordinate
    max_lat, max_lon = max_coordinate
    lat_dist = haversine(min_lat, min_lon, max_lat, min_lon)
    lon_dist = haversine(min_lat, min_lon, min_lat, max_lon)

    return lat_dist * lon_dist

async def get_logs_after(worker_id: str, start_time: datetime) :
    return await gps_logs.get_logs_in_window(worker_id, start_time, datetime.now(timezone.utc))

async def get_all_logs(worker_id: str) :
    return await gps_logs.get_logs_by_worker(worker_id)

async def get_last_log(worker_id: str) :
    return await gps_logs.get_last_log(worker_id)

def store_monitored_workers(worker_id: str) :
    if worker_id in MONITERED_WORKERS :
        return
    MONITERED_WORKERS[worker_id] = {"update available" : False}

def remove_monitored_workers(worker_id: str) :
    MONITERED_WORKERS.pop(worker_id)

async def monitor_worker_movement(worker_id: str, claim_id: str, start_time: datetime) -> dict:
    store_monitored_workers(worker_id)

    min_coords = None
    max_coords = None
    distance = 0

    fraud_checks = {
        "high_distance": False,
        "large_area": False,
        "no_movement": True
    }

    try:
        last_time = start_time

        while True:
            worker_meta = MONITERED_WORKERS.get(worker_id)

            if worker_meta is None:
                break

            await asyncio.sleep(5)

            if not worker_meta["update available"]:
                continue

            logs = await get_logs_after(worker_id, last_time)

            if logs:
                fraud_checks["no_movement"] = False

                distance += compute_total_distance(logs)

                mn, mx = get_minmax_coordinate(logs)

                if mn and mx:
                    if min_coords is None:
                        min_coords = list(mn)
                        max_coords = list(mx)
                    else:
                        min_coords[0] = min(min_coords[0], mn[0])
                        min_coords[1] = min(min_coords[1], mn[1])
                        max_coords[0] = max(max_coords[0], mx[0])
                        max_coords[1] = max(max_coords[1], mx[1])

                last_time = logs[-1]["timestamp"]

            worker_meta["update available"] = False

    except asyncio.CancelledError:
        remove_monitored_workers(worker_id)

        # ---- compute area safely ----
        area = 0
        if min_coords and max_coords:
            area = compute_area(min_coords, max_coords)

        # ---- fraud signals ----
        if distance > 1000:
            fraud_checks["high_distance"] = True

        if area > 5000:
            fraud_checks["large_area"] = True

        # ---- final classification ----
        if fraud_checks["high_distance"] or fraud_checks["large_area"]:
            status = "fraud"
        elif distance > 500 or area > 1000:
            status = "suspicious"
        else:
            status = "clean"

        return {
            "worker_id": worker_id,
            "claim_id": claim_id,
            "distance": distance,
            "area": area,
            "status": status,
            "fraud_checks": fraud_checks
        }