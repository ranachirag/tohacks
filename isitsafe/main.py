import populartimes, requests
from flask import Flask, request, render_template

api_key = "AIzaSyA598cf-Rj1uh07ZZwLxFwkipQQJj8NUAE"

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def homepage2():
    query = ''
    if request.method == 'POST':
        query = str(request.form.get('location'))

    # url variable store url
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

    r = requests.get(url + 'query=' + query +
                     '&key=' + api_key)

    x = r.json()

    y = x['results']
    data = {}
    data['name'] = []
    data['address'] = []
    data['current_popularity'] = []
    data['rating'] = []

    for i in range(len(y)):
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


    return render_template("my-form.html", message=data, len=len(y))


if __name__ == '__main__':
    app.run(debug=True)
