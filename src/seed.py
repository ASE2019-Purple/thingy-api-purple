import asyncio

import influx 
import mqtt 

async def main():
    await influx.init_db()
    await mqtt.init_mqtt()
    # values = await mqtt.subscribe(mqtt.thingys['Thingy1'], mqtt.topics['EnvironmentAll'], 10)
    await mqtt.subscribe_non_stop(mqtt.thingys['Thingy1'], mqtt.topics['EnvironmentAll']) 
    # influx.insert_bulk(values)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())

