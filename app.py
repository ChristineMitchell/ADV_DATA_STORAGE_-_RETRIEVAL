#Import pandas dependencies and their aliases
import datetime as dt
import numpy as np
import pandas as pd
#Import SQLAlchemy dependencies so that we can access our data in the sqlite db (flat files on our local host)
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
#Import flask dependency
from flask import Flask, jsonify

#Create DB Engine for the flask app to access the data
engine = create_engine("sqlite:///hawaii.sqlite")

#Reflect the DB
Base = automap_base()

#Reflect the Tables
Base.prepare(engine, reflect=True)

#Create variables for each of the Classes
Measurement = Base.classes.measurement
Station = Base.classes.station

#Create a session link from Python to our DB
session = Session(engine)

#Define our Flask App
app = Flask(__name__)

#First Step: Define what our route will be. Create our homepage which is the root

#Define Welcome Route
@app.route("/")

#The next step is to add the routing information for each of the other routes. For this we'll create a function, welcome()

#Create homepage welcome function. Next, add the precipitation, stations, tobs, and temp routes that we'll need for this module into our return statement. We'll use f-strings to display them for our investors:

def welcome():
    return(
    '''   
    Welcome to the Climate Analysis API!<br/>
    Available Routes:<br/>
    /api/v1.0/precipitation<br/>
    /api/v1.0/stations<br/>
    /api/v1.0/tobs<br/>
    /api/v1.0/temp/start/end<br/>
    /api/v1.0/temp/yyyy-mm-dd/yyyy-mm-dd<br/>
    ''')

# Run a Flask App, make sure the app.py file is in the same directory as the other code
# Be sure to have the following installed:
    # pip install flask
    # pip install psycopg2-binary
# Windows: Open the terminal - At the command line: "set FLASK_APP=app.py" (there will be not return output)
# Then enter, "flask run", then see output on the local server.

#Define Precipitation Route
@app.route("/api/v1.0/precipitation")

#Create Precipitation Function.  
def precipitation():
   #Calc the date one year ago from the most recent date in the db. 
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   #Then, get the date and precipation for that prev year
   precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
   #Finally, we'll create a dictionary with the date as the key and the precipitation as the value. To do this, we will "jsonify" our dictionary.
   #  Jsonify() is a function that converts the dictionary to a JSON file. 
   #  JSON files are structured text files with attribute-value pairs and array data types.
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)       

# To Run the flask app, be sure to ctrl+c, then enter "flask run" again, then see output on the local server+api/v1.0/precipitation.

#Define Stations Route
@app.route("/api/v1.0/stations")

#Create Stations Function.  
def stations():
    results = session.query(Station.station).all()
    #We want to start by unraveling our results into a one-dimensional array. So we use the function np.ravel() as a parameter
    #Next, we will convert our unraveled results into a list. To convert the results to a list, we will need to use the list function,
    #  which is list(), and then convert that array into a list.
    stations = list(np.ravel(results))
    #Then we'll jsonify the list and return it as JSON. Let's add that functionality to our code.
    return jsonify(stations=stations)
    #You may notice here that to return our list as JSON, we need to add stations=stations. This formats our list into JSON. 
    # If you'd like to read more about it, checkout the Flask documentation

# To Run the flask app, be sure to ctrl+c, then enter "flask run" again, then see output on the local server+api/v1.0/stations.

#Define Temperature (TOBS) Route
@app.route("/api/v1.0/tobs")

#Create Temp Function.  
def temp_monthly():
    #calculate the date one year ago from the last date in the database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    #query the primary station for all the temperature observations from the previous year 
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    #unravel the results into a one-dimensional array and convert that array into a list.
    temps = list(np.ravel(results))
    #jsonify our temps list, and then return it
    return jsonify(temps=temps)

# To Run the flask app, be sure to ctrl+c, then enter "flask run" again, then see output on the local server+api/v1.0/tobs.

# Define a Summary Statistics Route
# Our last route will be to report on the minimum, average, and maximum temperatures. However, this route is different from the 
# previous ones in that we will have to provide both a starting and ending date to calculate.
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

#Create Stats Function.  
def stats(start=None, end=None):
    #create a query to select the minimum, average, and maximum temperatures from our SQLite database. 
    # We'll start by just creating a list called sel, with the following
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    # Since we need to determine the starting and ending date, add an if-not statement to our code.
    # We'll need to query our database using the list that we just made. Then, we'll unravel the results into a one-dimensional
    # array and convert them to a list. Finally, we will jsonify our results and return them. 
    if not end:
        results = session.query(*sel).filter(Measurement.date >= start).all()# take note of the asterisk in the query next to the sel list. Here the asterisk is used to indicate there will be multiple results for our query: minimum, average, and maximum temperatures.
        temps = list(np.ravel(results))
        return jsonify(temps)
    # Now we need to calculate the temperature minimum, average, and maximum with the start and end dates. We'll use the sel list, 
    # which is simply the data points we need to collect. Let's create our next query, which will get our statistics data.
    results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

# To Run the flask app, be sure to ctrl+c, then enter "flask run" again, then see output on the local server+api/v1.0/temp/start/end
# This returned nothing null, null, null because we did not specify a start date or end date.
# Fix this byentering any date in the dataset as a start and end date.Lets take June for our date range on the 
# local server+api/v1.0/temp/2017-06-01/2017-06-30
