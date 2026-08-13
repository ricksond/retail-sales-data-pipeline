import os

import psycopg 
from dotenv import load_dotenv

#function to load the environment variables
load_dotenv()

#establishing the connection to the database
connection=psycopg.connect(
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
)

cursor=connection.cursor()

#Checking the connection to current database
cursor.execute("SELECT current_database();")

print("Connected to database:", cursor.fetchone()[0])

cursor.close()
connection.close()

