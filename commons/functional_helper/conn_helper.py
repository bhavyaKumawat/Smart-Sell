import logging
import os

import pyodbc

# async def get_cursor():
#     server = os.environ["server"]
#     database = os.environ["database"]
#     username = os.environ["username"]
#     password = os.environ["password"]
#     conn = pymssql.connect(server=server, user=username, password=password, database=database)
#
#     cursor = conn.cursor()
#     return (cursor, conn)

logger = logging.getLogger()


async def get_cursor():
    # server = os.environ["server"]
    # database = os.environ["database"]
    # username = os.environ["username"]
    # password = os.environ["password"]
    db_conn_string = os.environ["db_conn_string"]
    conn = pyodbc.connect(db_conn_string)
    # 'DRIVER={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.8.so.1.1};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

    cursor = conn.cursor()
    logger.info("Connected to the Database")
    return cursor, conn


