import httpx

class BaseClient:
    async def get(self, url: str, headers: dict = None):
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            return response.json()