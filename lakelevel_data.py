import urllib2, json, re
from math import ceil
from abstractdata import DataProvider

class LevelDataProvider(DataProvider):
    def get_key(self):
        return "leveldata"

    def download_latest_data(self):
        result = []
        for site in ["10010000", "10010100"]:
            result.append(urllib2.urlopen("http://waterdata.usgs.gov/nwis/uv?cb_72020=on&format=rdb&period=%d&begin_date=&end_date=&site_no=%s" % (119, site)))

        return result

    def process_data(self, datafiles):
        result = {}
        sites_data = {"saltair": self.get_levels_site_series(datafiles[0]),
                "saline": self.get_levels_site_series(datafiles[1])}

        common_dates = sorted(reduce(lambda s, t: s.intersection(t), (set(site_data.keys()) for site_data in sites_data.values())))

        result["graphjson"] = self.get_levels_json(sites_data, common_dates)
        
        result["current_saline"] = str(sites_data["saline"][common_dates[-1]])
        result["current_saltair"] = str(sites_data["saltair"][common_dates[-1]])

        return result
    
    
    def takespread(self, sequence, num):
        result = []
        length = float(len(sequence))
        for i in range(num):
            result.append( sequence[int(ceil(i * length / num))])

        return result

    def get_levels_site_series(self, f):
        result = {}

        data_line_matcher = re.compile("^USGS")

        for line in f:
            if data_line_matcher.match(line):
                row = line.split('\t')
                result[row[2]] = float(row[4])

        return result

    def get_levels_json(self, sites_data, common_dates):
        result_data = {}
        for site in sites_data.keys():
            result_data[site] = self.takespread([sites_data[site][date] for date in common_dates], 1000)

        result_data["start_value"] = min(min(site_data) for site_data in result_data.values()) - 1
        
        labels = sorted(set(date.split()[0] for date in common_dates))

        result_data["labels"] = [x for x in self.takespread(labels, 5)]

        return json.dumps(result_data)
