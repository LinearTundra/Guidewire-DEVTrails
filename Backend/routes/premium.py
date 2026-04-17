from fastapi import APIRouter, HTTPException
from models import ApiResponse
from database import policies
from pydantic import BaseModel
from services import ml_service, premium_service
from typing import Optional


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


class ml_payload(BaseModel) :
    precip_mm: Optional[float] = 0
    temperature_celsius: Optional[float] = 25
    humidity: Optional[float] = 50
    aqi: Optional[float] = 100
    hours_worked: Optional[float] = 10
    distance_km: Optional[float] = 200
    orders_completed: Optional[float] = 20
    avg_speed: Optional[float] = 30
    claims_last_week: Optional[float] = 0
    weekly_earning: Optional[float] = 6000
    hours_inactive: Optional[float] = 14


router = APIRouter(prefix="/premium")

@router.get(
    "/calculate",
    summary="Calculate the upcoming week's premium",
    response_model=ApiResponse,
    responses={
        400 : {"description":"Failed to calculate premium"}
    }
)
async def calculate_premium(worker_id: str):
    try:
        premium = premium_service.calculate_premium(worker_id)

        return ApiResponse(success=True, data={"premium": premium})

    except Exception:
        raise HTTPException(status_code=400, detail="Failed to calculate premium")



@router.post(
    "/calculate/mocked",
    summary="Calculate the upcoming week's premium with mocked weather and user data",
    response_model=ApiResponse,
    responses={
        400 : {"description":"Failed to calculate premium"}
    }
)
async def calculate_premium_mocked(worker_id: str, payload: ml_payload, streak: Optional[int]=None):
    try:
        result = await policies.get_active_policy(worker_id) or {}

        if not result:
            raise HTTPException(status_code=400, detail="Failed to calculate premium")

        try:
            ml_result = await ml_service.get_risk_score(payload.model_dump())
        except Exception:
            ml_result = {}

        discount = result.get("streak", 0) // 4
        if streak is not None:
            discount = streak // 4

        premium = ml_result.get("premium", 25)
        premium -= premium * discount / 100

        if premium < 10:
            premium = 10

        return ApiResponse(success=True, data={"premium": premium})

    except Exception:
        raise HTTPException(status_code=400, detail="Failed to calculate premium")