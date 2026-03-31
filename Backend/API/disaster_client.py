from Backend.API.base_client import BaseClient

client = BaseClient()

async def get_disaster_alerts():
    url = "https://api.reliefweb.int/v1/disasters"

    return await client.get(url)