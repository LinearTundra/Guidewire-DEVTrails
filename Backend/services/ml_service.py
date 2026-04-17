import httpx
import asyncio

ML_API_URL = "https://gigshield-ml-api.onrender.com/predict"

async def get_risk_score(payload: dict) -> dict | None:
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(ML_API_URL, json=payload)

        if response.status_code != 200:
            return None

        data = response.json()

        # basic sanity check
        if "risk_score" not in data:
            return None

        return data

    except (httpx.RequestError, asyncio.TimeoutError):
        return None