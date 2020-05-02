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



# EXAMPLE
# app = Flask(__name__)
# @app.route('/')
# def hello_world():
#	return 'Hello world'