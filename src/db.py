import asyncio
import os
from dotenv import load_dotenv
from influxdb import InfluxDBClient
from pathlib import Path  # python3 only

env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)

client = None

INFLUXDB_HOSTNAME = os.getenv('INFLUXDB_HOSTNAME')
INFLUXDB_PORT = os.getenv('INFLUXDB_PORT')
INFLUXDB_USER = os.getenv("INFLUXDB_USER")
INFLUXDB_USER_PASSWORD = os.getenv("INFLUXDB_USER_PASSWORD")
INFLUXDB_DB = os.getenv("INFLUXDB_DB")


async def init_db():
    global client
    client = InfluxDBClient('db', INFLUXDB_PORT, INFLUXDB_USER, INFLUXDB_USER_PASSWORD, INFLUXDB_DB)
    create_database()


def create_database():
    for db in client.get_list_database():
        if db['name'] == 'purple':
            return
    client.create_database('purple')


def drop_database():
    client.drop_database('purple')


def insert_bulk(values):
    points = []
    for v in values:
        points.append(insert_environment_data(v))
    client.write_points(points)


def insert_environment_light(topic_value_array, topic_array):
    value1 = topic_value_array[1].split(',')[0]
    value2 = topic_value_array[1].split(',')[1]
    value3 = topic_value_array[1].split(',')[2]
    value4 = topic_value_array[1].split(',')[3]

    point = {
        "measurement": topic_array[2].replace(' ', '-'),
        "tags": {
            "thingy": topic_array[0].replace(' ', '-'),
            "service": topic_array[1].replace(' ', '-'),
            "characteristic": topic_array[2].replace(' ', '-'),
        },
        "fields": {
            "value1": float(value1),
            "value2": float(value2),
            "value3": float(value3),
            "value4": float(value4)
        }
    }

    return point


def insert_environment_others(topic_value_array, topic_array, value):
    point = {
        "measurement": topic_array[2].replace(' ', '-'),
        "tags": {
            "thingy": topic_array[0].replace(' ', '-'),
            "service": topic_array[1].replace(' ', '-'),
            "characteristic": topic_array[2].replace(' ', '-'),
        },
        "fields": {
            "value": float(value.replace(',', '.'))
        }
    }

    return point


# DATA = THINGY/SERVICE/CHARACTERISTIC://:VALUE
def insert_environment_data(data):
    topic_value_array = data.split('://:')
    topic_array = topic_value_array[0].split('/')
    value = topic_value_array[1]

    if "Light Intensity" in topic_array[2]:
        return insert_environment_light(topic_value_array, topic_array)

    return insert_environment_others(topic_value_array, topic_array, value)


def get_all_humidity():
    return client.query('select * from "Thingy-Humidity-Characteristic"')


def get_all_temperature():
    return client.query('select * from "Thingy-Temperature-Characteristic"')


def get_all_pressure():
    return client.query('select * from "Thingy-Pressure-Characteristic"')


def get_all_air_quality():
    return client.query('select * from "Thingy-Air-Quality-Characteristic"')
