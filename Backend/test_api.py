import asyncio
from API.weather_client import get_weather_data

async def main():
    data = await get_weather_data()
    print(data)

asyncio.run(main())