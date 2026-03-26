from fastapi import APIRouter, HTTPException
from typing import Optional, List
from constants import ClaimStatus
from pydantic import BaseModel
from models import ApiResponse
from database import claims


"""
Error Codes:
    400 → Bad request (invalid input)
    401 → Not logged in / invalid token
    403 → Logged in but not allowed
    404 → Not found
    409 → Conflict (duplicate mobile, etc.)
    422 → Validation error (FastAPI auto uses this)
"""

class ClaimRequest(BaseModel) :
    worker_id: str
    status: Optional[List[ClaimStatus]] = None

router = APIRouter(prefix="/claims")

@router.post(
    "/get-all-claims",
    summary="Fetch all claims registered to a worker",
    description="worker_id: uid of the worker<br>status: array of claim status to filter, leave empty id need all claims",
    response_model=ApiResponse
)
async def get_claims(data: ClaimRequest) :
    result = await claims.get_claims_by_worker(data.worker_id, data.status)
    return ApiResponse(success=True, data=result)

@router.post(
    "/get-last-claim",
    summary="Fetch the last claim registered to a worker",
    description="worker_id: uid of the worker<br>status: array of claim status to filter, leave empty id need all claims",
    response_model=ApiResponse
)
async def get_last_claim(data: ClaimRequest) :
    result = await claims.get_last_claim_by_worker(data.worker_id, data.status)
    return ApiResponse(success=True, data=result)
