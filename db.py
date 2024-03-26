# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

def connect_to_postgresql():
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    database = os.getenv('DB_NAME')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')

    conn_string = f"host={host} port={port} dbname={database} user={user} password={password}"

    try:
        connection = psycopg2.connect(conn_string)
        cursor = connection.cursor()
        print("Connected to the PostgreSQL database.")
        return connection, cursor

    except Exception as e:
        print(f"Error: {e}")
        raise

def disconnect_from_postgresql(connection, cursor):
    try:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        print("Disconnected from the PostgreSQL database.")

    except Exception as e:
        print(f"Error: {e}")
        raise
