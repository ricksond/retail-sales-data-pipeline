import os
from pathlib import Path
import psycopg 
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]


#function to load the environment variables
load_dotenv(PROJECT_ROOT / ".env")


def get_connection():
    """
    Establish a connection to the PostgreSQL database and return the connection object.
    """
#establishing the connection to the database
    try:
        connection=psycopg.connect(
            host=os.getenv("PROJECT_POSTGRES_HOST", os.getenv("POSTGRES_HOST")),
            port=os.getenv("PROJECT_POSTGRES_PORT", os.getenv("POSTGRES_PORT")),
            dbname=os.getenv("PROJECT_POSTGRES_DB", os.getenv("POSTGRES_DB")),
            user=os.getenv("PROJECT_POSTGRES_USER", os.getenv("POSTGRES_USER")),
            password=os.getenv("PROJECT_POSTGRES_PASSWORD", os.getenv("POSTGRES_PASSWORD"))
        )

        print("Connection to the database established successfully.")

        return connection

    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None


if __name__ == "__main__":

    # Test the database Connection
    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute("SELECT current_database();")

        print("Connected to database:", cursor.fetchone()[0])

        cursor.close()

    except Exception as e:
        print(f"Error occurred while testing the database connection: {e}")

    finally:
        if connection is not None:
            connection.close()
            print("Database connection closed.")