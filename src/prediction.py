import mysql
import influx
import asyncio
import weather
from datetime import datetime, timedelta

async def predict(plant_id, thingy_id):
    #Get the plant from the db
    plant = mysql.select_plant_by_id(plant_id)

    #Get thingy info
    thingy = mysql.select_thing_by_id(thingy_id)

    #Get the weather predictions based on the thingy location
    weather_prediction = await weather.get_weather_for_5_days(thingy['location'])

    #Check plant's start date to generate the calendar prediction
    if datetime.today() < datetime.strptime(plant['start_date'],'%Y-%m-%d'):
        return generate_prediction_calendar(plant['start_date'], plant, thingy, weather_prediction)

    days_difference = days_between(plant['start_date'], datetime.today().strftime('%Y-%m-%d'))
    if days_difference >= plant['watering_interval_days']:
        substracted_date = (datetime.today() - timedelta(days=plant['watering_interval_days'])).strftime('%Y-%m-%d')
        return generate_prediction_calendar(substracted_date, plant, thingy, weather_prediction)

    substracted_date = (datetime.today() - timedelta(days=days_difference)).strftime('%Y-%m-%d')
    return generate_prediction_calendar(substracted_date, plant, thingy, weather_prediction)


def generate_prediction_calendar(startDate, plant, thingy, weather_prediction):
    calendar = {}
    

def days_between(d1,d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)


async def main():
    await mysql.init_db()
    await influx.init_db()
    await predict(3,1)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
