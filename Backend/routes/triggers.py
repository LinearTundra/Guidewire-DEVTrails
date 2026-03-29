from fastapi import APIRouter
from models import ApiResponse
from constants import EventType


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
    summary="Simulate an event",
    response_model=ApiResponse
)
async def simulate_trigger(event: EventType) :
    # Add trigger event services
    pass
