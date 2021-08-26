import sqlalchemy
import json
import decimal, datetime

#Connection info for the database
connection_name = "" #Connection name from the details page of the SQL instance
table_name = "" #The name of the table in the database
db_name = "" #The name of our database
db_user = "postgres"
db_password = "" #Password for the postgres database

driver_name = 'postgres+pg8000'
query_string =  dict({"unix_sock": "/cloudsql/{}/.s.PGSQL.5432".format(connection_name)})

#JSON encoder function for SQLAlchemy special classes (date and float)
def alchemyencoder(obj):
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)

#Function 1 - selecting all the values from the database
def select_temp(request):

    stmt = sqlalchemy.text("SELECT * FROM {}".format(table_name))
    
    db = sqlalchemy.create_engine(
      sqlalchemy.engine.url.URL(
        drivername=driver_name,
        username=db_user,
        password=db_password,
        database=db_name,
        query=query_string,
      ),
      pool_size=5,
      max_overflow=2,
      pool_timeout=30,
      pool_recycle=1800
    )
    try:
        with db.connect() as conn:
          res = conn.execute(stmt)
          #Formats the object returned by SQLAlchemy as JSON using the encoder for floats and date values
          return json.dumps([dict(r) for r in res], default=alchemyencoder)
    except Exception as e:
        return 'Error: {}'.format(str(e))

#Function 2 - selecting the stock info and rain(mm)
def select_rain(request):

    stmt = sqlalchemy.text("SELECT date, index, precipitation FROM {}".format(table_name))
    
    db = sqlalchemy.create_engine(
      sqlalchemy.engine.url.URL(
        drivername=driver_name,
        username=db_user,
        password=db_password,
        database=db_name,
        query=query_string,
      ),
      pool_size=5,
      max_overflow=2,
      pool_timeout=30,
      pool_recycle=1800
    )
    try:
        with db.connect() as conn:
          res = conn.execute(stmt)
          return json.dumps([dict(r) for r in res], default=alchemyencoder)
    except Exception as e:
        return 'Error: {}'.format(str(e))