from dotenv import load_dotenv
from asyncio import run
from os import getenv
import httpx

load_dotenv()
async def test() :
    KEY = getenv("TOMORROW_KEY")
    URL = f"https://api.tomorrow.io/v4/events?insights=&buffer=1&apikey={KEY}"
    headers = {
        "Accept-Encoding": "gzip",
        "accept": "application/json"
    }
    async with httpx.AsyncClient() as client :
        response = await client.get(URL, headers=headers)
        print(response.json())

if __name__ == "__main__" :
    run(test())