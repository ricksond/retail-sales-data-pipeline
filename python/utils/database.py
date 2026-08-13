import os

import psycopg 
from dotenv import load_dotenv

#function to load the environment variables
load_dotenv()

connection=psycopg.connect(
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
)

cursor=connection.cursor()

cursor.execute("SELECT current_database();")

print("Connected to database:", cursor.fetchone()[0])

cursor.close()
connection.close()

