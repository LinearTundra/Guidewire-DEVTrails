import httpx

class BaseClient :
    async def get(self, url: str, headers: dict = None) :
        async with httpx.AsyncClient(timeout=10) as client :
            try :
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                return response.json()
            except Exception as e :
                print(f"API error: {e}")
                return None