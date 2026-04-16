import asyncio
from datetime import datetime, timezone, timedelta
from models import ExternalAPIResponse
from API import weather_client, aqi_client, disaster_client
from constants import EventType
from services import trigger_service

POLL_INTERVAL = 300
TRIGGER_TTL = timedelta(hours=24)

ACTIVE_TRIGGERS: dict[str, datetime] = {}

# -----------------------------
# ZONE CONFIG
# -----------------------------

ZONES = {
    "lajpat": (28.5677, 77.2431),
    "dwarka": (28.5921, 77.0460),
}

CITY_TO_ZONES = {
    "delhi": ["lajpat", "dwarka"],
    "mumbai": ["mumbai_zone_1"],  # placeholder
}

ALL_ZONES = list(ZONES.keys())


# -----------------------------
# Deduplication
# -----------------------------

def should_create_trigger(event: EventType, zone: str) -> bool:
    key = f"{event}:{zone}"
    now = datetime.now(timezone.utc)

    if key in ACTIVE_TRIGGERS:
        if now - ACTIVE_TRIGGERS[key] < TRIGGER_TTL:
            return False

    ACTIVE_TRIGGERS[key] = now
    return True


# -----------------------------
# Core processing
# -----------------------------

async def process_event(resp: ExternalAPIResponse, zone: str):
    if not resp or not resp.is_trigger:
        return

    if not should_create_trigger(resp.event_type, zone):
        return

    await trigger_service.simulate_trigger(resp.event_type, zone)


# -----------------------------
# Pollers
# -----------------------------

async def poll_weather():
    tasks = []
    zone_list = []

    for zone, (lat, lon) in ZONES.items():
        tasks.append(weather_client.get_rain_data(lat, lon))
        tasks.append(weather_client.get_heat_data(lat, lon))
        zone_list.append(zone)

    results = await asyncio.gather(*tasks, return_exceptions=True)

    idx = 0
    event_tasks = []

    for zone in zone_list:
        rain_resp = results[idx]
        heat_resp = results[idx + 1]
        idx += 2

        if not isinstance(rain_resp, Exception) and rain_resp:
            event_tasks.append(process_event(rain_resp, zone))

        if not isinstance(heat_resp, Exception) and heat_resp:
            event_tasks.append(process_event(heat_resp, zone))

    await asyncio.gather(*event_tasks, return_exceptions=True)


async def poll_aqi():
    cities = list(CITY_TO_ZONES.keys())

    results = await asyncio.gather(
        *[aqi_client.get_aqi_data(city) for city in cities],
        return_exceptions=True
    )

    event_tasks = []

    for city, resp in zip(cities, results):
        if not resp or isinstance(resp, Exception):
            continue

        zones = CITY_TO_ZONES.get(city, [])

        for zone in zones:
            event_tasks.append(process_event(resp, zone))

    await asyncio.gather(*event_tasks, return_exceptions=True)


async def poll_disasters():
    responses = await disaster_client.get_disaster_alerts()

    if not responses:
        return

    event_tasks = []

    for resp in responses:
        if not resp or not resp.is_trigger:
            continue

        # still prototype: broadcast to all zones
        for zone in ALL_ZONES:
            event_tasks.append(process_event(resp, zone))

    await asyncio.gather(*event_tasks, return_exceptions=True)


# -----------------------------
# Main Scheduler
# -----------------------------

async def run_scheduler():
    try:
        while True:
            try:
                await asyncio.gather(
                    poll_weather(),
                    poll_aqi(),
                    poll_disasters(),
                    return_exceptions=True
                )
            except Exception as e:
                print("Scheduler error:", e)

            await asyncio.sleep(POLL_INTERVAL)

    except asyncio.CancelledError:
        print("Scheduler shutting down...")