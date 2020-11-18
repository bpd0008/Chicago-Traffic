from flask import Flask, render_template, request
from flask_googlemaps import GoogleMaps, Map, icons
import requests
from config import API_KEY
api_key = "API_Key"
app = Flask(__name__)
GoogleMaps(app, key= API_KEY
)
@app.route("/")
def map_created_in_view():
    gmap = Map(
        identifier="gmap",
        varname="gmap",
        lat=41.8,
        lng=-87.6,
        markers={
            icons.dots.green: [(41.8, -87.6), (41.8, -87.92)],
            icons.dots.blue: [(41.85, -87.89, "Lat: 41.85, Long: -97.89")],
        },
        zoom=15,
        style="height:400px;width:600px;margin:0;",
    )
    return render_template("example.html", form=form, gmap=gmap)
@app.route('/form')
def form():
    return render_template('form.html', form=form)
@app.route("/data", methods=["POST", "GET"])
def postdata():
    # Now lat and lon can be accessed as:
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form
        return render_template('data.html',form=form, form_data = form_data)
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)