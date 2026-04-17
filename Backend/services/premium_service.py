from pydantic import BaseModel
from database import plan_tiers
from services import ml_service, policy_service, worker_service, claim_service
from typing import Optional
import asyncio


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
    base_price: float


async def calculate_premium(worker_id: str) -> int:
    try :
        worker, claims, policy = await asyncio.gather(
            worker_service.worker_details(worker_id),
            claim_service.get_claims_this_week(worker_id),
            policy_service.get_last_policy(worker_id)
        )

        if not policy:
            raise ValueError("Policy not found")
        if not worker:
            raise ValueError("Worker not found")
        streak = worker.get("streak", 0)

        payload = create_payload(len(claims), worker.get("weekly_earnings", 6000))

        try :
            ml_result = await ml_service.get_risk_score(payload.model_dump())
        except Exception :
            ml_result = {}

        discount = streak // 4

        premium = ml_result.get("premium", 25)
        premium -= premium * discount / 100

        if premium < 10:
            premium = 10

        return premium

    except Exception as e :
        print("Premium Error :", e)
        return 25
    

def create_payload(claims_approved: int, weekly_earnings: float) :
    return ml_payload(
        precip_mm = 0,
        temperature_celsius = 25,
        humidity = 50,
        aqi = 100,
        hours_worked = 10,
        distance_km = 200,
        orders_completed = 20,
        avg_speed = 30,
        claims_last_week = claims_approved,
        weekly_earning = weekly_earnings,
        hours_inactive = 14
    )