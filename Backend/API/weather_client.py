from dotenv import load_dotenv
from os import getenv
from API.base_client import BaseClient
from models import ExternalAPIResponse
from datetime import datetime, timezone, timedelta
from constants import EventType
import asyncio

load_dotenv()
client = BaseClient()
KEY = getenv("TOMORROW_KEY")
CACHE: dict[tuple, dict] = {}
# key: (lat, lon)
# value: { "data": ..., "time": ..., "task": ... }

TTL = timedelta(seconds=300)


async def get_data(lat: float, lon: float) -> dict | None:
    key = (lat, lon)
    now = datetime.now(timezone.utc)

    entry = CACHE.get(key)

    # fresh cache
    if entry and (now - entry["time"] < TTL):
        return entry["data"]

    # request in progress
    if entry and entry.get("task"):
        return await entry["task"]

    # create new fetch task
    async def fetch():
        url = (
            f"https://api.tomorrow.io/v4/weather/realtime"
            f"?location={lat},{lon}&apikey={KEY}"
        )
        data = await client.get(url)

        CACHE[key] = {
            "data": data,
            "time": datetime.now(timezone.utc),
            "task": None
        }
        return data

    task = asyncio.create_task(fetch())

    CACHE[key] = {
        "data": None,
        "time": now,
        "task": task
    }

    return await task

async def get_rain_data(lat: float, lon: float) -> ExternalAPIResponse | None:
    data = await get_data(lat, lon)
    if not data:
        return None

    rainfall = data["data"]["values"].get("rainIntensity", 0)

    return ExternalAPIResponse(
        source="TOMORROW",
        event_type=EventType.RAINFALL,
        severity=rainfall,
        is_trigger=rainfall > 50,
        raw=data,
        fetched_at=datetime.now(timezone.utc)
    )


async def get_heat_data(lat: float, lon: float) -> ExternalAPIResponse | None:
    data = await get_data(lat, lon)
    if not data:
        return None

    heat = data["data"]["values"].get("temperatureApparent", 0)

    return ExternalAPIResponse(
        source="TOMORROW",
        event_type=EventType.HEAT,
        severity=heat,
        is_trigger=heat > 50,
        raw=data,
        fetched_at=datetime.now(timezone.utc)
    )