import fmi_weather_client as fmi
from fmi_weather_client.errors import ClientError, ServerError
import statsd
from statsd import StatsClient


try:
    weather = fmi.weather_by_place_name("Karhi, Hausjärvi")
    if weather is not None:
        #print(f"Temperature in {weather.place} is {weather.data.temperature}")
        #print(f"Pressure in {weather.place} is {weather.data.pressure}")
        pres_statd = StatsClient(host='localhost', port=8125, prefix='Pressure')
        pres_statd.gauge('FMI.karhi', weather.data.pressure[0])
        temp_statd = StatsClient(host='localhost', port=8125, prefix='Temperature')
        temp_statd.gauge('FMI.karhi', weather.data.temperature[0])
except ClientError as err:
    print(f"Client error with status {err.status_code}: {err.message}")
except ServerError as err:
    print(f"Server error with status {err.status_code}: {err.body}")
