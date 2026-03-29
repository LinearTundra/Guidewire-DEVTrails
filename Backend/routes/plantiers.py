from database import plan_tiers
from models import ApiResponse
from fastapi import APIRouter
from constants import Plan


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


router = APIRouter(prefix="/plan-tiers")

@router.get(
    "/details",
    summary="Get details of a plan tier",
    response_model=ApiResponse
)
async def plan_details(plan: Plan) :
    result = await plan_tiers.get_plan_tier(plan)
    if result is None :
        return ApiResponse(success=False)
    return ApiResponse(success=True, data=result)

@router.get(
    "/all",
    summary="Get list of all plan tier available",
    response_model=ApiResponse
)
async def plan_details() :
    result = await plan_tiers.get_all_plan_tiers()
    return ApiResponse(success=True, data=result)
