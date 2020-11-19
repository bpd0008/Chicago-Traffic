from flask import Flask, render_template, request
from flask_googlemaps import GoogleMaps, Map, icons
from geopy.geocoders import Nominatim
from config import MAP_API_KEY
import requests
app = Flask(__name__)
GoogleMaps(app, key= MAP_API_KEY
)

@app.route("/")
def map_created_in_view():

    gmap = Map(
        identifier="gmap",
        varname="gmap",
        lat=42.8,
        lng=-87.6,
        zoom=12,
        markers={
            icons.dots.green: [(41.8, -87.6), (41.8, -87.92)],
            icons.dots.blue: [(41.85, -87.89, "Lat: 41.85, Long: -97.89")],
        },
        style="height:400px;width:600px;margin:0;",
    )

    return render_template("index.html", form=form, gmap=gmap)

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
        geolocator = Nominatim(user_agent="Chicago-Traffic")
        start_location = geolocator.geocode(form_data["start_address"])
        start_lat = start_location.latitude
        start_long = start_location.longitude
        end_location = geolocator.geocode(form_data["end_address"])
        
        return render_template('data.html',form=form, form_data = form_data, start_location=start_location,
                               end_location=end_location, start_long=start_long, start_lat=start_lat)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)