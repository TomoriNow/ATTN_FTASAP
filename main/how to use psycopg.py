import psycopg2
from config import config

connection = None
try:
    params = config()
    print('Connecting to the postgreSQL database ...')
    connection = psycopg2.connect(**params)

    # create a cursor
    crsr = connection.cursor()
    # sql command to be executed for fetching the data
    sqlStr = "select * from u"

    # execute the data fetch SQL command along with the SQL placeholder values
    crsr.execute(sqlStr)
    db_version = crsr.fetchall()
    print(db_version)
    crsr.close()
except(Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if connection is not None:
        connection.close()
        print('Database connection terminated.')