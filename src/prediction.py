import mysql
import influx
import asyncio
import weather
from datetime import datetime, date, timedelta

optimal_humidity = 80
optimal_temperature = 20
optimal_rain_volume = 1
accepted_tolerance_temperature = 3
accepted_tolerance_humidity = 20
async def predict(plant_id, thingy_id):
    #Get the plant from the db
    plant = mysql.select_plant_by_id(plant_id)

    #Get thingy info
    thingy = mysql.select_thing_by_id(thingy_id)

    #Get the weather predictions based on the thingy location
    weather_prediction = await weather.get_weather_for_5_days(thingy['location'])

    #Check plant's start date to generate the calendar prediction
    if datetime.today() <= datetime.strptime(plant['start_date'],'%Y-%m-%d'):
        return generate_prediction_calendar(plant['start_date'], plant, thingy, weather_prediction)

    days_difference = days_between(plant['start_date'], datetime.today().strftime('%Y-%m-%d'))
    if days_difference >= plant['watering_interval_days']:
        substracted_date = (datetime.today() - timedelta(days=plant['watering_interval_days'])).strftime('%Y-%m-%d')
        return generate_prediction_calendar(substracted_date, plant, thingy, weather_prediction)

    substracted_date = (datetime.today() - timedelta(days=days_difference)).strftime('%Y-%m-%d')
    return generate_prediction_calendar(substracted_date, plant, thingy, weather_prediction)


def generate_prediction_calendar(startDate, plant, thingy, weather_prediction):
    calendar = []

    nb_sunny_days = 0
    nb_rainy_days = 0
    nb_optimal_days = 0

    total_days = 0

    #Get thingy info for past dates
    dateString = startDate
    currentDate = datetime.strptime(dateString, "%Y-%m-%d")
    while currentDate < datetime.now() and currentDate.strftime("%Y-%m-%d") != datetime.now().strftime("%Y-%m-%d"):
        total_days += 1
        print("Getting thingy info for date : " + dateString)
        average_temperature = influx.get_thingy_average_characteristic(thingy['mac_address'], "Thingy-Temperature-Characteristic", dateString)
        average_humidity = influx.get_thingy_average_characteristic(thingy['mac_address'], "Thingy-Humidity-Characteristic", dateString)

        if average_temperature == None or average_humidity == None:
            print("No data available at this date")
        else:
            obj = {
                "date" : dateString,
                "type" : "thingy",
                "temperature" : average_temperature,
                "humidity" : current_rain_volume
            }
            calendar.append(obj)
        currentDate = currentDate + timedelta(days=1)
        dateString = currentDate.strftime("%Y-%m-%d")

    print("OUT OF THE WHILE")
    print("NB SUNNY DAYS : " + str(nb_sunny_days))
    print("NB RAINY DAYS : " + str(nb_rainy_days))
    print("NB OPTIMAL DAYS : " + str(nb_optimal_days))
    print("TOTAL DAYS : " + str(total_days))

    print("avant parcourir les weather" + dateString)
    current_temperature = 0
    current_rain_volume = 0
    cpt = 0
    for weather in weather_prediction:
        print(weather['temperature']['temp'])
        if dateString == weather['reference_time']:
            try:
                cpt += 1
                current_temperature += weather['temperature']['temp']
                current_rain_volume += weather['rain_volume']['3h']
            except :
                print("No rain")
        elif cpt == 0:
            dateString = weather['reference_time']
            try:
                cpt += 1
                current_temperature += weather['temperature']['temp']
                current_rain_volume += weather['rain_volume']['3h']
            except :
                print("No rain")
        else:
            #Calculate average value
            obj = {
                "date" : dateString,
                "type" : "weather",
                "temperature" : current_temperature / cpt,
                "rain_volume" : current_rain_volume
            }
            calendar.append(obj)
            cpt = 0
            current_temperature = 0
            current_rain_volume = 0
            dateString = weather['reference_time']
            try:
                cpt += 1
                current_temperature += weather['temperature']['temp']
                current_rain_volume += weather['rain_volume']['3h']
            except :
                print("No rain")

    return evaluate_calendar(calendar, plant)

def evaluate_calendar(cal, plant):
    print(plant)
    calendar = []
    days_since_optimal = 0
    for x in cal:
        print("days since optimal : " + str(days_since_optimal))
        #Thingy prediction
        if x['type'] == 'thingy':
            if is_optimal_day_thingy(x['temperature'], x['humidity']):
               days_since_optimal = 0
               calendar.append({"date": x['date'], "watering": False})
            elif days_since_optimal == plant['watering_interval_days'] -1:
                calendar.append({"date": x['date'], "watering": True})
                days_since_optimal = 0
            else:
                calendar.append({"date": x['date'], "watering": False})
                days_since_optimal += 1
        #Weather prediction            
        else:
            if is_optimal_day_weather(x['temperature'], x['rain_volume']):
                days_since_optimal = 0
                calendar.append({"date": x['date'], "watering": False})
            elif days_since_optimal == plant['watering_interval_days'] -1:
                calendar.append({"date": x['date'], "watering": True})
                days_since_optimal = 0
            else:
                calendar.append({"date": x['date'], "watering": False})
                days_since_optimal += 1


    return calendar

def is_optimal_day_thingy(average_temperature, average_humidity):
    if is_sunny_day(average_temperature):
        if is_humid_day(average_humidity):
            return True
    return False

def is_optimal_day_weather(average_temperature, average_humidity):
    if is_sunny_day(average_temperature):
        if is_rainy_day(average_humidity):
            return True
    return False

def is_sunny_day(average_temperature):
    print("AVERAGE TEMPERATURE : " + str(average_temperature))
    if average_temperature >= optimal_temperature-accepted_tolerance_temperature and average_temperature <= optimal_temperature + accepted_tolerance_temperature:
        return True
    return False

def is_humid_day(average_humidity):
    print("AVERAGE HUMIDITY : " + str(average_humidity))
    if average_humidity >= optimal_humidity - accepted_tolerance_humidity and average_humidity <= optimal_humidity + accepted_tolerance_humidity:
        return True
    return False

def is_rainy_day(rain_volume):
    if rain_volume >= optimal_rain_volume:
        return True
    return False

def days_between(d1,d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

async def main():
    await mysql.init_db()
    await influx.init_db()
    calendar = await predict(3,1)
    print(calendar)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
