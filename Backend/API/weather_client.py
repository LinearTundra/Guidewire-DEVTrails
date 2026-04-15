from dotenv import load_dotenv
from os import getenv
from API.base_client import BaseClient
from models import ExternalAPIResponse
from datetime import datetime, timezone
from constants import EventType

load_dotenv()
client = BaseClient()
KEY = getenv("TOMORROW_KEY")


async def get_rain_data(lat: float, lon: float) -> ExternalAPIResponse | None:

    url = (
        f"https://api.tomorrow.io/v4/weather/realtime"
        f"?location={lat},{lon}&apikey={KEY}"
    )

    data = await client.get(url)
    if not data:
        return None

    values = data["data"]["values"]

    rainfall = values.get("rainIntensity", 0)
    heat = values.get("temperatureApparent", 0)

    return ExternalAPIResponse(
        source="TOMORROW",
        city=None,
        zone=None,
        event_type=EventType.RAINFALL,
        severity=rainfall,
        is_trigger=rainfall > 50,
        raw=data,
        fetched_at=datetime.now(timezone.utc)
    )

async def get_heat_data(lat: float, lon: float) -> ExternalAPIResponse | None:

    url = (
        f"https://api.tomorrow.io/v4/weather/realtime"
        f"?location={lat},{lon}&apikey={KEY}"
    )

    data = await client.get(url)
    if not data:
        return None

    values = data["data"]["values"]

    rainfall = values.get("rainIntensity", 0)
    heat = values.get("temperatureApparent", 0)

    return ExternalAPIResponse(
        source="TOMORROW",
        city=None,
        zone=None,
        event_type=EventType.HEAT,
        severity=heat,
        is_trigger=heat > 50,
        raw=data,
        fetched_at=datetime.now(timezone.utc)
    )