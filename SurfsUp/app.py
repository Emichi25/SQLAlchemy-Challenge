# Import the dependencies.

import datetime as dt
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################



# Here is the Homepage

@app.route("/")
def welcome():
    return (
        f" <h1> <b> Welcome to the Climate Homepage <b/></h1>"
        f"<br/>"
        f"<ol>"
        f"<strong><h2> Available Pages: </h2></strong><br/>"
        f"<h3>/api/v1.0/precipitation</h3><br/>"
        f"<h3>/api/v1.0/stations</h3><br/>"
        f"<h3>/api/v1.0/tobs</h3><br/>"
        f"<h3>/api/v1.0/temp/<start></h3><br/>"
        f"<h3>/api/v1.0/temp/<start>/<end></h3><br/>"
    )



# Here is the perciptation page where you can see the precipitation rates for 8/23/2017 back to 8/23/2016

@app.route("/api/v1.0/precipitation")
def precipitation():
    
   
    most_recent_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= most_recent_year).all()

    
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)



# Here is the stations page where you'll find the different stations listed
#https://numpy.org/doc/stable/reference/generated/numpy.ravel.html



@app.route("/api/v1.0/stations")
def stations():
    
    findings = session.query(Station.station).all()

  
    stations = list(np.ravel(findings))
    return jsonify(stations)

# Here is the tobs page where you'll find the different temperatures listed

@app.route("/api/v1.0/tobs")
def temp_monthly():
  
   
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

   
    conclusion = session.query(Measurement.tobs).\
        filter(Measurement.station == "USC00519281").\
        filter(Measurement.date >= prev_year).all()

    
    temps1 = list(np.ravel(conclusion))

   
    return jsonify(temps1)

# Here is the start/end page where you can find the min, max and average temperatures for specified dates. 

 
# See 10.3 notes and https://docs.sqlalchemy.org/en/20/core/sqlelement.html#sqlalchemy.sql.expression.func
# Credit for this code below goes to Uzma and Jospeh during office hours 9/7/23
    
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

 
def stats(start=None, end=None):

    # Select statement
    sel = [func.min(Measurement.tobs),
           func.avg(Measurement.tobs),
           func.max(Measurement.tobs)]
    if not end:
        start = dt.datetime.strptime(start,"%m%d%Y")
        # Compute TMIN, TAVG, TMAX for start date
        results = session.query(*sel).\
                        filter(Measurement.date >= start).all()
        session.close()
        # Unravel and convert to list
        temps = list(np.ravel(results))
        return jsonify (temps)
      # Compute TMIN, TAVG, TMAX with start and stop date
    start = dt.datetime.strptime(start, "%m%d%Y")
    end = dt.datetime.strptime(end, "%m%d%Y")
    results = session.query(*sel).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).all()
    session.close()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
     



#https://learn.microsoft.com/en-us/troubleshoot/developer/webapps/aspnet/site-behavior-performance/debug-mode-applications

if __name__ == "__main__":
    app.run(debug=True)
