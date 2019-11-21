import asyncio

from influxdb import InfluxDBClient
from MQTTBroker import initMQTT, subscribeToTopic, thingys, topics


client = None

async def main():
    global client
    client = InfluxDBClient('localhost', 8086, 'purple', 'purple', 'purple')
    createDatabase()
    # query()
    await initMQTT()
    await populateDB()

def createDatabase():
    for db in client.get_list_database():
        if db['name'] == 'purple':
            return
    client.create_database('purple')


async def populateDB():
    values = await subscribeToTopic(thingys['Thingy1'], topics['EnvironmentAll'])
    insert_multiple_data(values)



#array expected
def insert_multiple_data(values):
    points = []
    for v in values:
        points.append(insert_data(v))
    client.write_points(points)


#parameter should be of the form : THINGY/SERVICE/CHARACTERISTIC://:VALUE
def insert_data(data):
    # Get the topic and the corresponding value
    topic_value_array = data.split('://:')
    topic_array = topic_value_array[0].split('/')
    value = topic_value_array[1]

    if "Light Intensity" in topic_array[2]:
        value1 = topic_value_array[1].split(',')[0]
        value2 = topic_value_array[1].split(',')[1]
        value3 = topic_value_array[1].split(',')[2]
        value4 = topic_value_array[1].split(',')[3]
        
        point = {
        "measurement" : topic_value_array[0],
        "tags" : {
            "thingy": topic_array[0].replace(' ','-'),
            "service": topic_array[1].replace(' ','-'),
            "characteristic": topic_array[2].replace(' ','-'),
        },
            "time": "2009-11-10T23:00:00Z",
            "fields": {
                "value1": float(value1),
                "value2": float(value2),
                "value3": float(value3),
                "value4": float(value4)
            }
        }

        return point
    
    point = {
        "measurement" : topic_value_array[0],
        "tags" : {
            "thingy": topic_array[0].replace(' ','-'),
            "service": topic_array[1].replace(' ','-'),
            "characteristic": topic_array[2].replace(' ','-'),
        },
        "time": "2009-11-10T23:00:00Z",
        "fields": {
            "value": float(value.replace(',', '.'))
        }
    }

    return point

def query():
    result = client.query('select value from "fe:84:88:ca:47:ca/Thingy Environment Service/Thingy Temperature Characteristic";')
    print("Result: {0}".format(result))
    


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
