# Weather Data Pipeline (ZIP → Coordinates → Weather → SQLite)

## Overview

This project is a small **data integration pipeline** built in Python.

The program accepts a **US ZIP code**, retrieves its **geographic coordinates**, uses those coordinates to request **weather data from an external API**, and then stores the results in a **local SQLite database**.

This project demonstrates:

* API integration
* HTTP requests
* JSON parsing
* data transformation
* working with SQLite databases
* modular Python project structure

---

## Pipeline Architecture

The pipeline follows this workflow:

```
User ZIP Code
      ↓
Zippopotam API
(ZIP → latitude/longitude)
      ↓
Open-Meteo API
(latitude/longitude → weather data)
      ↓
Data transformation
      ↓
SQLite database storage
```

---

## Project Structure

```
project/
│
├── coordinates_api.py   # ZIP → latitude/longitude API integration
├── weather_api.py       # Coordinates → weather data API integration
├── database.py          # SQLite database functions
├── pipeline.py          # Main pipeline orchestration script
├── view_db.py           # Utility script to view stored database records
```

### File Descriptions

**coordinates_api.py**

* Fetches latitude and longitude from the **Zippopotam API** using a US ZIP code.

**weather_api.py**

* Retrieves weather data from a weather API using geographic coordinates.

**database.py**

* Creates and manages the SQLite database.
* Inserts weather data records.

**pipeline.py**

* Main script that orchestrates the entire pipeline:

  * accepts ZIP code input
  * fetches coordinates
  * fetches weather
  * stores results in the database

**view_db.py**

* Simple utility script used to inspect the contents of the SQLite database.

---

## Example Workflow

Run the pipeline:

```bash
python pipeline.py
```

Example interaction:

```
Enter a US ZIP code: 92821

Data entered into database
--------------------------
city: Brea
temperature: 19.9
windspeed: 9.2
weathercode: 3
```

To view stored records:

```bash
python view_db.py
```

---

## Example Stored Data

The SQLite database stores weather data retrieved from the API.

Example record:

| City | Temperature | Wind Speed | Weather Code |
| ---- | ----------- | ---------- | ------------ |
| Brea | 19.9        | 9.2        | 3            |

---

## Technologies Used

* **Python**
* **Requests** (API requests)
* **SQLite3** (local database)
* **REST APIs**
* JSON data parsing

APIs used:

* Zippopotam API (ZIP → coordinates)
* Open-Meteo API (coordinates → weather data)

---

## Skills Demonstrated

This project demonstrates several important backend/data engineering skills:

* working with **REST APIs**
* handling **HTTP requests and responses**
* parsing **nested JSON structures**
* transforming API data for storage
* building a **data pipeline**
* organizing a **modular Python project**
* using **SQLite for data persistence**

---

## Author

Built as part of a personal portfolio project to demonstrate **API integration and data pipeline development in Python**.
