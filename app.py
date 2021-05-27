import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():

    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data for the last year"""
    
    # Calculate the date 1 year ago from last date in database
    one_year_date = dt.date(2017,8,23) - dt.timedelta(days = 365)
    # Query for the date and precipitation for the last year
    precipitation_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>= one_year_date).order_by(Measurement.date).all()
    
    # precipitation = list(np.ravel(precipitation_data))
    # Dict with date as the key and prcp as the value
    precipitation_dict = {date: prcp for date, prcp in precipitation_data}
    
    return jsonify(precipitation_dict)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations."""
    
    session = Session(engine)
    station_results = session.query(Station.name).all() 
    
    # Unravel results into a 1D array and convert to a list
    station_detail = list(np.ravel(station_results)) # check this function
    return jsonify(station_detail)


@app.route("/api/v1.0/tobs")
def temp_monthly():
    """Return the temperature observations (tobs) for previous year."""
   #Query for date 1 year ago
    one_year_date = dt.date(2017,8,23) - dt.timedelta(days = 365)

    # Query for the date and temperature for the last year
    temperature_data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date>= one_year_date).order_by(Measurement.date).all()
    temperature_data_list = list(temperature_data)
    #Return a JSON list of temperature observations (TOBS) for the previous year
    return jsonify(temperature_data_list)
  

    
    return jsonify()


@app.route("/api/v1.0/<start>")
def start_day(start):
    """Return TMIN, TAVG, TMAX."""
    start_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).all()
    start_day_list = list(start_day)
    return jsonify(start_day_list)





if __name__ == '__main__':
    app.run()