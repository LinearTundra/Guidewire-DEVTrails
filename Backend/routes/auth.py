from fastapi import APIRouter, HTTPException
from database import auth, workers
from models import Worker, Auth
from pydantic import BaseModel


class LoginData(BaseModel) :
    mobile: str
    password: str

class RegisterData(BaseModel) :
    worker: Worker
    password: str

router = APIRouter(prefix="/auth")

@router.post("/login")
async def login(login: LoginData) :
    try :
        return await auth.login(login.mobile, login.password)
    except auth.AuthError as e :
        raise HTTPException(status_code=404, detail=e.message)
    except Exception as e :
        return {"error" : e}

# TODO: OTP verification
@router.post("/register")
async def register(data: RegisterData):
    if type(data.worker) != Worker :
        raise HTTPException(status_code=401, detail="Missing fields")

    worker_id = await workers.create_worker(data.worker)
    if worker_id == None :
        raise HTTPException(status_code=401, detail="Invalid mobile")
    user_auth = Auth(
        worker_id = worker_id,
        mobile = data.worker.mobile,
        email = data.worker.email,
        password = data.password
    )
    auth_id = await auth.create_auth(user_auth)
    if auth_id == None :
        workers.delete_worker(worker_id)
        raise HTTPException(status_code=401, detail="Error creating worker, try again")

    return {"worker_id": worker_id}
    

# TODO: OTP verification
@router.post("/reset-password")
async def reset_password(data: LoginData) :
    try :
        result = await auth.update_password(data.mobile, data.new_password)
        return {"result" : result}
    except Exception as e :
        return {"error" : e}