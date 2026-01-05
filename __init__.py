from flask import Flask, render_template, jsonify
from flask import json
from urllib.request import urlopen
from datetime import datetime


app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("hello.html")

@app.route('/contact/')
def MaPremiereAPI():
    return render_template("contact.html")

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))

    results = []

    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')

        temp_k = list_element.get('main', {}).get('temp')
        if temp_k is None:
            continue  # on saute cet élément s'il n'y a pas de température

        temp_day_value = temp_k - 273.15  # Kelvin -> °C

        results.append({
            'Jour': dt_value,
            'temp': temp_day_value
        })

    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

@app.route('/commits-api/')
def commits_api():
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    raw = urlopen(url).read()
    commits = json.loads(raw.decode('utf-8'))

    results = []
    for c in commits:
        date_str = c['commit']['author']['date']
        date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        minute = date_obj.strftime("%H:%M")
        results.append({"minute": minute})

    return jsonify(results=results)


@app.route('/commits/')
def commits_graph():
    return render_template("commits.html")



if __name__ == "__main__":
    app.run(debug=True)
