from fastapi import APIRouter
from models import ApiResponse
from constants import EventType
from services import trigger_service
from asyncio import sleep, create_task


"""
Error Codes:
    400 → Bad request (invalid input/format)
    401 → Not logged in / invalid token
    403 → Logged in but not allowed
    404 → Not found
    409 → Conflict (duplicate mobile, etc.)
    422 → Validation error (FastAPI auto uses this)
    500 → DB Failure
"""


router = APIRouter(prefix="/trigger")

@router.get(
    "/simulate",
    summary="Simulate an event for certain peroid of time",
    response_model=ApiResponse
)
async def simulate_trigger(event: EventType, zone: str, time: float=20) :
    create_task(runSequence(event, zone, time))
    return ApiResponse(success=True, data="Event Simulated")

async def runSequence(event: EventType, zone: str, time: float) :
    trigger_id = await trigger_service.simulate_trigger(event, zone)
    await sleep(time)
    await trigger_service.end_trigger(trigger_id)