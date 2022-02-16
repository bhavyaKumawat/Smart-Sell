import os
import pymssql
import pandas as pd


async def get_cursor():
    server = os.environ["server"]
    database = os.environ["database"]
    username = os.environ["username"]
    password = os.environ["password"]
    conn = pymssql.connect(server=server, user=username, password=password, database=database)

    cursor = conn.cursor()
    return (cursor, conn)



