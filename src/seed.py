import asyncio

from db import init_db, insert_bulk
from mqtt import init_mqtt, subscribe, thingys, topics

async def main():
    await init_db()
    await init_mqtt()
    values = await subscribe(thingys['Thingy1'], topics['EnvironmentAll'])
    insert_bulk(values)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())

