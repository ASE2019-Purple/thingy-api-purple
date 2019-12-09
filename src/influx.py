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
    client = InfluxDBClient('35.241.155.14',8086,'purple','purple','purple')
    create_database()


def create_database():
    for db in client.get_list_database():
        if db['name'] == 'purple':
            return
    client.create_database('purple')


def drop_database():
    client.drop_database('purple')


def insert_bulk(values):
    for v in values:
        insert_environment_data(v)


def insert_environment_light(topic_value_array, topic_array):
    value1 = topic_value_array[1].split(',')[0]
    value2 = topic_value_array[1].split(',')[1]
    value3 = topic_value_array[1].split(',')[2]
    value4 = topic_value_array[1].split(',')[3]

    point = [{
        "measurement": "Environment-Light",
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
    }]

    client.write_points(point)


def insert_environment_others(topic_value_array, topic_array, value):
    point = [{
        "measurement": topic_array[2].replace(' ', '-'),
        "tags": {
            "thingy": topic_array[0].replace(' ', '-'),
            "service": topic_array[1].replace(' ', '-'),
            "characteristic": topic_array[2].replace(' ', '-'),
        },
        "fields": {
            "value": float(value.replace(',', '.'))
        }
    }]

    client.write_points(point)


# DATA = THINGY/SERVICE/CHARACTERISTIC://:VALUE
def insert_environment_data(data):
    print("data received in db\n")
    topic_value_array = data.split('://:')
    topic_array = topic_value_array[0].split('/')
    value = topic_value_array[1]

    if "Light Intensity" in topic_array[2]:
        return insert_environment_light(topic_value_array, topic_array)

    return insert_environment_others(topic_value_array, topic_array, value)

def get_all(characteristic):
    return client.query('select * from "'+characteristic+'"')

def get_characteristic_by_day(characteristic, date):
    query = 'SELECT * FROM "'+characteristic+'" WHERE time >= \''+date+'T00:00:00Z\' AND time <= \''+date+'T23:59:00Z\''
    return client.query(query)

def get_characteristic_by_hours(characteristic, date, startHour, endHour):
    query = 'SELECT * FROM "'+characteristic+'" WHERE time >= \''+date+'T'+startHour+':00Z\' AND time <= \''+date+'T'+endHour+':00Z\''
    return client.query(query)

def get_thingy_humidity(thingy):
    rs = client.query('select * from "Thingy-Humidity-Characteristic"')
    return list(rs.get_points(tags={'thingy': thingy}))

def get_thingy_temperature(thingy):
    rs = client.query('select * from "Thingy-Temperature-Characteristic"')
    return list(rs.get_points(tags={'thingy': thingy}))

def get_thingy_pressure(thingy):
    rs = client.query('select * from "Thingy-Pressure-Characteristic"')
    return list(rs.get_points(tags={'thingy': thingy}))

def get_thingy_air_quality(thingy):
    rs = client.query('select * from "Thingy-Air-Quality-Characteristic"')
    return list(rs.get_points(tags={'thingy': thingy}))

def create_retention_policy(name, duration, default):
    client.create_retention_policy(name, duration, 1, database=INFLUXDB_DB, default=default, shard_duration=duration)

def get_list_retention_policies():
    return client.get_list_retention_policies(database=INFLUXDB_DB)