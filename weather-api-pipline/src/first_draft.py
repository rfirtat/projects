import requests
import json
import sqlite3

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 33.9257,
    "longitude": -117.8897,
    "current_weather": True
}

response = requests.get(url, params=params)

data = response.json()

weather = data["current_weather"]

temperature = weather["temperature"]
windspeed = weather["windspeed"]
weathercode = weather["weathercode"]

conn = sqlite3.connect("data/weather.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS weather_data(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temperature REAL,
    windspeed REAL,
    weathercode INTEGER,
    timestampe DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
INSERT INTO weather_data (temperature, windspeed, weathercode)
VALUES (?, ?, ?)
""", (temperature, windspeed, weathercode))

cursor.execute("SELECT * FROM weather_data")

print(cursor.fetchall())

conn.commit()
conn.close()

print("Weather data saved to database.")

