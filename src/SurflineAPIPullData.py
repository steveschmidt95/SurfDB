
import requests, json, csv, datetime, copy, pandas
from dateutil import parser


class ForecastConstants:
    SEABROOK_SPOT_ID = '5842041f4e65fad6a770884a'
    SBSID = SEABROOK_SPOT_ID
    SEABROOK_LATITUDE = 42.424770
    SEABROOK_LONGITUDE = -70.936249
    BASE_WEATHER_URL = 'https://api.weather.gov/points/'
    BASE_WAVE_SURFLINE_URL = 'https://services.surfline.com/kbyg/spots/forecasts/wave'
    BASE_TIDE_SURFLINE_URL = 'https://services.surfline.com/kbyg/spots/forecasts/tides?'

def weather_api_call(latitude = ForecastConstants.SEABROOK_LATITUDE, longitude = ForecastConstants.SEABROOK_LONGITUDE):
    
    """
    Description
    ----------
    This function primarily generates a weather forecast dictionary from the NWS API for a supplied latitude and longitude. It does this by first querying NWS grid URL for an endpoint corresponding to the supplied latitude,longitude pair and then calls the endpoint to return weather data in dictionary form.
    
    Parameters
    ----------
    latitude : float, optional
        The latitude of the desired weather forecast location. The default is ForeCast.SEABROOK_LATITUDE.
        
    longitude : float, optional
        The longitude of the desired weather forecast location. The default is SEABROOK_LONGITUDE.

    Returns
    -------
    weather_forecast_dict : dict
        This dictionary contains all of ther weather data for the requested location. Every weather parameter is stored in weather_forecast_dict['properties']
        
    weather_grid_dict : dict
        This dictionary containts mostly API endpoints for seeking weather info. Most relevant info is stored in weather_grid_dict['properties']
        
    """
    #build initial URL for grid data
    weather_grid_coordinates_url = ForecastConstants.BASE_WEATHER_URL + str(latitude) + ',' + str(longitude)
    #return grid data response and parse JSON into dict
    weather_grid_json = requests.get(weather_grid_coordinates_url,timeout=2)
    weather_grid_dict = weather_grid_json.json()
    
    #call weather data API endpoint from grid response and parse returned JSON into dict
    weather_forecast_json = requests.get(weather_grid_dict['properties']['forecastGridData'])
    weather_forecast_dict = weather_forecast_json.json()
    
    return weather_forecast_dict, weather_grid_dict


def convert_iso_to_timestamp(iso_time):
    """
    Description
    ----------
    This function converts a timestamp from ISO8601 (string) format to unix epoch timestamp format. It also extracts the duration information from the end
    
    Parameters
    ----------
    iso_time : str
        A string that is an ISO8601 timestamp
    Returns
    -------
    epoch_timestamp : int
        An integer that is a unix timestamp.

    """

    #Get the timestamp part
    iso_timestamp = iso_time.split("+")[0]
    epoch_timestamp = int(datetime.datetime.strptime(iso_timestamp, '%Y-%m-%dT%H:%M:%S').timestamp())
    
    
    #Get the duration part (number of hours forecast is good for, including listed hour timestamp)
    duration = int(iso_time.split("+")[1].split('T')[1][0])
    
    return epoch_timestamp, duration

def reformat_weather_forecast_dicts(weather_forecast_list):
    """
    Description
    ----------
    
    Parameters
    ----------
    weather_forecast_list : list
    A specific list within the default dict returned by weather api call. Each parameter in weather_forecast_dict['properties'] has a dict with the key:val pairs of uom(units of measure):str
    and also values:list. The values:list pair is a list of dicts containing an ISO8601 timestamp (w/ forecast in effect duration info) and the corresponding forecast

    Returns
    -------
    weather_forecast_dict : TYPE
        DESCRIPTION.

    """
    
    weather_forecast_dict = {}
    weather_forecast_dict['data'] = {}
    for forecast_point in weather_forecast_list:
        unix_time = convert_iso_to_timestamp(forecast_point['validTime'])
        weather_forecast_dict['data'][unix_time] = forecast_point['value']
    return weather_forecast_dict

def weather_forecast_manager(weather_forecast_dict):
    """
    Description
    ----------

    Parameters
    ----------
    weather_forecast_dict : TYPE
        DESCRIPTION.

    Returns
    -------
    list_of_dicts : TYPE
        DESCRIPTION.

    """
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
   
