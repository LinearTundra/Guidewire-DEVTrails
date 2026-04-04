from dotenv import load_dotenv
from os import getenv
from API.base_client import BaseClient

load_dotenv()

client = BaseClient()

async def get_weather_data():
    key = getenv("TOMORROW_KEY")
    url = f"https://api.tomorrow.io/v4/events?apikey={key}"

    return await client.get(url)