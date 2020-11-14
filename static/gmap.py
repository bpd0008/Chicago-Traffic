from flask import Flask, render_template
from flask_googlemaps import GoogleMaps, Map, icons
app = Flask(__name__)
GoogleMaps(app, key="Googe Api Key Here"
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
        style="height:400px;width:600px;margin:0;",
    )
    return render_template("simple.html", gmap=gmap)
if __name__ == "__main__":
    app.run(port=5050)