import os
import pyodbc
import pandas as pd

async def get_cursor():
    server = os.environ["server"]
    database = os.environ["database"]
    username = os.environ["username"]
    password = os.environ["password"]
    conn = pyodbc.connect(
        'DRIVER={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.8.so.1.1};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

    cursor = conn.cursor()
    return (cursor, conn)



