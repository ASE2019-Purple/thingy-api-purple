# Created by Narek at 08.12.2019

# Feature: # Get weather information
# Enter feature description here

# Scenario: # get the weather and forecast weather
# Enter steps here

from pyowm import OWM

API_KEY = '8074bee2618edf62080549a071a19914'
owm = OWM(API_key=API_KEY, language='en')

FribourgId = 2660718


def get_weather_for_5_days(location):
    fc = owm.three_hours_forecast(location)
    _forecast = fc.get_forecast()
    list_forecast = []
    for weather in _forecast.get_weathers():
        obj = {
            "reference_time": weather.get_reference_time(timeformat="iso"),
            "cloud_coverage": weather.get_clouds(),
            "rain_volume": weather.get_rain(),
            "snow_volume": weather.get_snow(),
            "wind": weather.get_wind(),
            "temperature": weather.get_temperature(unit='celsius'),
            "weather_status": weather.get_detailed_status(),
            "sunset_time": weather.get_sunset_time('iso')
        }
        list_forecast.append(obj)
    return list_forecast


lat = 46.803  # for Fribourg
lon = 7.1513  # for Fribourg


def get_weather_for_5_days_lat_lon(_lat, _lon):
    fc = owm.three_hours_forecast_at_coords(_lat, _lon)
    forecast_cords = fc.get_forecast()
    list_forecast = []
    for weather in forecast_cords.get_weathers():
        obj = {
            "reference_time": weather.get_reference_time(timeformat="iso"),
            "cloud_coverage": weather.get_clouds(),
            "rain_volume": weather.get_rain(),
            "snow_volume": weather.get_snow(),
            "wind": weather.get_wind(),
            "temperature": weather.get_temperature(unit='celsius'),
            "weather_status": weather.get_detailed_status(),
            "sunset_time": weather.get_sunset_time('iso')
        }
        list_forecast.append(obj)
    return list_forecast


# print(get_weather_for_5_days('Fribourg, CH'))

print(get_weather_for_5_days_lat_lon(lat, lon))
