from API.base_client import BaseClient
from models import ExternalAPIResponse
from datetime import datetime, timezone
from constants import EventType

client = BaseClient()

async def get_disaster_alerts() -> list[ExternalAPIResponse]:
    url = "https://api.reliefweb.int/v1/disasters"

    data = await client.get(url)
    if not data:
        return []

    results = []

    for item in data.get("data", [])[:10]:  # limit
        fields = item.get("fields", {})

        try :
            disaster_type = EventType(fields.get("type", "disaster"))
        except :
            disaster_type = EventType.DISASTER

        results.append(
            ExternalAPIResponse(
                source="NDMA",
                city=None,
                zone=None,
                event_type=disaster_type,
                severity=1,  # no real metric
                is_trigger=True,  # assume active = trigger
                raw=item,
                fetched_at=datetime.now(timezone.utc)
            )
        )

    return results