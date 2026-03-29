from fastapi import APIRouter, HTTPException
from models import ApiResponse
from database import policies


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


router = APIRouter(prefix="/premium")

@router.get(
    "/calculate",
    summary="Calculate the upcoming week's premium",
    response_model=ApiResponse
)
async def calculate_premium(worker_id: str):
    try:
        result = await policies.get_active_policy(worker_id)

        if not result or "weekly_premium" not in result:
            return ApiResponse(success=True, data={"premium": 25})

        return ApiResponse(success=True, data={"premium": result["weekly_premium"]})

    except Exception:
        raise HTTPException(status_code=500, detail="Failed to calculate premium")