# Created by Narek at 08.12.2019

# Feature: # Get weather inforamtion
# Enter feature description here

# Scenario: # get the weather and forecast weather
# Enter steps here
import json
import pyowm
from pyowm.commons import http_client
from pyowm.utils import geo
from pyowm.weatherapi25 import forecaster, forecast
from pyowm.weatherapi25.configuration25 import THREE_HOURS_FORECAST_URL

from pyowm import OWM


API_KEY = '8074bee2618edf62080549a071a19914'
owm = OWM(API_key=API_KEY, language='en')

FribourgId = 2660718

# test = owm.three_hours_forecast_at_coords(47.9959, 7.85222)

f = owm.three_hours_forecast('London')
# print("three ours forcast", f)

# print("three_hours_forecast_at_coords ", test)

# CityWeather = owm.weather_at_id(FribourgId)

# print("Friborug Weather", CityWeather)

# CityFc = owm.three_hours_forecast_at_id(FribourgId)
# CityF = CityFc.get_forecast()
# weatherList = CityF.get_weathers()
# threeHours = 3 * 60 * 60
# newWeatherList = []
# time = CityFc.when_starts()
# interval = CityF.get_interval()
# reception_time = CityF.get_reception_time(timeformat='unix')
# location = CityF.get_location()

# for i in range(0, 2):
#     newWeatherList.append(CityFc.get_weather_at(time + threeHours * i))
#     print(newWeatherList)

# FribourgF = forecast.Forecast(interval, reception_time, location, newWeatherList)
# FribourgFc = forecaster.Forecaster(FribourgF)

# print(FribourgFc)

# Fribourg city ID 2660718


def get_weather_for_5_days(location):
    fc = owm.three_hours_forecast(location)
    forecast = fc.get_forecast()
    list_forecast = []
    for weather in forecast.get_weathers():
        obj = {
            "reference_time": weather.get_reference_time(timeformat="iso"),
            "cloud_coverage": weather.get_clouds(),
            "rain_volume" : weather.get_rain(),
            "snow_volume" : weather.get_snow(),
            "wind" : weather.get_wind(),
            "temperature" : weather.get_temperature(unit='celsius'),
            "weather_status": weather.get_detailed_status(),
            "sunset_time":weather.get_sunset_time('iso')
        }
        list_forecast.append(obj)
    return list_forecast

print(get_weather_for_5_days('Fribourg, CH'))

