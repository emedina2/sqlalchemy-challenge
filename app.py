import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask,jsonify
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
#################################################


app = Flask(__name__)

#################################################
# Flask Routes
#################################################
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
#Define precipitation page
@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Precipitation Page opened.")
    session= Session(engine)
    date_prec = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= 2016-8-23).all()
    session.close()
    return jsonify(date_prec)

@app.route("/api/v1.0/stations")
def stations():
    print("Station Page Opened."
    session= Session(engine)
    total_stations = session.query(distinct(Station.station)).all()
    session.close()
    return jsonify(total_stations)


if __name__ == "__main__":
    app.run(debug=True)