import sqlite3

# Local path to database
DB_PATH = "data/weather_database.db"


def connect_db():
    # Returns connection object
    return sqlite3.connect(DB_PATH)


def create_table(conn):
    """
    Create the weather_data table if it does not exist.
    """
    # Create cursor object - used to execute SQL commands
    cursor = conn.cursor()

    # Execute SQL command to create table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather_data (
        id INTEGER PRIMARY KEY,
        city VARCHAR,
        temperature REAL,
        windspeed REAL,
        weathercode INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )        
    """)

    # Save changes
    conn.commit()


def insert_weather(conn: str, city: str, temperature: float, windspeed: float, weathercode: int):
    """
    Insert a weather record into the database.

    Parameters
    ----------
    conn : str
    city : str
    temperature : float
    windspeed : float
    weathercode : int
    """
    # Create cursor object
    cursor = conn.cursor()

    # Execute SQL command to insert data into table
    cursor.execute("""
    INSERT INTO weather_data (city, temperature, windspeed, weathercode)
    VALUES (?, ?, ?, ?)   
    """, (city, temperature, windspeed, weathercode))
    
    # Save changes
    conn.commit()