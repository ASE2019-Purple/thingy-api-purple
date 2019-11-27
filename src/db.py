import asyncio
import os

from influxdb import InfluxDBClient

client = None

async def init_db():
    global client
    client = InfluxDBClient("localhost", 8086, "purple" , "purple","purple")
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