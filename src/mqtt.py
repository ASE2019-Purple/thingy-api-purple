import logging
import asyncio

from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1, \
    QOS_2  # QOS_1 means from publishing client to broker, QOS_2 from broker to subscribing client

uri = 'mqtt://purple:bfe6d5288f@mqtt.thing.zone:1897'

client = None

thingys = {
    "Thingy1": "fe:84:88:ca:47:ca/",
    "Thingy2": "macaddress2/",
    "Thingy3": "macaddress3/"
}

topics = {
    "Thingy1": "fe:84:88:ca:47:ca/",
    "EnvironmentAll": "Thingy Environment Service/#",
    "EnvironmentTemperature": "Thingy Environment Service/Thingy Temperature Characteristic"

    # TODO: Add all the other services (can be found in config.json)
}


async def init_mqtt():
    global client
    client = MQTTClient()
    await client.connect(uri)

@asyncio.coroutine
def subscribe(thingy, topic):
    values = []
    yield from client.subscribe([
        (thingy + topic, QOS_2)
    ])
    try:
        for i in range(1, 1000):
            message = yield from client.deliver_message()
            packet = message.publish_packet
            values.append(packet.variable_header.topic_name + "://:" + packet.payload.data.decode())
        print(values)
    except ClientException as ce:
        logger.error("Client exception: %s" % ce)

    return values