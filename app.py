# Import dependencies
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Create engine to access and query our SQLite database file
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect the database into our classes
Base = automap_base()

# Reflect database into new model
Base.prepare(engine, reflect=True)

# Create variables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session link from Python to the database
session = Session(engine)

# Create flask app
app = Flask(__name__)

#Setting up Welcome route
@app.route("/")

def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# Setting up precipitation route
@app.route("/api/v1.0/precipitation")

def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

# Setting up Stations Route, and return an unraveled list of results in JSON
@app.route("/api/v1.0/stations")

def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations)

# Setting up Monthly Temperature route
@app.route("/api/v1.0/tobs")

def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

	results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
	return jsonify(temps)

# Setting up Statistics Route (two routes for beginning and end)
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start=None, end=None):
     	sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]           

     if not end: 
	   results = session.query(*sel).filter(Measurement.date <= start).all()
           temps = list(np.ravel(results))
           return jsonify(temps)

     results = session.query(*sel).filter(Measurement.date >= start).\
	     filter(Measurement.date <= end).all()
     temps = list(np.ravel(results))
     return jsonify(temps)



# EXAMPLE
# app = Flask(__name__)
# @app.route('/')
# def hello_world():
#	return 'Hello world'