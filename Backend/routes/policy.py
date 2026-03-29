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


router = APIRouter(prefix="/policy")

@router.get(
    "/current",
    summary="Get worker's current active policy",
    response_model=ApiResponse
)
async def current_active_policy(worker_id: str) :
    result = await policies.get_active_policy(worker_id)
    if result is None :
        return ApiResponse(success=False)
    return ApiResponse(success=True, data=result)

@router.get(
    "/all",
    summary="Get all of the worker's policies, active and past ones",
    response_model=ApiResponse
)
async def all_policies(worker_id: str) :
    result = await policies.get_policies_by_worker(worker_id)
    return ApiResponse(success=True, data=result)

