import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def default():
    return(
        f"Welcome to this Flask App!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
	f"/api/v1.0/<start><br/>"
	f"/api/v1.0/<start>/<end><br/>"


    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    all_prcp = []
    for date, prcp in results:
        measurement_dict = {}
        measurement_dict["date"]= date
        measurement_dict["prcp"]= prcp
        all_prcp.append(measurement_dict)
    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station, Station.name, Station.latitude,
    Station.longitude, Station.elevation).all()
    session.close()
    all_stat=[]
    for station,name,latitude,longitude,elevation in results:
        station_dict = {}
        station_dict["station"]= station
        station_dict["name"]= name
        station_dict["latitude"]= latitude
        station_dict["longitude"]=longitude
        station_dict["elevation"]=elevation
        all_stat.append(station_dict)
    return jsonify(all_stat)

@app.route("/api/v1.0/tobs")
def Temps():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date <= '2017-08-23') .\
    filter(Measurement.date >= '2016-08-23').all()
    session.close()
    all_temps = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"]= date
        tobs_dict["tobs"]= tobs
        all_temps.append(measurement_dict)
    return jsonify(all_temps)

@app.route("/api/v1.0/<start>")
def starttemp(start_date):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start_date).all()
    startdata = []
    for mint, avgt, maxt in results:
        startdict = {}
        startdict["TMIN"]=mint
        startdict["TAVG"]=avgt
        startdict["TMAX"]=maxt
        startdata.append(startdict)
    return jsonify(startdata)


@app.route("/api/v1.0/<start>/<end>")
def startendtemp(startdate, enddate):
	session = Session(engine)
	results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= startdate).\
	filter(Measurement.date <= enddate).all()
    startenddata = []
    for minse,avgse,maxse in results:
        startend = {}
        startend["TMIN"] = minse
        startend["TAVG"] = avgse
        startend["TMAX"] = maxse
        startenddata.append(startend)
    return jsonify(startenddata)


if __name__ == '__main__':
    app.run(debug=True)