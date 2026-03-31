import sqlite3

# Local path to database
DB_PATH = "data/weather_database.db"


def connect_db():
    # Returns connection object
    return sqlite3.connect(DB_PATH)


def create_table(conn):
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


def insert_weather(conn, city, temperature, windspeed, weathercode):
    # Create cursor object
    cursor = conn.cursor()

    # Execute SQL command to insert data into table
    cursor.execute("""
    INSERT INTO weather_data (city, temperature, windspeed, weathercode)
    VALUES (?, ?, ?, ?)   
    """, (city, temperature, windspeed, weathercode))
    
    # Save changes
    conn.commit()