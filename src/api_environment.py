import influx
import mysql
import logging
from aiohttp.web import run_app
from aiohttp import web
import aiohttp_cors

properties_types = {
    "temperature": "Thingy-Temperature-Characteristic",
    "humidity": "Thingy-Humidity-Characteristic",
    "pressure": "Thingy-Pressure-Characteristic",
    "airquality": "Thingy-Air-Quality-Characteristic"
}

thingys = ["fe:84:88:ca:47:ca", "e6:97:3d:de:ca:a3", "fe:0f:3c:ed:a3:d6"]

#THINGY API METHODS
#------------------------------------------------------------------------------
def get_temperature(request):
    print(request.query_string)
    temperatures = list(influx.get_all(properties_types["temperature"]))
    return web.json_response(temperatures)

def get_temperature_filter(request):
    params = dict(x.split("=") for x in request.query_string.split("&"))
    temperatures = []
    try:
        temperatures = get_filter_data(thingy_temperature_charac, params)
    except:
        return web.json_response("Bad request, date format should be YYYY-MM-DD", status=400)

    return web.json_response(temperatures)

def get_humidity_filter(request):
    params = dict(x.split("=") for x in request.query_string.split("&"))
    humidities = []
    try:
        humidities = get_filter_data(thingy_humidity_charac, params)
    except:
        return web.json_response("Bad request, date format should be YYYY-MM-DD", status=400)

    return web.json_response(humidities)

def get_pressure_filter(request):
    params = dict(x.split("=") for x in request.query_string.split("&"))
    pressures = []
    try:
        pressures = get_filter_data(thingy_pressure_charac, params)
    except:
        filterByHours = False
    
    #Get data from db
    temperatures = []
    if filterByHours:
        temperatures = list(influx.get_characteristic_by_hours(properties_types["temperature"], date, startHour, endHour))
    else:
        temperatures = list(influx.get_characteristic_by_day(properties_types["temperature"], date))

    return web.json_response(pressures)

def get_air_quality_filter(request):
    params = dict(x.split("=") for x in request.query_string.split("&"))
    list_airquality = []
    try:
        list_airquality = get_filter_data(thingy_air_quality_charac, params)
    except:
        return web.json_response("Bad request, date format should be YYYY-MM-DD", status=400)

    return web.json_response(list_airquality)

def get_humidity(request):
    humidities = list(influx.get_all(properties_types["humidity"]))
    return web.json_response(humidities)

def get_air_quality(request):
    list_airquality = list(influx.get_all(properties_types["airquality"]))
    return web.json_response(list_airquality)

def get_pressure(request):
    pressures = list(influx.get_all(properties_types["pressure"]))
    return web.json_response(pressures)

def get_things(request):
    things = []
    # TODO
    return web.json_response(things)

def get_thing(request):
    thing_mac = thingys[int(request.match_info['id'])-1]
    thing = [thing_mac]
    # TODO
    return web.json_response(thing)

def get_thing_properties(request):
    properties = {}
    try: thing_mac = thingys[int(request.match_info['id'])-1]
    except IndexError as e: raise web.HTTPNotFound
    for key, value in properties_types.items():
        properties[key] = influx.get_thingy_last_characteristic(thing_mac, value)
    return web.json_response(properties)

def get_thing_property(request):
    try: thing_mac = thingys[int(request.match_info['id'])-1]
    except IndexError as e: raise web.HTTPNotFound
    try: property_type = properties_types[request.match_info['type']]
    except KeyError as e: raise web.HTTPNotFound
    property = influx.get_thingy_last_characteristic(thing_mac, property_type)
    return web.json_response(property)

async def put_thing_property(request):
    thing_id = request.match_info['id']
    property = await request.json()
    # TODO
    return get_thing_property(request)

def get_thing_events(request):
    events = []
    # TODO
    return web.json_response(events)

def get_thing_event(request):
    thing_id = request.match_info['id']
    event_type = int(request.match_info['type'])
    event = [event_type]
    # TODO
    return web.json_response(event)


#PLANTS API METHODS
#------------------------------------------------------------------------------
def get_plant(request):
    id = int(request.match_info['id'])
    result = mysql.get_plant_by_id(id)

    if result == None:
        return web.json_response("Plant not found", status=404)

    return web.json_response(result, status=200)

def get_plants(request):
    result = mysql.get_all_plants()

    if result == None:
        return web.json_response("No plants available", status=404)

    return web.json_response(result, status=200)

