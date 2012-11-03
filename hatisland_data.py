import re
import urllib2 
from datetime import datetime

'''
LOOK OUT!
This script currently accesses the datapoints in the wrong order.
This is being fixed.
'''

def get_data():
    hatisland_data = {}
    
    date = datetime.now()

    response = urllib2.urlopen('http://mesowest.utah.edu/cgi-bin/droman/meso_download_mesowest_ndb.cgi?product=&stn=HATUT&unit=0&time=LOCAL&daycalendar=1&day1=' + str(date.day) + '&month1=' + str(date.month) +'&year1=' + str(date.year) +'&hour1=' + str(date.hour) + '&hours=24&output=csv&order=1&TMPF=TMPF&GUST=GUST&DRCT=DRCT&SKNT=SKNT')

    htmlText = response.read()
    html = re.split('[\\r\\n]{1,2}', htmlText)

    csvStart = 0
    csvEnd = 0

    for lineNo, line in enumerate(html):
        if "<PRE>" in line:
            csvStart = lineNo + 3
            while ",," in html[csvStart] and csvStart < len(html):
                csvStart += 1

        if "</PRE>" in line:
            csvEnd = lineNo

    html = html[csvStart:csvEnd]
    
    if len(html) < 1:
        # OMG GO NUTS
        return None
    
    
    currentData = re.split(',', html[0])
    hatisland_data['temp_f'] = float(currentData[6])
    hatisland_data['temp_c'] = celsiusify( float(currentData[6]) )
    hatisland_data['wind_speed'] = float(currentData[9])
    hatisland_data['wind_direction'] = meaningful_direction( float(currentData[8]) )
    hatisland_data['gust'] = float(currentData[7])
    # Add last (current) time
    
    high_temp_f = hatisland_data['temp_f']
    low_temp_f = high_temp_f
    high_gust = hatisland_data['gust']
    
    # Calc. Maxima/Minima:
    for csv_entry in html[1:]:
        data = re.split(',', csv_entry)
        thisTemp = data[6]
        
        # Inefficient. That's OK.
        high_temp_f = happy_max(high_temp_f, thisTemp)
        low_temp_f = happy_min(low_temp_f, thisTemp)
        high_gust = happy_max(high_gust, data[7])
        
    high_temp_c = celsiusify(high_temp_f)
    low_temp_c = celsiusify(low_temp_f)
    
    hatisland_data['high_temp_f'] = high_temp_f
    hatisland_data['low_temp_f'] = low_temp_f
    hatisland_data['high_temp_c'] = high_temp_c
    hatisland_data['low_temp_c'] = low_temp_c
    hatisland_data['high_gust'] = high_gust
    
    return hatisland_data

# dictionary = {"month": int(data[0]), "day": int(data[1]), "year": int(data[2]), "hour": int(data[3]), "minute": int(data[4]), "temp": float(data[6]), "gust": float(data[7]), "wind_direction": float(data[8])}

def happy_max(current, test_str):
    # happy because it doesn't complain if you give it erroneous values.
    test_num = 0
    try:
        test_num = float(test_str)
    except ValueError:
        return current
    return max(current, test_num)
    
    
def happy_min(current, test_str):
    test_num = 0
    try:
        test_num = float(test_str)
    except ValueError:
        return current
    return min(current, test_num)


def celsiusify(fahrenVal):
    return (fahrenVal - 32) * (5 / 9)


wind_directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']

def meaningful_direction(wind_degrees):
    adjusted_degrees = (wind_degrees + 11.25) % 360
    direction_index = int(adjusted_degrees / 16)
    return wind_directions[direction_index]
