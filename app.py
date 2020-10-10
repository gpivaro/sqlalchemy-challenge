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
from sqlalchemy import create_engine, func
import datetime as dt

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
        f"<h3>Available Routes:</h3>"
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
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of all precipitation measurments"""

    # Query all precipitation measurments
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()

    # close the session to end the communication with the database
    session.close()

    # Create a dictionary from the row data and append to a list of all_stations
    all_precipitation = []
    for meas in results:
        meas_dict = {str(meas.date): meas.prcp}
        all_precipitation.append(meas_dict)

    return jsonify(all_precipitation)


# /api/v1.0/stations
# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all stations"""

    # Query all precipitation measurments
    session = Session(engine)
    results = session.query(
        Station.id,
        Station.station,
        Station.name,
        Station.latitude,
        Station.longitude,
        Station.elevation,
    ).all()

    # close the session to end the communication with the database
    session.close()

    # Create a dictionary from the row data and append to a list of all_stations
    all_stations = []
    for stat in results:
        station_dict = {}
        station_dict["Id"] = stat.id
        station_dict["Station"] = stat.station
        station_dict["Name"] = stat.name
        station_dict["Latitude"] = stat.latitude
        station_dict["Longitude"] = stat.longitude
        station_dict["Elevation"] = stat.elevation
        all_stations.append(station_dict)

    return jsonify(all_stations)


# /api/v1.0/tobs
# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of all tobs"""

    # Query all precipitation measurments
    session = Session(engine)

    # Retrieve the most recent meas data
    date_last_meas_str = session.query(func.max(Measurement.date))

    # Convert the data from string to datetime
    date_last_meas_object = dt.datetime.strptime(
        date_last_meas_str.first()[0], "%Y-%m-%d"
    ).date()

    # Create a query data interval
    query_date = date_last_meas_object - dt.timedelta(days=365)

    # What are the most active stations? (i.e. what stations have the most rows)?
    # List the stations and the counts in descending order.
    most_active_stations = (
        session.query(Station.station, func.count(Station.station))
        .filter(Measurement.station == Station.station)
        .group_by(Station.station)
        .order_by(func.count(Station.station).desc())
        .all()
    )

    # Using the station id from the previous query, calculate the temperature recorded,
    most_active_station_id = most_active_stations[0][0]

    results = (
        session.query(Measurement.date, Measurement.tobs)
        .filter(Measurement.date > query_date)
        .filter(Measurement.station == most_active_station_id)
        .all()
    )

    # close the session to end the communication with the database
    session.close()

    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(results))
    print(all_tobs)
    return jsonify(all_tobs)


# /api/v1.0/<start> and /api/v1.0/<start>/<end>
# Return a JSON list of the minimum temperature, the average temperature,
# and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates
# greater than and equal to the start date.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX
# for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start_date>")
def tobs_from_data(start_date):
    """Return a JSON list of the minimum temperature, the average temperature, 
    and the max temperature for a given start data on."""

    # Query all precipitation measurments
    session = Session(engine)

    # Retrieve the most recent meas data
    date_last_meas_str = session.query(func.max(Measurement.date))

    # Convert the data from string to datetime
    date_last_meas_object = dt.datetime.strptime(
        date_last_meas_str.first()[0], "%Y-%m-%d"
    ).date()

    date_start = dt.datetime.strptime(start_date, "%Y-%m-%d").date()

    # Create a query data interval
    # query_date = date_last_meas_object - dt.timedelta(days=365)
    query_date = date_last_meas_object - date_start

    # What are the most active stations? (i.e. what stations have the most rows)?
    # List the stations and the counts in descending order.
    most_active_stations = (
        session.query(Station.station, func.count(Station.station))
        .filter(Measurement.station == Station.station)
        .group_by(Station.station)
        .order_by(func.count(Station.station).desc())
        .all()
    )

    # Using the station id from the previous query, calculate the temperature recorded,
    most_active_station_id = most_active_stations[0][0]

    # lowest temperature recorded
    TMIN = (
        session.query(Measurement.tobs)
        .filter(Measurement.date > query_date)
        .filter(Measurement.station == most_active_station_id)
        .order_by(Measurement.tobs.asc())
        .all()
    )

    # highest temperature recorded
    TMAX = (
        session.query(Measurement.tobs)
        .filter(Measurement.date > query_date)
        .filter(Measurement.station == most_active_station_id)
        .order_by(Measurement.tobs.desc())
        .all()
    )

    # average temperature
    TAVG = (
        session.query(func.avg(Measurement.tobs))
        .filter(Measurement.date > query_date)
        .filter(Measurement.station == most_active_station_id)
        .all()
    )

    # lst = [TMIN, TMAX]
    # Method 1: List Comprehension
    # results = [x for l in lst for x in l]
    results = [{x, y, z} for x in TMIN for y in TMAX for z in TAVG]

    # close the session to end the communication with the database
    session.close()

    # Convert list of tuples into normal list
    tobs_from_data = list(np.ravel(results))
    print(tobs_from_data)
    return jsonify(tobs_from_data)


if __name__ == "__main__":
    app.run(debug=True)
