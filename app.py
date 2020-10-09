# Docs on session basics
# https://docs.sqlalchemy.org/en/13/orm/session_basics.html


# Now that you have completed your initial analysis, design a Flask API
# based on the queries that you have just developed.

import numpy as np
import os

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
# Use Flask to create your routes.

# Routes

# /
# Home page. List all routes that are available.
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"<h3>Available Routes:</h3><br/><br/>"
        f"<h4>Precipitation:</h4>"
        f"/api/v1.0/precipitation<br/><br/>"
        f"<h4>Stations:</h4>"
        f"/api/v1.0/stations<br/><br/>"
        f"<h4>Temperature Observations:</h4>"
        f"/api/v1.0/tobs<br/><br/>"
        f"<h4>Minimum, average, and the max temperature for a given start or start-end range:</h3>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )


# /api/v1.0/precipitation
# Convert the query results to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.

# /api/v1.0/stations
# Return a JSON list of stations from the dataset.

# /api/v1.0/tobs
# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.


# /api/v1.0/<start> and /api/v1.0/<start>/<end>
# Return a JSON list of the minimum temperature, the average temperature,
# and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates
# greater than and equal to the start date.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX
# for dates between the start and end date inclusive.


if __name__ == "__main__":
    app.run(debug=True)
