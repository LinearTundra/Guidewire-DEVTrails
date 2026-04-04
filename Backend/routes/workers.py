from fastapi import APIRouter, HTTPException
from models import ApiResponse
from database import workers
from bson import ObjectId


"""
Error Codes:
    400 → Bad request (invalid input/format)
    401 → Not logged in / invalid token
    403 → Logged in but not allowed
    404 → Not found
    409 → Conflict (duplicate mobile, etc.)
    422 → Validation error (FastAPI auto uses this)
"""


router = APIRouter(prefix="/worker")

@router.get(
    "/get-worker-details",
    responses={
        400 : {"description":"Invalid worker_id"}
    },
    response_model=ApiResponse,
    summary="Get worker details"
)
async def get_worker_details(worker_id: str) :
    try :
        ObjectId(worker_id)
    except Exception as e :
        raise HTTPException(status_code=400, detail="Invalid worker_id")
    result = await workers.get_worker(worker_id)
    if result == None :
        raise HTTPException(status_code=400, detail="Invalid worker_id")
    if "_id" in result :
        result["_id"] = str(result["_id"])
    return ApiResponse(success=True, data=result)
