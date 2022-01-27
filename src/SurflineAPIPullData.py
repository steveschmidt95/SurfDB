
import requests, json, csv, datetime, copy, pandas
# from pyowm.owm import OWM
from dateutil import parser
seabrookSpotId = '5842041f4e65fad6a770884a'
testSpotId = '58581a836630e24c44878fd4'
SBSID = seabrookSpotId
# class surfForecast:
#     def __init__(self):
        

# class weatherForecast:
# class dayForecast:

def weather_API_call(latitude, longitude):
    getGridCoordinatesURL = 'https://api.weather.gov/points/' + str(latitude) + ',' + str(longitude)
    weatherGridResponseJSON = requests.get(getGridCoordinatesURL,timeout=2)
    weatherGridResponseJSON = weatherGridResponseJSON.json()
    
    weatherForecastJSON = requests.get(weatherGridResponseJSON['properties']['forecastGridData'])
    weatherForecast = weatherForecastJSON.json()
    # owm = OWM('0460e464f35ad7c355e4ff18b87d15cc')
    # mgr = owm.weather_manager()
    # weatherForecast = mgr.one_call(lat=latitude, lon=longitude)
    
    return weatherForecast, weatherGridResponseJSON
def convert_iso_to_timestamp(iso_time):
    # NWS ISO8601 timestamps come in the form YYYY-MM-DDTHH:MM:SS followed by 
    #  a '+' and a bunch of other shit, so we split off the important stuff and
    # convert to epoch timestamp for easy increment
    
    iso_time = iso_time.split("+")[0] 
    epoch_timestamp = int(datetime.datetime.strptime(iso_time, '%Y-%m-%dT%H:%M:%S').timestamp())
    return epoch_timestamp

def reformat_weather_forecast_dicts(weather_forecast_list):
    weather_forecast_dict = {}
    weather_forecast_dict['data'] = {}
    for forecast_point in weather_forecast_list:
        unix_time = convert_iso_to_timestamp(forecast_point['validTime'])
        weather_forecast_dict['data'][unix_time] = forecast_point['value']
    return weather_forecast_dict

def weather_forecast_manager(weather_forecast_dict):
    #these are all lists of forecast points
    wind_dir_dict = reformat_weather_forecast_dicts(weather_forecast_dict['properties']['windDirection']['values'])
    wind_spd_dict = reformat_weather_forecast_dicts(weather_forecast_dict['properties']['windSpeed']['values'])
    wind_gust_dict = reformat_weather_forecast_dicts(weather_forecast_dict['properties']['windGust']['values'])
    temp_dict = reformat_weather_forecast_dicts(weather_forecast_dict['properties']['temperature']['values'])
    
    wind_dir_dict['name'] = 'Wind Direction'
    wind_spd_dict['name'] = 'Wind Speed'
    wind_gust_dict['name'] = 'Wind Gust'
    temp_dict['name'] = 'Temperature'
    list_of_dicts = [wind_dir_dict, wind_spd_dict, wind_gust_dict, temp_dict]
    master_dict_keys = {}
    for forecast_dict in list_of_dicts:
        keys_to_add = forecast_dict['data'].keys()
        arbitrary_vals = [1]*len(keys_to_add)
        master_dict_keys.update(dict(zip(keys_to_add,arbitrary_vals)))
    master_keys_list = [*range(min(master_dict_keys.keys()), max(master_dict_keys.keys()), 3600)]
    for forecast_dict in list_of_dicts:
        i = 0
        for timestamp in master_keys_list:
            i += 1
            if timestamp in forecast_dict['data'].keys():
                previous_forecast_value = forecast_dict['data'][timestamp]
            # elif timestamp not in forecast_dict['data'].keys() and i == 1:
            #     forecast_dict['data'][timestamp] = previous_forecast_value
            elif timestamp not in forecast_dict.keys():
                forecast_dict['data'][timestamp] = previous_forecast_value
    return list_of_dicts
# def addin_missing_forecast_points(orig_list_dict):
#     # NWS only gives data points when the forecast changes, ie if its 7°C at 3AM 
#     #  and doesn't change for 6 hours, the next data point will be 9am. This unfortunately doesn't
#     #  vibe well with a forecast point for every hour in the surf forecast. This function accepts
#     #  the (individual) lists from the NWS returned dict for windSpeed, windGust, windDirection, temperature, 
#     #  and probably other dicts, changes the time to epoch time, and fills in the gaps between forecast hours
#     #  returning a dictionary with epoch_timestamp:value pairs for every hour over the whole range forecasted
    
#     full_forecast_dict = {}
#     time_list = []
    
