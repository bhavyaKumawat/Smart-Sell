import logging
import os
# import pymssql
import pyodbc

logger = logging.getLogger()


async def get_cursor():
    db_conn_string = os.environ["db_conn_string"]
    # db_conn_string = get_secret_b64('db-conn-string')
    conn = pyodbc.connect(db_conn_string)
    # conn = pymssql.connect(server=server, user=username, password=password, database=database)
    cursor = conn.cursor()
    logger.info("Connected to the Database")
    return cursor, conn
