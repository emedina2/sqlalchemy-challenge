from flask import Flask,jsonify
app = Flask(__name__)

#home page & routes
@app.route("/")
def home():
    print("Home page requested")
    return (
       f"<b> Welcome to the Climate App. Below is a list of available routes. </b> <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start/<end><br/>"
    )
    @app.route(/api/v1.0/precipitation)