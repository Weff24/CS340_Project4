import maxminddb

def get_loc_scan(ips):
    locations = set()
    for ip in ips:
        country = None
        province = None
        city = None

        reader = maxminddb.open_database('GeoLite2-City.mmdb')
        loc = reader.get(ip)

        if loc is not None:
            if "country" in loc.keys() and "names" in loc["country"].keys() and "en" in loc["country"]["names"]:
                country = loc["country"]["names"]["en"]
            if "subdivisions" in loc.keys() and len(loc["subdivisions"]) > 0 and "names" in loc["subdivisions"][0].keys() and "en" in loc["subdivisions"][0]["names"]:
                province = loc["subdivisions"][0]["names"]["en"]
            if "city" in loc.keys() and "names" in loc["city"].keys() and "en" in loc["city"]["names"]:
                city = loc["city"]["names"]["en"]

            if country and province and city:
                locations.add(city + ", " + province + ", " + country)
    return list(locations)
