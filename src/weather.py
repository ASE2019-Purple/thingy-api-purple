# Created by Narek at 08.12.2019

# Feature: # Get weather inforamtion
# Enter feature description here

# Scenario: # get the weather and forecast weather
# Enter steps here
import pyowm
from pyowm.commons import http_client
from pyowm.utils import geo
from pyowm.weatherapi25 import forecaster, forecast
from pyowm.weatherapi25.configuration25 import THREE_HOURS_FORECAST_URL

from pyowm import OWM


API_KEY = '8074bee2618edf62080549a071a19914'
owm = OWM(API_key=API_KEY, language='en')

FribourgId = 2660718

test = owm.three_hours_forecast_at_coords(47.9959, 7.85222)

f = owm.three_hours_forecast('London')
print("three ours forcast", f)

print("three_hours_forecast_at_coords ", test)

CityWeather = owm.weather_at_id(FribourgId)

print("Friborug Weather", CityWeather)

CityFc = owm.three_hours_forecast_at_id(FribourgId)
CityF = CityFc.get_forecast()
weatherList = CityF.get_weathers()
threeHours = 3 * 60 * 60
newWeatherList = []
time = CityFc.when_starts()
interval = CityF.get_interval()
reception_time = CityF.get_reception_time(timeformat='unix')
location = CityF.get_location()

for i in range(0, 2):
    newWeatherList.append(CityFc.get_weather_at(time + threeHours * i))
    print(newWeatherList)

FribourgF = forecast.Forecast(interval, reception_time, location, newWeatherList)
FribourgFc = forecaster.Forecaster(FribourgF)

print(FribourgFc)

# Fribourg city ID 2660718

# test = three_hours_forecast_at_coords(self= ,47.9959, 7.85222)


# Search for current weather in London (Great Britain)
observation = owm.weather_at_place('Fribourg,CH')
w = observation.get_weather()
print("Print weather", w)                      # <Weather - reference time=2013-12-18 09:20,
                              # status=Clouds>

# Weather details
w.get_wind()                  # {'speed': 4.6, 'deg': 330}
w.get_humidity()              # 87
w.get_temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}

# Search current weather observations in the surroundings of Fribourg

observation_list = owm.weather_around_coords(46.803, 7.1513)

print("Obervation LIST", observation_list)


