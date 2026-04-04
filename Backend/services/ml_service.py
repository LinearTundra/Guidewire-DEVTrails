import httpx

ML_API_URL = "https://gigshield-ml-api.onrender.com/predict"  # replace

async def get_risk_score(payload: dict) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(ML_API_URL, json=payload)
        return response.json()