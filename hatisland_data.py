import re
import urllib2 
import csv
from datetime import datetime

'''
LOOK OUT!
This script currently accesses the datapoints in the wrong order.
This is being fixed.

authors: Zach, Talis, Michael, Adair, Derek
'''

def get_data():
    hatisland_data = {}
    
    date = datetime.now()

    response = urllib2.urlopen('http://mesowest.utah.edu/cgi-bin/droman/meso_download_mesowest_ndb.cgi?product=&stn=HATUT&unit=0&time=LOCAL&daycalendar=1&day1=' + str(date.day) + '&month1=' + str(date.month) +'&year1=' + str(date.year) +'&hour1=' + str(date.hour) + '&hours=24&output=csv&order=1&TMPF=TMPF&GUST=GUST&DRCT=DRCT&SKNT=SKNT')

    htmlText = response.read()
    html = re.split('[\\r\\n]{1,2}', htmlText)

    csvStart = 0
    csv_text = []
    for lineNo, line in enumerate(html):
        if "PARM = " in line:
            csvStart = lineNo + 1
            csv_text.append(line[7:])
            while "</PRE>" not in html[csvStart] and csvStart < len(html):
                if len(html[csvStart]) > 0 and ",," not in html[csvStart]:
                    csv_text.append(html[csvStart])
                csvStart += 1

    if len(csv_text) < 2:
        # OMG GO NUTS
        return None
    
    
    param = re.split(',', csv_text[0])
    temp_f_idx = param.index('TMPF')
    wind_idx = param.index('SKNT')
    gust_idx = param.index('GUST')
    drct_idx = param.index('DRCT')

    
    latest_data = re.split(',',csv_text[1])
    hatisland_data['temp_f'] = float(latest_data[temp_f_idx])
    hatisland_data['temp_c'] = celsiusify( float(latest_data[temp_f_idx]) )
    hatisland_data['wind_speed'] = float(latest_data[wind_idx])
    hatisland_data['wind_direction'] = meaningful_direction( float(latest_data[drct_idx]) )
    hatisland_data['gust'] = float(latest_data[gust_idx])
    # Add last (current) time
    
    high_temp_f = hatisland_data['temp_f']
    low_temp_f = high_temp_f
    high_gust = hatisland_data['gust']
    
    # Calc. Maxima/Minima:
    for csv_entry in csv_text[1:]:
        data = re.split(',', csv_entry)
        thisTemp = data[temp_f_idx]
        
        # Inefficient. That's OK.
        high_temp_f = happy_max(high_temp_f, thisTemp)
        low_temp_f = happy_min(low_temp_f, thisTemp)
        high_gust = happy_max(high_gust, data[gust_idx])
        
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
    direction_index = int(adjusted_degrees / 22.5)
    return wind_directions[direction_index]

print "makeshift main"
get_data()

