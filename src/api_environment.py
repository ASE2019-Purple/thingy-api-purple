import influx
import mysql
import logging
from aiohttp.web import run_app
from aiohttp import web
import aiohttp_cors
import datetime
import prediction
import notification
from aiohttp_swagger import setup_swagger

# PLANTS API METHODS
# ------------------------------------------------------------------------------

def get_plants(request):
    result = mysql.select_plants()
    return web.json_response(result, status=200)


def get_plant(request):
    result = mysql.select_plant_by_id(request.match_info["id"])
    if result == None:
        return web.json_response(status=404)
    return web.json_response(result, status=200)


async def post_plant(request):
    data = await request.json()
    try:
        plant_id = mysql.insert_plant(data)
    except KeyError:
        return web.json_response(status=400)
    return web.json_response(mysql.select_plant_by_id(plant_id), status=201)


async def put_plant(request):
    data = await request.json()
    data["plant_id"] = request.match_info["id"]
    try:
        mysql.update_plant_by_id(data)
    except KeyError:
        return web.json_response(status=400)
    return web.json_response(mysql.select_plant_by_id(data["plant_id"]), status=200)


def delete_plant(request):
    if mysql.delete_plant_by_id(request.match_info["id"]):
        return web.json_response(status=204)
    return web.json_response(status=404)


async def get_plant_prediction(request):
    # Get the plant from the db
    plant = mysql.select_plant_by_id(request.match_info["id"])

    # Get thingy info
    thingy = mysql.select_thing_by_id(plant.get("thing_id"))

    result = await prediction.predict(plant, thingy)
    if not result:
        return web.json_response(status=404)

    # send_notification(result, plant['name'], thingy['location'])
    return web.json_response(result, status=200)


# THINGY API METHODS
# ------------------------------------------------------------------------------


def get_things(request):
    results = mysql.select_things()
    for result in results:
            result["links"] = [{"href": "http://" + request.host + "/thing/" + str(result["id"])}]
    return web.json_response(results, status=200)


def get_thing(request):
    result = mysql.select_thing_by_id(request.match_info["id"])
    if result == None:
        return web.json_response(status=404)
    properties = mysql.select_properties()
    for property in properties:
            property["links"] = [{"href": "http://" + request.host + "/thing/" + str(result["id"]) + "/property/" + property["name"]}]
    result["properties"] = properties
    result["links"] = [{"rel": "properties","href": "http://" + request.host + "/thing/" + str(result["id"]) + "/properties"}]
    return web.json_response(result, status=200)


async def post_thing(request):
    data = await request.json()
    try:
        thing_id = mysql.insert_thing(data)
    except KeyError:
        return web.json_response(status=400)
    return web.json_response(mysql.select_thing_by_id(thing_id), status=201)


def delete_thing(request):
    if mysql.delete_thing_by_id(request.match_info["id"]):
        return web.json_response(status=204)
    return web.json_response(status=404)


def get_thing_properties(request):
    results = {}
    thing = mysql.select_thing_by_id(request.match_info["id"])
    if thing == None:
        return web.json_response(status=404)
    if request.query_string.split("&") == [""]:
        for property in mysql.select_properties():
            results[property["name"]] = influx.get_thingy_characteristic(
                thing["mac_address"], property["characteristic"]
            )
    else:
        params = dict(x.split("=") for x in request.query_string.split("&"))
        for property in mysql.select_properties():
            results[property["name"]] = get_filter_data(
                thing["mac_address"], property["characteristic"], params
            )
    return web.json_response(results, status=200)


def get_thing_property(request):
    thing = mysql.select_thing_by_id(request.match_info["id"])
    if thing == None:
        return web.json_response(status=404)
    property = mysql.select_property_by_name(request.match_info["name"])
    if property == None:
        return web.json_response(status=404)
    if request.query_string.split("&") == [""]:
        result = influx.get_thingy_characteristic(
            thing["mac_address"], property["characteristic"]
        )
    else:
        params = dict(x.split("=") for x in request.query_string.split("&"))
        result = get_filter_data(
            thing["mac_address"], property["characteristic"], params
        )
    return web.json_response(result, status=200)


