from Backend.API.base_client import BaseClient

client = BaseClient()

async def get_aqi_data(city: str):
    url = f"https://api.waqi.info/feed/{city}/?token=demo"

    return await client.get(url)