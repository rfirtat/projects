import sqlite3

DB_PATH = "data/weather_database.db"


def connect_db():
    return sqlite3.connect(DB_PATH)


def create_table(conn):
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather_data (
        id INTEGER PRIMARY KEY,
        temperature REAL,
        windspeed REAL,
        weathercode INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )        
    """)

    conn.commit()


def insert_weather(conn, temperature, windspeed, weathercode):
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO weather_data (temperature, windspeed, weathercode)
    VALUES (?, ?, ?)   
    """, (temperature, windspeed, weathercode))
    
    conn.commit()