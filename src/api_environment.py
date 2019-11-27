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

    return app