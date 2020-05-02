import populartimes
import flask

api = "AIzaSyAZVCDDCb9VzLNby3OpH9U_B-VUZ6NNy0I"
user_input = "bar"
lat = (43.750126, -79.639509,)
long = (43.723822, -79.055455,)
id = populartimes.get(api, [user_input], lat, long)


