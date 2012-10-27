import re
import urllib2 
from datetime import datetime

#This script returns example data followed by var name
def hatIslandData():
  
  date = datetime.now()

  response = urllib2.urlopen('http://mesowest.utah.edu/cgi-bin/droman/meso_download_mesowest_ndb.cgi?product=&stn=HATUT&unit=0&time=LOCAL&daycalendar=1&day1=' + str(date.day) + '&month1=' + str(date.month) +'&year1=' + str(date.year) +'&hour1=' + str(date.hour) + '&hours=24&output=csv&order=1&TMPF=TMPF&GUST=GUST&DRCT=DRCT')
  htmlText = response.read()
  html = re.split('[\\r\\n]{1,2}', htmlText)

  csvStart = 0
  csvEnd = 0

  for lineNo, line in enumerate(html):
    if "<PRE>" in line:
      csvStart = lineNo +3

    if "</PRE>" in line:
      csvEnd = lineNo
  html = html[csvStart:csvEnd]
  final_list = []
  for csv_entry in html:
    data = re.split(',', csv_entry)
    dictionary = { "month":data[0], "day":data[1], "year":data[2], "hour":data[3], "minute":data[4], "temp":data[6], "gust":data[7], "wind_direction":data[8]}
    final_list.append(dictionary)
  return final_list
