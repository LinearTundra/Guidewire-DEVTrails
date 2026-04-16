from fastapi import APIRouter, HTTPException
from models import ApiResponse, GpsLogs
from services import gps_service

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


router = APIRouter(prefix="/gps")

@router.post(
    "/post-location",
    response_model=ApiResponse,
    summary="Upload location",
    responses={
        500 : {"description":"Failed to insert gps log"}
    }
)
async def insert_location(data: GpsLogs) :
    try :
        await gps_service.insert_log(data)
        return ApiResponse(success=True)
    except :
        raise HTTPException(status_code=500, detail="Failed to insert gps log")

@router.post(
    "/post-location-many",
    response_model=ApiResponse,
    summary="Upload multiple locations",
    description=(
        "Upload multiple locations at once. "
        "Store logs locally (e.g., 1 hour) and send in batch."
    ),
    responses={
        400 : {"description":"Empty GPS log list"},
        500 : {"description":"Failed to insert gps log"}
    }
)
async def insert_location_many(data: list[GpsLogs]) :
    if not data :
        raise HTTPException(status_code=400, detail="Empty GPS log list")
    try :
        await gps_service.insert_log_multiple(data)
        return ApiResponse(success=True)
    except Exception :
        raise HTTPException(status_code=500, detail="Failed to insert gps log")