#     for i in orig_list_dict:
#         epoch_time = convert_iso_to_timestamp(i['validTime'])  #custom function call
#         time_list.append(epoch_time)
#         # time_list.append(i['validTime'])
#         full_forecast_dict[epoch_time] = i['value']
    
#     time_list.sort()
#     forecast_end_time = time_list[-1]
#     for idx, floor_time in enumerate(time_list):
#         if floor_time != forecast_end_time:
#             ceiling_time = time_list[idx+1]
#             insert_time = floor_time + 3600
#             while insert_time<ceiling_time:
#                 full_forecast_dict[insert_time] = full_forecast_dict[floor_time]
#                 insert_time += 3600
#     return full_forecast_dict
        
# def add_forecast_times_to_end(end_timestamp, forecast_dict):
#     #Inputs:
#         #end_timestamp(int): unix timestamp as an integer - supplied by determining the max
#         # timestamp (latest forecast time) for all of the weather forecasts
        
#         #forecast_dict(dict): forecast dictionary for ea. aspect (temp, windspeed, etc)) 
#         # formatted as {timestamp(int):value}
#     # Description:
#         #Due to the same issue with how NWS only reports weather when it changes on the hour,
#          # not all forecasts end on the same time point (ie wind ends at 17:00 and temp might end @ 23:00)
#          # this function takes the max time (unix) of all of the reported forecasts and then brings
#          # all of the other forecast lists up to this timestamp by replicating the forecast for the last
#          # timestamp until this new max timestamp
#     if end_timestamp not in forecast_dict.keys():
#         last_value = forecast_dict[max(forecast_dict.keys())]
#         forecast_dict.update(dict(zip([*range(max(forecast_dict.keys()), end_timestamp, 3600)]
#                                       ,[last_value]*(end_timestamp-max(forecast_dict.keys()))/3600)))
#         print(last_value)
#         # for time_to_add in range(max(forecast_dict.keys()), end_timestamp, 3600): #for every hour from current end to end_timestamp
#         #     forecast_dict[time_to_add] = last_value
#     return forecast_dict

# def unify_forecast_dict_ranges(weather_forecast):
#     wind_gust = weather_forecast['wind_gust']
#     wind_direction = weather_forecast['wind_direction']
#     wind_speed = weather_forecast['wind_speed']
#     temperature = weather_forecast['temperature']
#     end_timestamp = max(max(wind_gust.keys()), max(wind_direction.keys()), max(wind_speed.keys()))
#     weather_forecast['wind_gust'] = add_forecast_times_to_end(end_timestamp,wind_gust)
#     weather_forecast['wind_direction'] = add_forecast_times_to_end(end_timestamp,wind_direction)
#     weather_forecast['wind_speed'] = add_forecast_times_to_end(end_timestamp,wind_speed)
#     weather_forecast['temperature'] = add_forecast_times_to_end(end_timestamp,temperature)
    
#     return weather_forecast

# def weather_data_manager(weather_forecast):
#     wind_direction = weather_forecast['properties']['windDirection']['values']
#     wind_speed = weather_forecast['properties']['windSpeed']['values']
#     wind_gust = weather_forecast['properties']['windGust']['values']
    
#     wind_direction = addin_missing_forecast_points(wind_direction)
#     wind_speed = addin_missing_forecast_points(wind_speed)
#     wind_gust = addin_missing_forecast_points(wind_gust)
    

#     weather_forecast['properties']['windDirection'] = wind_direction
#     weather_forecast['properties']['windSpeed'] = wind_speed
#     weather_forecast['properties']['windGust'] = wind_gust
    
#     return weather_forecast
    
    
    
def surfline_wave_API_call(spot_ID,days=6,interval_hours=6,max_heights='false',access_token=None):
    #spot_id (str) - Can get this from the taxonomy API
    #days (int) - Greater than 1 and less than 6 (unless logged in)
    #interval_hours(int) - used only in wave forecast - determines # of hrs a forecast block is
    #accessToken (str) - Allows gathering data for more than 6 days out
    
    #Description:
        #Makes a call to surfline API for both wave forecast & tide. Right now, this function really only
        # accepts the provisioned spot_ID taken from their internal identification system and the days and
        # interval_hours arguments creates a URL, requests it, and then parses JSON into dict.
    days = str(days)
    interval_hours = str(interval_hours)
    
    base_wave_surfline_URL = 'https://services.surfline.com/kbyg/spots/forecasts/wave'
    base_tide_surfline_URL = 'https://services.surfline.com/kbyg/spots/forecasts/tides?'
    
    surfline_wave_request_URL = base_wave_surfline_URL + '?' 
    surfline_wave_request_URL = surfline_wave_request_URL +'spotId=' + spot_ID 
    surfline_wave_request_URL = surfline_wave_request_URL + '&' + 'days=' + days
    surfline_wave_request_URL = surfline_wave_request_URL + '&' +'intervalHours=' + interval_hours
    surfline_wave_request_URL = surfline_wave_request_URL + '&' + 'maxHeights=' + max_heights
    surfline_wave_response_JSON = requests.get(surfline_wave_request_URL)
    surf_forecast = surfline_wave_response_JSON.json()
    
    surfline_tide_request_URL = base_tide_surfline_URL
    surfline_tide_request_URL = surfline_tide_request_URL + 'spotId=' + spot_ID 
    surfline_tide_request_URL = surfline_tide_request_URL + '&' + 'days=' + days
    surflineTideResponseJSON = requests.get(surfline_tide_request_URL)
    tideForecast = surflineTideResponseJSON.json()
    return surf_forecast, tideForecast

