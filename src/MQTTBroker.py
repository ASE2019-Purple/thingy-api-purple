import logging
import asyncio

from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1, QOS_2 #QOS_1 means from publishing client to broker, QOS_2 from broker to subscribing client

uri = 'mqtt://purple:bfe6d5288f@mqtt.thing.zone:1897'


client = None

thingys = {
    "Thingy1" : "fe:84:88:ca:47:ca/",
    "Thingy2" : "macaddress2/",
    "Thingy3" : "macaddress3/"
}

topics = {
    "Thingy1" : "fe:84:88:ca:47:ca/",
    "EnvironmentAll" : "Thingy Environment Service/#",
    "EnvironmentTemperature" : "Thingy Environment Service/Thingy Temperature Characteristic"
}


async def initMQTT():
    global client
    client = MQTTClient()
    await client.connect(uri)

@asyncio.coroutine
def subscribeToTopic(thingy, topic):
    yield from client.subscribe([
            (thingy+topic, QOS_2)
         ])
    try:
        for i in range(1, 100):
            message = yield from client.deliver_message()
            packet = message.publish_packet
            print("%d:  %s => %s" % (i, packet.variable_header.topic_name, str(packet.payload.data)))
    except ClientException as ce:
        logger.error("Client exception: %s" % ce)

async def main():
    await initMQTT()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
