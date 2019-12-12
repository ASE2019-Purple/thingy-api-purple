import influx
import mysql
import logging
from aiohttp.web import run_app
from aiohttp import web
import aiohttp_cors
import datetime

#PLANTS API METHODS
#------------------------------------------------------------------------------
def get_plants(request):
    result = mysql.select_plants()
    return web.json_response(result, status=200)

def get_plant(request):
    result = mysql.select_plant_by_id(request.match_info['id'])
    if result == None: return web.json_response("Plant not found", status=404)
    return web.json_response(result, status=200)

async def post_plants(request):
    data = await request.json()
    mysql.insert_plant(data['name'], data['nb_sunny_days'], data['nb_rainy_days'], data['watering_interval_days'], data['thing_id'])
    return web.json_response(data, status=201)

#THINGY API METHODS
#------------------------------------------------------------------------------
def get_things(request):
    result = mysql.select_things()
    return web.json_response(result, status=200)

def get_thing(request):
    result = mysql.select_thing_by_id(request.match_info['id'])
    if result == None: return web.json_response("Thing not found", status=404)
    return web.json_response(result, status=200)

def get_thing_properties(request):
    results = {}
    thing = mysql.select_thing_by_id(request.match_info['id'])
    if thing == None: return web.json_response("Thing not found", status=404)
    if request.query_string.split("&") == ['']: 
        for property in mysql.select_properties():
            results[property['name']] = influx.get_thingy_characteristic(thing['mac_address'], property['characteristic'])
    else:
        params = dict(x.split("=") for x in request.query_string.split("&"))
        for property in mysql.select_properties():
            results[property['name']] = get_filter_data(thing['mac_address'], property['characteristic'], params)
    return web.json_response(results, status=200)

def get_thing_property(request):
    thing = mysql.select_thing_by_id(request.match_info['id'])
    if thing == None: return web.json_response("Thing not found", status=404)
    property = mysql.select_property_by_name(request.match_info['name'])
    if property == None: return web.json_response("Property not found", status=404)
    if request.query_string.split("&") == ['']: 
        result = influx.get_thingy_characteristic(thing['mac_address'], property['characteristic'])
    else:
        params = dict(x.split("=") for x in request.query_string.split("&"))
        result = get_filter_data(thing['mac_address'], property['characteristic'], params)
    return web.json_response(result, status=200)

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

#LOGIC METHODS
#------------------------------------------------------------------------------
def get_filter_data(thingy_mac, characteristic_name, params):
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
        return list(influx.get_characteristic_by_hours(characteristic_name, date, startHour, endHour, thingy_mac))
    
    return list(influx.get_characteristic_by_day(characteristic_name, date, thingy_mac))


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

    # Resources
    plants_resource = cors.add(app.router.add_resource("/plants", name='plants'))
    cors.add(plants_resource.add_route("GET", get_plants))
    cors.add(plants_resource.add_route("POST", post_plants))
    plant_resource = cors.add(app.router.add_resource("/plant/{id:\\d+}", name='plant'))
    cors.add(plant_resource.add_route("GET", get_plant))
    things_resource = cors.add(app.router.add_resource("/things", name='things'))
    cors.add(things_resource.add_route("GET", get_things))
    thing_resource = cors.add(app.router.add_resource("/thing/{id:\\d+}", name='thing'))
    cors.add(thing_resource.add_route("GET", get_thing))
    thing_properties_resource = cors.add(app.router.add_resource("/thing/{id:\\d+}/properties", name='thing_properties'))
    cors.add(thing_properties_resource.add_route("GET", get_thing_properties))
    thing_property_resource = cors.add(app.router.add_resource("/thing/{id:\\d+}/property/{name}", name='thing_property'))
    cors.add(thing_property_resource.add_route("GET", get_thing_property))
    # cors.add(thing_property_resource.add_route("PUT", put_thing_property))
    # thing_events_resource = cors.add(app.router.add_resource("/thing/{id:\d+}/events/", name='thing_events'))
    # cors.add(thing_events_resource.add_route("GET", get_thing_events))
    # thing_event_resource = cors.add(app.router.add_resource("/thing/{id:\d+}/event/{type}", name='thing_event'))
    # cors.add(thing_event_resource.add_route("GET", get_thing_event))
    
    return app
    
if __name__ == '__main__':
    run_app(app_factory(), host='0.0.0.0', port=8081)
