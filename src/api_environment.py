import db

from aiohttp import web
import aiohttp_cors

def get_temperature(request):
    temperatures = list(db.get_all_temperature())
    return web.json_response(temperatures)

def get_humidity(request):
    humidities = list(db.get_all_humidity())
    return web.json_response(humidities)
    
def get_air_quality(request):
    list_airquality = list(db.get_all_air_quality())
    return web.json_response(list_airquality)

def get_pressure(request):
    pressures = list(db.get_all_pressure())
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

async def app_factory(args=()):
    #init the db
    await db.init_db()
    #Create web app
    app = web.Application()

    # Configure default CORS settings.
    cors = aiohttp_cors.setup(app,
    defaults={"*": aiohttp_cors.ResourceOptions(allow_credentials=True,expose_headers="*",allow_headers="*")})

    #Temperature routes
    temperature_route = cors.add(app.router.add_resource('/temperature'))
    cors.add(temperature_route.add_route("GET", get_temperature))

    #Humidity routes
    humidity_route = cors.add(app.router.add_resource('/humidity'))
    cors.add(humidity_route.add_route("GET",get_humidity))

    #Pressure routes
    pressure_route = cors.add(app.router.add_resource('/pressure'))
    cors.add(pressure_route.add_route("GET",get_air_quality))

    #Air quality routes
    air_quality_route = cors.add(app.router.add_resource('/air-quality'))
    cors.add(air_quality_route.add_route("GET",get_air_quality))

    # Resources
    things_resource = cors.add(app.router.add_resource("/things/", name='things'))
    cors.add(things_resource.add_route("GET", get_things))
    thing_resource = cors.add(app.router.add_resource("/thing/{id}", name='thing'))
    cors.add(thing_resource.add_route("GET", get_thing))
    thing_properties_resource = cors.add(app.router.add_resource("/thing/{id}/properties/", name='thing_properties'))
    cors.add(thing_properties_resource.add_route("GET", get_thing_properties))
    thing_property_resource = cors.add(app.router.add_resource("/thing/{id}/property/temperatrue", name='thing_property'))
    cors.add(thing_property_resource.add_route("GET", get_thing_property))
    cors.add(thing_property_resource.add_route("PUT", put_thing_property))
    thing_events_resource = cors.add(app.router.add_resource("/thing/{id}/events/", name='thing_events'))
    cors.add(thing_events_resource.add_route("GET", get_thing_events))
    thing_event_resource = cors.add(app.router.add_resource("/thing/{id}/event/{type:\d+}", name='thing_event'))
    cors.add(thing_event_resource.add_route("GET", get_thing_event))
    
    return app