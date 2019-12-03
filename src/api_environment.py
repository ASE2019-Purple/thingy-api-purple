import db
import logging
from aiohttp.web import run_app
from aiohttp import web
import aiohttp_cors

import datetime

thingy_temperature_charac = "Thingy-Temperature-Characteristic"
thingy_humidity_charac = "Thingy-Humidity-Characteristic"
thingy_pressure_charac = "Thingy-Pressure-Characteristic"
thingy_air_quality_charac = "Thingy-Air-Quality-Characteristic"

#API METHODS
#------------------------------------------------------------------------------
def get_temperature(request):
    temperatures = list(db.get_all(thingy_temperature_charac))
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
        return web.json_response("Bad request, date format should be YYYY-MM-DD", status=400)

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
    humidities = list(db.get_all(thingy_humidity_charac))
    return web.json_response(humidities)

def get_air_quality(request):
    list_airquality = list(db.get_all(thingy_air_quality_charac))
    return web.json_response(list_airquality)

def get_pressure(request):
    pressures = list(db.get_all(thingy_pressure_charac))
    return web.json_response(pressures)

def get_things(request):
    things = []
    # TODO
    return web.json_response(things)

def get_thing(request):
    thing_id = int(request.match_info['id'])
    thing = [thing_id]
    # TODO
    return web.json_response(thing)

def get_thing_properties(request):
    properties = []
    # TODO
    return web.json_response(properties)

def get_thing_property(request):
    thing_id = request.match_info['id']
    # property_type = int(request.match_info['type'])
    # property = [property_type]
    property = db.get_thingy_temperature(thing_id)
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

#Logic Methods
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
    
    #Get data from db
    if filterByHours:
        return list(db.get_characteristic_by_hours(characteristic, date, startHour, endHour))
    
    return list(db.get_characteristic_by_day(characteristic, date))


def validate_date(date):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect date format, should be YYYY-MM-DD")

#App Factory
#------------------------------------------------------------------------------
async def app_factory(args=()):
    # init the db
    await db.init_db()
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

    # Resources
    things_resource = cors.add(app.router.add_resource("/things/", name='things'))
    cors.add(things_resource.add_route("GET", get_things))
    thing_resource = cors.add(app.router.add_resource("/thing/{id}", name='thing'))
    cors.add(thing_resource.add_route("GET", get_thing))
    thing_properties_resource = cors.add(app.router.add_resource("/thing/{id}/properties/", name='thing_properties'))
    cors.add(thing_properties_resource.add_route("GET", get_thing_properties))
    thing_property_resource = cors.add(app.router.add_resource("/thing/{id}/property/temperature", name='thing_property'))
    cors.add(thing_property_resource.add_route("GET", get_thing_property))
    cors.add(thing_property_resource.add_route("PUT", put_thing_property))
    thing_events_resource = cors.add(app.router.add_resource("/thing/{id}/events/", name='thing_events'))
    cors.add(thing_events_resource.add_route("GET", get_thing_events))
    thing_event_resource = cors.add(app.router.add_resource("/thing/{id}/event/{type:\d+}", name='thing_event'))
    cors.add(thing_event_resource.add_route("GET", get_thing_event))
    
    return app
if __name__ == '__main__':
    run_app(app_factory(), host='0.0.0.0', port=8080)
