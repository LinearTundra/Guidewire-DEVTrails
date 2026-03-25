from fastapi import APIRouter, HTTPException
from database import workers

router = APIRouter(prefix="/worker")

@router.get("/get-worker-details")
async def get_worker_id(worker_id: str) :
    try :
        result = await workers.get_worker(worker_id)
        if result == None :
            raise HTTPException(status_code=402, detail="Invalid worker_id")
        if "_id" in result :
            result["_id"] = str(result["_id"])
        return result
    except Exception as e :
        return {"error" : e}
