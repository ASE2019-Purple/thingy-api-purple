from influxdb import InfluxDBClient

client = None

point = [
    {
        "measurement": "cpu_load_short",
        "tags": {
            "host": "server01",
            "region": "us-west"
        },
        "time": "2009-11-10T23:00:00Z",
        "fields": {
            "value": 0.65
        }
    }
]

client = InfluxDBClient('localhost', 8086, 'purple', 'purple', 'purple')
client.create_database('purple')
client.write_points(point)
result = client.query('select value from cpu_load_short;')

print("Result: {0}".format(result))