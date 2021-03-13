import numpy as np
import pandas as pd
import sqlalchemy
import datetime
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, distinct, desc

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
        f"/api/v1.0/< start ><br/>"
        f"/api/v1.0/< start >/< end ><br/>"
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
    print("Station Page Opened.")
    session = Session(engine)
    total_stations = session.query(distinct(Station.station)).all()
    session.close()
    return jsonify(total_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    print("Tobs Page Opened")
    session = Session(engine)
    most_popular = "USC00519281"
    station_temp= session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= 2016-8-18).\
    filter(Measurement.station == most_popular).all()

    return jsonify(station_temp)

@app.route("/api/v1.0/<start>")
def start_only (start):
    print(f"Start date {start} entered.")
    start_date = start
 #Check if date format is correct   
    try:
        datetime.datetime.strptime(start_date, '%Y-%m-%d')
        correct_format = True
    except ValueError:
        correct_format = False

    if correct_format == True:
        session = Session(engine)
        date_high = session.query(func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).all()
        date_low = session.query(func.min(Measurement.tobs)).\
            filter(Measurement.date >= start_date).all()
        date_avg = session.query(func.avg(Measurement.tobs)).\
            filter(Measurement.date >= start_date).all()
        session.close()
        json_data = {"Date": start, "Max Temp": date_high[0], "Min Temp": date_low[0], "Avg Temp": date_avg[0]}
        return jsonify(json_data)
    else:
        return "No data for Date Entered or invalid date foorat. Date must be in format YYYY-MM-DD and between "
    
        

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    print(f'Start date {start} and end date {end} entered.')
    start_date = start
    end_date = end
    try:
        datetime.datetime.strptime(start_date, '%Y-%m-%d')
        datetime.datetime.strptime(end_date, '%Y-%m-%d')
        correct_format = True
    except ValueError:
        correct_format = False

    if correct_format == True:
        session = Session(engine)
        date_high = session.query(func.max(Measurement.tobs)).\
            filter(Measurement.date.between(start_date, end_date)).all()
        date_low = session.query(func.min(Measurement.tobs)).\
            filter(Measurement.date.between(start_date, end_date)).all()
        date_avg = session.query(func.avg(Measurement.tobs)).\
            filter(Measurement.date.between(start_date, end_date)).all()
        session.close()
        json_data = {"Start Date": start_date, "End Date": end_date, "Max Temp": date_high[0], "Min Temp": date_low[0], "Avg Temp": date_avg[0]}
        return jsonify(json_data)
    else:
        return "No data for Date Entered or invalid date foorat. Date must be in format YYYY-MM-DD and between "
    

if __name__ == "__main__":
    app.run(debug=True)