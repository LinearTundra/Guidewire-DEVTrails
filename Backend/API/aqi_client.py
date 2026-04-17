from API.base_client import BaseClient
from models import ExternalAPIResponse
from datetime import datetime, timezone
from constants import EventType
from dotenv import load_dotenv
from os import getenv

load_dotenv
TOKEN = getenv("WAQI_TOKEN")
client = BaseClient()

async def get_aqi_data(city: str) -> ExternalAPIResponse | None:
    url = f"https://api.waqi.info/feed/{city}/?token={TOKEN}"

    data = await client.get(url)
    if not data or data.get("status") != "ok":
        return None

    aqi = data["data"]["aqi"]

    return ExternalAPIResponse(
        source="AQICN",
        city=city,
        zone=None,
        event_type=EventType.AQI,
        severity=aqi,
        is_trigger=aqi > 300,  # your rule
        raw=data,
        fetched_at=datetime.now(timezone.utc)
    )

if __name__ == "__main__" :
    pass