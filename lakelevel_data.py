import urllib2, json, re
from math import ceil

def takespread(sequence, num):
    result = []
    length = float(len(sequence))
    for i in range(num):
        result.append( sequence[int(ceil(i * length / num))])

    return result

def get_levels_site_series(site, days=119):
    f = urllib2.urlopen("http://waterdata.usgs.gov/nwis/uv?cb_72020=on&format=rdb&period=%d&begin_date=&end_date=&site_no=%s" % (days, site))

    result = {}

    data_line_matcher = re.compile("^USGS")

    for line in f:
        if data_line_matcher.match(line):
            row = line.split('\t')
            result[row[2]] = float(row[4])

    return result

def get_levels_json(sites_data):

    common_dates = sorted(reduce(lambda s, t: s.intersection(t), (set(site_data.keys()) for site_data in sites_data.values())))

    result_data = {}
    for site in sites_data.keys():
        result_data[site] = takespread([sites_data[site][date] for date in common_dates], 3000)

    result_data["start_value"] = min(min(site_data) for site_data in result_data.values()) - 1
    
    labels = sorted(set(date.split()[0] for date in common_dates))

    result_data["labels"] = [x for x in takespread(labels, 7)]

    return json.dumps(result_data)

def get_data():
    result = {}
    sites_data = {"saltair": get_levels_site_series("10010000"),
            "saline": get_levels_site_series("10010100")}

    result["graphjson"] = get_levels_json(sites_data)

    return result
