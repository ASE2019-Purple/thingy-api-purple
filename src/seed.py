import asyncio

import db 
import mqtt 

async def main():
    await db.init_db()
    await mqtt.init_mqtt()
    values = await mqtt.subscribe(mqtt.thingys['Thingy1'], mqtt.topics['EnvironmentAll'], 10)
    # mqtt.subscribe_non_stop(mqtt.thingys['Thingy1'], mqtt.topics['EnvironmentAll']) 
    insert_bulk(values)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())

