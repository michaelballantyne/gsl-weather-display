import urllib2, json, re
from math import ceil
from abstractdata import DataProvider

class LevelDataProvider(DataProvider):
    def get_key(self):
        return "leveldata"

    def download_latest_data(self):
        result = []
        # 10010000 is saltair, 10010100 is saline
        for site in ["10010000", "10010100"]:
            result.append(urllib2.urlopen("http://waterdata.usgs.gov/nwis/uv?cb_72020=on&format=rdb&period=%d&begin_date=&end_date=&site_no=%s" % (119, site)))

        return result

    def process_data(self, datafiles):
        result = {}
        sites_data = {"saltair": self.get_levels_site_series(datafiles[0]),
                "saline": self.get_levels_site_series(datafiles[1])}

        # Find dates for which we have data for both sites.
        common_dates = sorted(reduce(lambda s, t: s.intersection(t), (set(site_data.keys()) for site_data in sites_data.values())))
        
        # Should have 96 entries per day x 119 days = about 11424 entries.
        # But sometimes we don't have that much. Fail if it seems like we're missing
        # way too much for things to be working correctly.
        if len(common_dates) < 5000:
            raise Exception("too few results: %d" % len(result))

        result["graphjson"] = self.get_levels_json(sites_data, common_dates)
        
        # Dates are sorted in ascending order, so common_dates[-1] should be the most recent.
        result["current_saline"] = str(sites_data["saline"][common_dates[-1]])
        result["current_saltair"] = str(sites_data["saltair"][common_dates[-1]])

        return result
    
    
    # Return a list of num evenly spaced elements of sequence.
    def takespread(self, sequence, num):
        result = []
        length = float(len(sequence))
        for i in range(num):
            result.append( sequence[int(ceil(i * length / num))])

        return result

    # Parse the datafile and return a dictionary from date to level.
    def get_levels_site_series(self, f):
        result = {}

        # Data ines begin with agency name of USGS
        data_line_matcher = re.compile("^USGS")

        for line in f:
            if data_line_matcher.match(line):
                row = line.split('\t')
                # Column 3 is datetime, column 5 is the elevation value.
                result[row[2]] = float(row[4])

        return result

    # Given raw data, select the data to provide the client
    def get_levels_json(self, sites_data, common_dates):
        result_data = {}
        for site in sites_data.keys():
            # Send the client 1000 evenly spaced values
            result_data[site] = self.takespread([sites_data[site][date] for date in common_dates], 1000)

        result_data["start_value"] = min(min(site_data) for site_data in result_data.values()) - 1
        
        labels = sorted(set(date.split()[0] for date in common_dates))

        # Send the client 5 evenly spaced date values to use for x axis labels.
        result_data["labels"] = [x for x in self.takespread(labels, 5)]

        return json.dumps(result_data)
