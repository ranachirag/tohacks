import requests
from functools import partial
import pyproj
from shapely.ops import transform
from shapely.geometry import Point


api = "AIzaSyA598cf-Rj1uh07ZZwLxFwkipQQJj8NUAE"
# address = input("Please enter your current location/ address: ")
# radius = int(input("How far are you willing to travel (radius in km)?: "))
address = '177 Linus Rd'
radius = 2
geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?address={}".format(address)
geocode_url = geocode_url + "&key={}".format(api)
results = requests.get(geocode_url)
results = results.json()

# if there's no results or an error, return empty results.
if len(results['results']) == 0:
    output = {
        "formatted_address": None,
        "latitude": None,
        "longitude": None,
        "accuracy": None,
        "google_place_id": None,
        "type": None,
        "postcode": None
    }
else:
    answer = results['results'][0]
    output = {
        "formatted_address": answer.get('formatted_address'),
        "latitude": answer.get('geometry').get('location').get('lat'),
        "longitude": answer.get('geometry').get('location').get('lng'),
        "accuracy": answer.get('geometry').get('location_type'),
        "google_place_id": answer.get("place_id"),
        "type": ",".join(answer.get('types')),
        "postcode": ",".join([x['long_name'] for x in answer.get('address_components')
                              if 'postal_code' in x.get('types')])
    }

# Append some other details:
output['input_string'] = address
output['number_of_results'] = len(results['results'])
output['status'] = results.get('status')
output['response'] = results

proj_wgs84 = pyproj.Proj('init='+'EPSG:'+'4326')
lat = output["latitude"]
lon = output["longitude"]
print(lat, lon)

aeqd_proj = '+proj=aeqd +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0'
project = partial(
    pyproj.transform,
    pyproj.Proj(aeqd_proj.format(lat=lat, lon=lon)),
    proj_wgs84)
buf = Point(0, 0).buffer(radius * 1000)  # distance in metres
coords = transform(project, buf).exterior.coords[:]
latitudes = []
longitudes = []
if coords is not None:
    for items in coords:
        latitudes.append(items[1])
        longitudes.append(items[0])
topleft = (max(latitudes), min(longitudes))
bottomright = (min(latitudes), max(longitudes))
print(topleft, bottomright)
