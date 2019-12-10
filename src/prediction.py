import mysql
import influx
import asyncio
import weather

async def predict(plant_id, thingy_id):
    #Get the plant from the db
    plant = await mysql.get_plant_by_id(plant_id)

    #Get thingy info
    thingy = await mysql.get_thingy_by_id(thingy_id)

    #Get the weather predictions based on the thingy location
    weather_prediction = await weather.get_weather_for_5_days(thingy['location'])

async def main():
    await mysql.init_db()
    await influx.init_db()
    await predict(1,1)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
