from tabulate import tabulate
import sqlite3

conn = sqlite3.connect("data/weather_database.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM weather_data")

rows = cursor.fetchall()
columns = [col[0] for col in cursor.description]

print(tabulate(rows, headers=columns, tablefmt="grid"))