def headerGeneration():
    swellHeader = []
    headers = ['generation_date', 'generation_hour', 'forecast_date', 'forecast_hour', 'tide_height', 
               'surf_min', 'surf_max', 'surf_optimal_score', 'wind_direction', 'wind_speed', 'wind_gust', 'temperature']
    for i in range(1,7):
        swellNumber = 'swell_' + str(i)
        swellHeight = swellNumber + '_height'
        swellDirection = swellNumber + '_direction'
        swellMinDirection = swellNumber + '_swell_min_direction'
        swellPeriod = swellNumber + '_period'
        swellOptimalScore = swellNumber + '_optimal_score'
        swellHeader = swellHeader + [swellHeight,swellDirection,swellMinDirection,swellPeriod,swellOptimalScore]
    headers = headers + swellHeader
    return headers

def extract_weather_data_for_timestamp(weather_forecast_dict_list, timestamp):
    weather_datapoints = []
    for forecast_dict in weather_forecast_dict_list:
        weather_datapoint = forecast_dict['data'][timestamp]
        weather_datapoints.append(weather_datapoint)
    return weather_datapoints









headers = headerGeneration()
seabrookForecast,tideForecast = surfline_wave_API_call(seabrookSpotId, 6, 3)
longitude = seabrookForecast['associated']['location']['lon']
latitude = seabrookForecast['associated']['location']['lat']
longitude = -70.936249
latitude = 42.424770
weatherForecast, weatherGridResponse = weather_API_call(latitude,longitude)
weather_forecast_list = weather_forecast_manager(weatherForecast)

tideTimeStampList = []
tideHeightList=[]
for i in tideForecast['data']['tides']:
    # print(datetime.datetime.fromtimestamp(i['timestamp']))
    tideTimeStampList = tideTimeStampList + [i['timestamp']] #extract a list of timestamps from the tide dictionary
    
    tideHeightList = tideHeightList + [i['height']]
    
    
    
with open('sampledata.txt', 'w', newline='') as csvfile: 
    datawriter = csv.writer(csvfile, quotechar='|', quoting=csv.QUOTE_MINIMAL)
    datawriter.writerow(headers)
    surfdatalist = []
    today = datetime.datetime.now()
    generationDateString = today.strftime('%m-%d-%Y')
    previousTideHeight = -1
    for surfdatapoint in seabrookForecast['data']['wave']:
        if surfdatapoint['timestamp'] >= today.timestamp():
            if surfdatapoint['timestamp'] in tideTimeStampList:
                tideIndex = tideTimeStampList.index(surfdatapoint['timestamp'])
                tideHeight = tideForecast['data']['tides'][tideIndex]['height']
                previousTideHeight = tideHeight
            else:
                tideHeight = previousTideHeight
            [wind_dir, wind_spd, wind_gust, temperature] = extract_weather_data_for_timestamp(weather_forecast_list,surfdatapoint['timestamp'])
            forecastDate = datetime.datetime.fromtimestamp(surfdatapoint['timestamp'])
            forecastDateString = forecastDate.strftime('%m-%d-%Y')
            surfdatalist = [generationDateString,
                            today.hour,
                            forecastDateString,
                            forecastDate.hour,
                            tideHeight,
                            surfdatapoint['surf']['min'],
                            surfdatapoint['surf']['max'], 
                            surfdatapoint['surf']['optimalScore'],
                            wind_dir,
                            wind_spd,
                            wind_gust,
                            temperature]
            for swell in surfdatapoint['swells']:
                surfdatalist = surfdatalist + [swell['height']]
                surfdatalist = surfdatalist + [swell['direction']]
                surfdatalist = surfdatalist + [swell['directionMin']]
                surfdatalist = surfdatalist + [swell['period']]
                surfdatalist = surfdatalist + [swell['optimalScore']]
            
            datawriter.writerow(surfdatalist)
    
