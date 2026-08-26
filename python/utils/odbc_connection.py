import os

import pyodbc
from dotenv import load_dotenv

#Loads the enviroment variables
load_dotenv()

#create the odbc connection string function 
def get_odbc_connection():
    """
    Establish an ODBC connection to the PostgreSQL data warehouse
    """

    driver_name="PostgreSQL Unicode"

    try:
        #Check whether the PostgreSQL ODBC Driver was installed
        available_drivers=pyodbc.drivers()

        if driver_name not in available_drivers:
            raise RuntimeError(
                f"Required ODBC Driver: {driver_name} was not found."
                f"Available Drivers:{available_drivers}"
            )

        print(f"ODBC driver found:{driver_name}")

        connection_string = (
            f"DRIVER={{{driver_name}}};"
            f"SERVER={os.getenv('POSTGRES_HOST')};"
            f"PORT={os.getenv('POSTGRES_PORT')};"
            f"DATABASE={os.getenv('POSTGRES_DB')};"
            f"UID={os.getenv('POSTGRES_USER')};"
            f"PWD={os.getenv('POSTGRES_PASSWORD')};"
        )

        connection =pyodbc.connect(connection_string)

        print("ODBC Connection Established Successfully")

        return connection

    except pyodbc.Error as e:
        print(f"ODBC Database Connection Failed:{e}")
        raise

    except Exception as e:
        print(f"ODBC setup failed:{e}")
        raise

if __name__=="__main__":
    connection = None

    try:
        connection=get_odbc_connection()

        cursor=connection.cursor()

        cursor.execute("SELECT current_database();")

        database_name=cursor.fetchone()[0]

        print(f"Connected to database:{database_name}")

    except Exception as e:
        print(f"ODBC validation failed:{e}")

    finally:
        if connection is not None:
            cursor.close()
            connection.close()
            print("ODBC connection closed.")