def surfline_wave_API_call(spot_ID,days=6,interval_hours=3,max_heights='false',access_token=None):
    
    """
    Description
    ----------
    This function makes a call to the surfline API with the supplied arguments and returns two dicts - 1. Surf forecast dictionary 2. Tide forecast dictionary
    Parameters
    ----------
    spot_ID : str
        A surfline specific string for a specified spot. Can be retreived from their taxonomy API
    days : int, optional
        An integer corresponding to the number of days of forecast requested. The default and max without Surfline Premium is 6.
    interval_hours : int, optional
        An integer for the number of hours in between forecasts. If set to 3, you'll have 8 forecasts per day. The default is 3.
    max_heights : string, optional
        I don't know what this is. I don't think Surfline knows what this is. The default is 'false'.
    access_token : str, optional
        Probably a string, for if you have a surfline premium account. Essentially an API key to get longer forecasts and such. The default is None.

    Returns
    -------
    surf_forecast : dict
        A dictionary that holds all of the relevant surf forecast data. Important info is held in the following structure:
            surf_forecast['data']['wave']
                List[0,days*24/interval_hours] of dicts for each interval hour
                    each dict{
                        surf -> dict of stats -> {min (float), max (float), optimalScore (int)}
                        swells -> list[0,N] of dicts of swells -> {direction (int), directionMin (int), height (int), optimalScore(int), period(int)}
                        timestamp -> unix timestamp (int)
                        }
                    
                    
    tideForecast : dict
        A dictionary that holds all of the relevant tide forecast data, basically a datapoint for every hour between now and now+days. Important info is held in the following structure:
            tide_forecast['data']['tides']
                list[0,N] of dicts for each hour in range containing these fields:
                    height -> float
                    timestamp -> int unix epoch
                    type -> str (low, normal, high)
                
    """
    #input handling to ensure strings for URL formulation
    days = str(days)
    interval_hours = str(interval_hours)
    
     
    surfline_wave_request_URL = ForecastConstants.BASE_WAVE_SURFLINE_URL + '?'
    surfline_wave_request_URL = surfline_wave_request_URL + 'spotId=' + spot_ID
    surfline_wave_request_URL = surfline_wave_request_URL + '&' + 'days=' + days
    surfline_wave_request_URL = surfline_wave_request_URL + \
        '&' + 'intervalHours=' + interval_hours
    surfline_wave_request_URL = surfline_wave_request_URL + \
        '&' + 'maxHeights=' + max_heights
    surfline_wave_response_JSON = requests.get(surfline_wave_request_URL)
    surf_forecast = surfline_wave_response_JSON.json()

    surfline_tide_request_URL = ForecastConstants.BASE_TIDE_SURFLINE_URL
    surfline_tide_request_URL = surfline_tide_request_URL + 'spotId=' + spot_ID
    surfline_tide_request_URL = surfline_tide_request_URL + '&' + 'days=' + days
    surflineTideResponseJSON = requests.get(surfline_tide_request_URL)
    tide_forecast = surflineTideResponseJSON.json()
    return surf_forecast, tide_forecast


def headerGeneration():
    """
    Description
    ----------
    This function builds the header for the forecast output csv 
    Returns
    -------
    headers : 
        DESCRIPTION.

    """
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
    """
    Description
    ----------

    Parameters
    ----------
    weather_forecast_dict_list : TYPE
        DESCRIPTION.
    timestamp : TYPE
        DESCRIPTION.

    Returns
    -------
    weather_datapoints : TYPE
        DESCRIPTION.

    """
    weather_datapoints = []
    for forecast_dict in weather_forecast_dict_list:
        weather_datapoint = forecast_dict['data'][timestamp]
        weather_datapoints.append(weather_datapoint)
    return weather_datapoints

# def build_forecast_output(spotID = ):
#     """
#     Description
#     ----------

#     Parameters
#     ----------
#     spotID : TYPE
#         DESCRIPTION.

#     Returns
#     -------
#     None.

#     """

headers = headerGeneration()
seabrookForecast,tideForecast = surfline_wave_API_call(ForecastConstants.SEABROOK_SPOT_ID, 6, 3)
longitude = seabrookForecast['associated']['location']['lon']
latitude = seabrookForecast['associated']['location']['lat']
weatherForecast, weatherGridResponse = weather_api_call(latitude,longitude)
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
    
