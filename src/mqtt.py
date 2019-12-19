import logging
import asyncio
import time
import os

from influx import insert_bulk, insert_environment_data
from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1, \
    QOS_2  # QOS_1 means from publishing client to broker, QOS_2 from broker to subscribing client

MQTT_HOST=os.getenv("MQTT_HOST")
MQTT_PORT=os.getenv("MQTT_PORT")
MQTT_USERNAME=os.getenv("MQTT_USERNAME")
MQTT_PASSWORD=os.getenv("MQTT_PASSWORD")

client = None

thingys = {
    "Thingy1": "fe:84:88:ca:47:ca/",
    "Thingy2": "fe:0f:3c:ed:a3:d6/",
    "Thingy3": "e6:97:3d:de:ca:a3/"
}

topics = {
    "EnvironmentAll": "Thingy Environment Service/#",
    "EnvironmentTemperature": "Thingy Environment Service/Thingy Temperature Characteristic"

    # TODO: Add all the other services (can be found in config.json)
}


async def init_mqtt():
    global client
    client = MQTTClient()
    uri = 'mqtt://' + MQTT_USERNAME + ':' + MQTT_PASSWORD + '@' +MQTT_HOST + ':' + MQTT_PORT
    await client.connect(uri)

async def init_local_mqtt():
    global client
    client = MQTTClient()
    uri_local = 'mqtt://purple:bfe6d5288f@mqtt.thing.zone:1897'
    await client.connect(uri_local)


@asyncio.coroutine
def subscribe(thingy, topic, range):
    values = []
    yield from client.subscribe([
        (thingy + topic, QOS_2)
    ])
    try:
        for i in range(1, range):
            message = yield from client.deliver_message()
            packet = message.publish_packet
            values.append(packet.variable_header.topic_name + "://:" + packet.payload.data.decode())
    except ClientException as ce:
        logging.error("Client exception: %s" % ce)

    return values

@asyncio.coroutine
def subscribe_non_stop(thingy, topic):
    values = []
    yield from client.subscribe([
        (thingy + topic, QOS_2)
    ])
    try:
        while True:
            time.sleep(10)
            message = yield from client.deliver_message()
            packet = message.publish_packet
            data = packet.variable_header.topic_name + "://:" + packet.payload.data.decode()
            print("Data received from the thingy : " + data)
            values.append(data)
            insert_environment_data(data)
    except ClientException as ce:
        logging.error("Client exception: %s" % ce)
        return "error"