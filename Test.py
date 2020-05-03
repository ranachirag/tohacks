import populartimes, requests
from flask import Flask, request, render_template

api_key = "AIzaSyAZVCDDCb9VzLNby3OpH9U_B-VUZ6NNy0I"
# user_input = "bar"
# lat = (43.750126, -79.639509,)
# long = (43.723822, -79.055455,)
# id = populartimes.get(api, [user_input], lat, long)

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def homepage2():
    query = ''
    if request.method == 'POST':
        query = str(request.form.get('location'))

    # url variable store url
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

    # The text string on which to search
    # query = input('Search query: ')

    # get method of requests module
    # return response object
    r = requests.get(url + 'query=' + query +
                     '&key=' + api_key)

    # json method of response object convert
    #  json format data into python format data
    x = r.json()

    # now x contains list of nested dictionaries
    # we know dictionary contain key value pair
    # store the value of result key in variable y
    y = x['results']
    data = {}
    data['name'] = []
    data['address'] = []
    data['current_popularity'] = []
    data['rating'] = []
    # keep looping upto length of y
    for i in range(len(y)):

        # Print value corresponding to the
        # 'name' key at the ith index of y
        # print(y[i])
        f = populartimes.get_id(api_key, y[i]['reference'])
        if "name" in f.keys():
            data['name'].append(f['name'])
        else:
            data['name'].append('')
        if "address" in f.keys():
            data['address'].append(f['address'])
        else:
            data['address'].append('')
        if "current_popularity" in f.keys():
            data['current_popularity'].append(f['current_popularity'])
        else:
            data['current_popularity'].append('')
        if "rating" in f.keys():
            data['rating'].append(f['rating'])
        else:
            data['rating'].append('')


    return render_template("my-form.html", message=data)


if __name__ == '__main__':
    app.run(port=4998, debug=True, use_reloader=True)
