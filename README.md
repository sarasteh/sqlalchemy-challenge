# sqlalchemy-challenge
------
In this challenge, I used Python and SQLAlchemy to do the climate analysis and data exploration of the climate database which are inside the *Resources folder*.
Next I designed a Flask API based on the queries that I developed. 
The API has the following routes:

---------------------------
### 1. /api/v1.0/precipitation
> Retrieve only the last 12 months of data and convert it to a dictionary using date as the key and prcp as the value.

### 2. /api/v1.0/stations
> Return a JSON list of stations from the dataset.

### 3. /api/v1.0/tobs
> Dates and temperature observations of the most-active station for the previous year of data.

### 4. /api/v1.0/<start_date>
> For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
> (example: /api/v1.0/2016-11-09)

### 5. /api/v1.0/<start_date>/<end_date>
> For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
> (example: /api/v1.0/2016-11-09/2017-01-09)
---------------------------

       
