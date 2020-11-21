from flask import Flask, render_template, request, url_for, redirect
from flask_googlemaps import GoogleMaps, Map, icons
from geopy.geocoders import Nominatim
from locate_neighborhood import get_neighborhood
from joblib import load
import pandas as pd

app = Flask(__name__)
GoogleMaps(app, key= "AIzaSyDom1FJvz41eWHt9r7e8_tq93_w7Fg8sQA"
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

    return render_template("index2.html", gmap=gmap)

@app.route("/data", methods=["POST", "GET"])
def postdata():
    if request.method == 'POST':
        form_data = request.form
        geolocator = Nominatim(user_agent="Chicago-Traffic")
        start_location = geolocator.geocode(form_data["Start"])
        start_lat = start_location.latitude
        start_long = start_location.longitude
        end_location = geolocator.geocode(form_data["End"])
        end_lat = end_location.latitude
        end_long = end_location.longitude
        start_hood = get_neighborhood(start_long, start_lat)
        end_hood = get_neighborhood(end_long, end_lat)

        start_column = f"hood_label_{start_hood}"
        end_column = f"hood_label_{end_hood}"
        weather = f"weather_condition_{form_data['weather']}"
        light_con = f"lighting_condition_{form_data['light_con']}"
        day = f"crash_day_of_week_{form_data['day_of_week']}"
        hour = f"crash_hour_{form_data['hour']}"

        input_template = pd.read_csv("input_template.csv")
        input_template.at[0, start_column] = 1
        input_template.at[1, end_column] = 1
        input_template.at[0, weather] = 1
        input_template.at[1, weather] = 1
        input_template.at[0, light_con] = 1
        input_template.at[1, light_con] = 1
        input_template.at[0, day] = 1
        input_template.at[1, hour] = 1

        model_damage = load("damage.joblib")
        damage = model_damage.predict_proba(input_template)
        model_hit_n_run = load("hit_and_run.joblib")
        hit_n_run = model_hit_n_run.predict_proba(input_template)

        return render_template("data.html", form_data=form_data, start_location=start_location,
                               end_location=end_location, start_long=start_long, start_lat=start_lat,
                               hit_n_run=hit_n_run, damage=damage)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)