import numpy as np
import pandas as pd
import datetime as dt
from datetime import timedelta

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func,inspect,desc

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
station=Base.classes.station
measurement=Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"----------------------------------------------------<br/>"
        f" <h4> Available Routes: </h4> <br/>"
        f"----------------------------------------------------<br/>"
        f" 1.&nbsp &nbsp/api/v1.0/precipitation<br/>"
        f"----------------------------------------------------<br/>"
        f"  2.&nbsp &nbsp/api/v1.0/stations<br/>"
        f"----------------------------------------------------<br/>"
        f"  3.&nbsp &nbsp/api/v1.0/tobs<br/>"
        f"----------------------------------------------------<br/>"
        f"  4.&nbsp &nbsp/api/v1.0/start_date? <br/>"
        f"&nbsp &nbsp(example: /api/v1.0/2016-11-09)<br/>"
        f"----------------------------------------------------<br/>"
        f"  5.&nbsp &nbsp/api/v1.0/start_date?/end_date? <br/>"
        f"&nbsp &nbsp (example: /api/v1.0/2016-11-09/2017-01-09)<br/>"
        f"----------------------------------------------------<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Find the most recent date in the data set.
    most_recent=session.query(measurement).order_by(measurement.date.desc()).first()
    
    # Calculate the date one year from the last date in data set.
    year_ago=pd.to_datetime(most_recent.date)-timedelta(days=366)
    year_ago=str(year_ago)[:10]

    # Perform a query to retrieve the data and precipitation scores
    one_year_prcp = session.query(measurement.date,measurement.prcp).\
    filter(measurement.date>year_ago).order_by(measurement.date.desc()).all()

    session.close()

    prcp_results = []
    for date,prcp in one_year_prcp:
        prcp_dict = {}
        prcp_dict[date] = prcp
        prcp_results.append(prcp_dict)

    return jsonify(prcp_results)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # query to calculate the total number stations in the dataset
    number_of_stataions=session.query(measurement.station).distinct().count()

    session.close()
    
    return jsonify(number_of_stataions)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # query to find the most active stations (i.e. what stations have the most rows?)
    # List the stations and the counts in descending order.
    measurement_rows=session.query(measurement.station,func.count(measurement.id).\
                                label('number')).group_by(measurement.station).order_by(desc('number'))

    most_active_station=measurement_rows.first()[0]
    

    # Find the most recent date in the data set.
    most_recent=session.query(measurement).order_by(measurement.date.desc()).first()
    
    # Calculate the date one year from the last date in data set.
    year_ago=pd.to_datetime(most_recent.date)-timedelta(days=366)
    year_ago=str(year_ago)[:10]

    # Perform a query to retrieve the date and temperature
    one_year_temp = session.query(measurement.date,measurement.tobs).\
                    filter(measurement.station==most_active_station).\
                    filter(measurement.date>year_ago).order_by(measurement.date.desc()).all()
    
    session.close()
    
    one_year_temp_list = list(np.ravel(one_year_temp))
    return jsonify(one_year_temp_list)


@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    #query to calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date
    start_date_stats=session.query(func.min(measurement.tobs),
                                  func.max(measurement.tobs),func.avg(measurement.tobs)).\
                                  filter(measurement.date >= start).all()
    session.close()
   
    results_dict={}
    for min,max,avg in start_date_stats:
        results_dict["Min Temp"]=min
        results_dict["Max Temp"]=max
        results_dict["Avg Temp"]=round(avg,2)
 
    return jsonify(results_dict)


@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    #query to calculate TMIN, TAVG, and TMAX for all the dates between the start date and end date (inclusive)
    start_end_date_stats=session.query(func.min(measurement.tobs),
                                  func.max(measurement.tobs),func.avg(measurement.tobs)).\
                                  filter(measurement.date >= start).\
                                  filter(measurement.date <= end).all()
    session.close()
   
    results_dict={}
    for min,max,avg in start_end_date_stats:
        results_dict["Min Temp"]=min
        results_dict["Max Temp"]=max
        results_dict["Avg Temp"]=round(avg,2)

    
    return jsonify(results_dict)


if __name__ == '__main__':
    app.run(debug=True)