async def put_thing_property(request):
    thing_id = request.match_info["id"]
    property = await request.json()
    # TODO
    return web.json_response(get_thing_property(request), status=501)


# LOGIC METHODS
# ------------------------------------------------------------------------------
def get_filter_data(thingy_mac, characteristic_name, params):
    # Check corectness of the params
    filterByHours = True
    date = None
    startHour = None
    endHour = None

    start_date = params.get("start_date")
    end_date = params.get("end_date")

    if start_date:
        validate_date(start_date)
        if end_date:
            validate_date(end_date)
        else:
            end_date = datetime.today().strftime("%Y-%m-%d")

        return influx.get_characteristic_by_date_range(
            characteristic_name, start_date, end_date, thingy_mac
        )

    try:
        date = params["date"]
        validate_date(date)
    except ValueError:
        raise ValueError("Incorrect date format, should be YYYY-MM-DD")

    try:
        startHour = params["startHour"]
        endHour = params["endHour"]
    except:
        filterByHours = False

    # Get data from influx db
    if filterByHours:
        return influx.get_characteristic_by_hours(
            characteristic_name, date, startHour, endHour, thingy_mac
        )

    return influx.get_characteristic_by_day(characteristic_name, date, thingy_mac)


def validate_date(date):
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Incorrect date format, should be YYYY-MM-DD")


def send_notification(calendar, plant_name, location):
    message = "Hello,\n\nHere are your next watering days for the plant " + plant_name + " in " + location + "\n\n"
    for x in calendar:
        if x['watering'] == True:
            message += x['date'] + "\n"

    notification.send_message(message, '+41792490274')


# App Factory
# ------------------------------------------------------------------------------
async def app_factory(args=()):
    
    # init the db
    await influx.init_db()
    await mysql.init_db()
    await notification.init_twilio()

    # Create web app
    app = web.Application()

    # Configure default CORS settings.
    cors = aiohttp_cors.setup(
        app,
        defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True, expose_headers="*", allow_headers="*"
            )
        },
    )

    # Resources

    plants_resource = cors.add(app.router.add_resource("/plants", name="plants"))
    cors.add(plants_resource.add_route("GET", get_plants))
    cors.add(plants_resource.add_route("POST", post_plant))

    plant_resource = cors.add(app.router.add_resource("/plant/{id:\\d+}", name="plant"))
    cors.add(plant_resource.add_route("GET", get_plant))
    cors.add(plant_resource.add_route("PUT", put_plant))
    cors.add(plant_resource.add_route("DELETE", delete_plant))

    plant_prediction_resource = cors.add(app.router.add_resource("/plant/{id:\\d+}/prediction", name="plant_prediction"))
    cors.add(plant_prediction_resource.add_route("GET", get_plant_prediction))

    things_resource = cors.add(app.router.add_resource("/things", name="things"))
    cors.add(things_resource.add_route("GET", get_things))
    cors.add(things_resource.add_route("POST", post_thing))

    thing_resource = cors.add(app.router.add_resource("/thing/{id:\\d+}", name="thing"))
    cors.add(thing_resource.add_route("GET", get_thing))
    cors.add(thing_resource.add_route("DELETE", delete_thing))

    thing_properties_resource = cors.add(app.router.add_resource("/thing/{id:\\d+}/properties", name="thing_properties"))
    cors.add(thing_properties_resource.add_route("GET", get_thing_properties))
    thing_property_resource = cors.add(app.router.add_resource("/thing/{id:\\d+}/property/{name}", name="thing_property"))
    cors.add(thing_property_resource.add_route("GET", get_thing_property))

    setup_swagger(app, swagger_url="/api/v1/doc", swagger_from_file="..\swagger.yaml")

    return app


if __name__ == "__main__":
    run_app(app_factory(), host="0.0.0.0", port=8081)
