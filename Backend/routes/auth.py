from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, HTTPException
from models import Worker, Auth, ApiResponse, Policies
from constants import Plan
from services import policy_service
from database import auth, workers
from pydantic import BaseModel
import asyncio


"""
Error Codes:
    400 → Bad request (invalid input)
    401 → Not logged in / invalid token
    403 → Logged in but not allowed
    404 → Not found
    409 → Conflict (duplicate mobile, etc.)
    422 → Validation error (FastAPI auto uses this)
"""


class LoginData(BaseModel) :
    mobile: str
    password: str

class RegisterData(BaseModel) :
    worker: Worker
    password: str

router = APIRouter(prefix="/auth")

@router.post(
    "/login",
    summary="User login",
    response_model=ApiResponse,
    responses={
        400 : {"description":"Bad Request"},
        401 : {"description":"Invalid Credentials"}
    }
)
async def login(login: LoginData) :
    try :
        result = await auth.login(login.mobile, login.password)
        return ApiResponse(success=True, data=result)
    except auth.AuthError :
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    except Exception as e :
        raise HTTPException(status_code=400, detail=e)

# TODO: OTP verification
@router.post(
    "/register",
    summary="Create new user",
    response_model=ApiResponse,
    responses={
        400 : {"description":"Error creating worker, try again"},
        401 : {"description":"Invalid Credentials"}
    }
)
async def register(data: RegisterData) :
    worker_id = await workers.create_worker(data.worker)
    if worker_id == None :
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    user_auth = Auth(
        worker_id = worker_id,
        mobile = data.worker.mobile,
        email = data.worker.email,
        password = data.password
    )
    policy = create_policy_object(worker_id)
    auth_id, policy_id = await asyncio.gather(
        auth.create_auth(user_auth),
        policy_service.insert_policy(policy)
    ) 
    if auth_id == None :
        workers.delete_worker(worker_id)
        raise HTTPException(status_code=400, detail="Error creating worker, try again")

    return ApiResponse(success=True, data={"worker_id": worker_id})
    

# TODO: OTP verification
@router.post(
    "/reset-password",
    summary="Reset user password",
    response_model=ApiResponse
)
async def reset_password(data: LoginData) :
    result = await auth.update_password(data.mobile, data.new_password)
    return ApiResponse(success=result)

def create_policy_object(worker_id: str) :
    today = datetime.now(timezone.utc)
    today.replace(hour=0, minute=0, second=0, microsecond=0)
    return Policies(
        worker_id = worker_id, 
        plan = Plan.STANDARD,
        weekly_premium = 38,
        max_payout = 1200,
        current_payout = 0,
        start_date = today,
        end_date = today+timedelta(days=6, hours=23, minutes=59, seconds=59),
        is_active = True,
        waiting_period_complete = True,
        streak_week = 2
    )