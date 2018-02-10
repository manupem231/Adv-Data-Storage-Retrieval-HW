from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func

from flask import Flask, jsonify
import numpy as np
import pandas as pd
import time
from datetime import datetime, timedelta, date
from dateutil.parser import parse

# Database Setup
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

#print(Base.classes.keys())

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measure

# Define a session
session = Session(engine)
app = Flask(__name__)

# Flask Routes

@app.route("/")
def welcome():
    """List all available api routes."""
    return ("Available Routes:<br/> \
            /api/v1.0/precipitation<br/> \
            /api/v1.0/stations<br/> \
            /api/v1.0/tobs<br/> \
            /api/v1.0/&ltstart&gt<br/> \
            /api/v1.0/&ltstart&gt/&ltend&gt")

@app.route("/api/v1.0/precipitation")
def dates():
    """ Return a list of all dates and temperature observations
    """
    # Query all dates and temperature observations for last year
    results = session.query(Measurement.date, Measurement.tobs).\
              filter(Measurement.date.between('2017-01-01', '2017-12-31')).all()

    #Convert query results to dictionary
    all_observations = []
    for temp in results:
        temp_dict = {}
        temp_dict["date"] = temp.date
        temp_dict["tobs"] = temp.tobs
        all_observations.append(temp_dict)

    # Convert list of tuples into normal list
    return jsonify(all_observations)

@app.route("/api/v1.0/stations")
def stations():
    station_results = session.query(Measurement.station, Measurement.date).\
                      filter(Measurement.date.between('2017-01-01', '2017-12-31')).all()
                      
    all_stations = []
    for station in station_results:
        station_dict = {}
        station_dict["Station"] = station.station
        station_dict["Date"] = station.date
        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    tobs_results = session.query(Measurement.tobs, Measurement.station, Measurement.date).\
                    filter(Measurement.date.between('2017-01-01', '2017-12-31')).all()
                      
    all_tobs = []
    for tob in tobs_results:
        tob_dict = {}
        tob_dict["Temp. Observations"] = tob.tobs
        tob_dict["Station"] = tob.station
        tob_dict["Date"] = tob.date
        all_tobs.append(tob_dict)

    return jsonify(all_tobs)


@app.route("/api/v1.0/<start>")
def temp_start_details(start = '2017-01-01'):

    """Return Min/Max/Avg temperature details for a given start date."""
    
    temperature_min = session.query(func.min(Measurement.tobs)).\
                        filter(Measurement.date >= '2017-01-01').scalar()

    temperature_max = session.query(func.max(Measurement.tobs)).\
                        filter(Measurement.date >= '2017-01-01').scalar()

    temperature_avg = session.query(func.avg(Measurement.tobs)).\
                        filter(Measurement.date >= '2017-01-01').scalar()

    
    return f"TMIN: {temperature_min} \nTMAX: {temperature_max} \nTAVG: {temperature_avg}"

@app.route("/api/v1.0/<start>/<end>")
def temp_start_end_details(start = '2017-01-01', end = '2017-12-31'):

    """Return Min/Max/Avg temperature details for a given start & end date."""
    
    temp_min = session.query(func.min(Measurement.tobs)).\
                        filter(Measurement.date.between('2017-01-01', '2017-12-31')).scalar()

    temp_max = session.query(func.max(Measurement.tobs)).\
                        filter(Measurement.date.between('2017-01-01', '2017-12-31')).scalar()

    temp_avg = session.query(func.avg(Measurement.tobs)).\
                        filter(Measurement.date.between('2017-01-01', '2017-12-31')).scalar()

    
    return f"TMIN: {temp_min} \nTMAX: {temp_max} \nTAVG: {temp_avg}"

if __name__ == '__main__':
    app.run(debug = True)