async def add_plant(request):
    data = await request.json()
    mysql.insert_plant(data['name'], data['nb_sunny_days'], data['nb_rainy_days'], data['watering_interval_days'])
    raise web.HTTPFound('/plants')

#LOGIC METHODS
#------------------------------------------------------------------------------
def get_filter_data(characteristic, params):
    #Check corectness of the params
    filterByHours = True
    date = None
    startHour = None
    endHour = None
    try:
        date = params['date']
        validate_date(date)
    except ValueError:
        raise ValueError("Incorrect date format, should be YYYY-MM-DD")

    try:
        startHour = params['startHour']
        endHour = params['endHour']
    except:
        filterByHours = False
    
    #Get data from influx db
    if filterByHours:
        return list(influx.get_characteristic_by_hours(characteristic, date, startHour, endHour))
    
    return list(influx.get_characteristic_by_day(characteristic, date))


def validate_date(date):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect date format, should be YYYY-MM-DD")

#App Factory
#------------------------------------------------------------------------------
async def app_factory(args=()):
    # init the db
    await influx.init_db()
    await mysql.init_db()
    # Create web app
    app = web.Application()

    # Configure default CORS settings.
    cors = aiohttp_cors.setup(app,
                              defaults={"*": aiohttp_cors.ResourceOptions(allow_credentials=True, expose_headers="*",
                                                                          allow_headers="*")})

    # Temperature routes
    temperature_route = cors.add(app.router.add_resource('/temperature'))
    cors.add(temperature_route.add_route("GET", get_temperature))
    temperature_filter_route = cors.add(app.router.add_resource('/temperature/filter'))
    cors.add(temperature_filter_route.add_route("GET", get_temperature_filter))

    # Humidity routes
    humidity_route = cors.add(app.router.add_resource('/humidity'))
    cors.add(humidity_route.add_route("GET", get_humidity))
    humidity_filter_route = cors.add(app.router.add_resource('/humidity/filter'))
    cors.add(humidity_filter_route.add_route("GET", get_humidity_filter))

    # Pressure routes
    pressure_route = cors.add(app.router.add_resource('/pressure'))
    cors.add(pressure_route.add_route("GET", get_pressure))
    pressure_filter_route = cors.add(app.router.add_resource('/pressure/filter'))
    cors.add(pressure_filter_route.add_route("GET", get_pressure_filter))

    # Air quality routes
    air_quality_route = cors.add(app.router.add_resource('/air-quality'))
    cors.add(air_quality_route.add_route("GET", get_air_quality))
    air_quality_filter_route = cors.add(app.router.add_resource('/air-quality/filter'))
    cors.add(air_quality_filter_route.add_route("GET", get_air_quality_filter))

    #Plants routes
    plant_route = cors.add(app.router.add_resource('/plants/{id:\d+}'))
    cors.add(plant_route.add_route("GET", get_plant))

    plants_route = cors.add(app.router.add_resource('/plants'))
    cors.add(plants_route.add_route("GET", get_plants))
    cors.add(plants_route.add_route("POST", add_plant))




    # Resources
    # things_resource = cors.add(app.router.add_resource("/things/", name='things'))
    # cors.add(things_resource.add_route("GET", get_things))
    # thing_resource = cors.add(app.router.add_resource("/thing/{id:\d+}", name='thing'))
    # cors.add(thing_resource.add_route("GET", get_thing))
    thing_properties_resource = cors.add(app.router.add_resource("/thing/{id:\d+}/properties/", name='thing_properties'))
    cors.add(thing_properties_resource.add_route("GET", get_thing_properties))
    thing_property_resource = cors.add(app.router.add_resource("/thing/{id:\d+}/property/{type}", name='thing_property'))
    cors.add(thing_property_resource.add_route("GET", get_thing_property))
    # cors.add(thing_property_resource.add_route("PUT", put_thing_property))
    # thing_events_resource = cors.add(app.router.add_resource("/thing/{id:\d+}/events/", name='thing_events'))
    # cors.add(thing_events_resource.add_route("GET", get_thing_events))
    # thing_event_resource = cors.add(app.router.add_resource("/thing/{id:\d+}/event/{type}", name='thing_event'))
    # cors.add(thing_event_resource.add_route("GET", get_thing_event))
    
    return app
    
if __name__ == '__main__':
    run_app(app_factory(), host='0.0.0.0', port=8081)
