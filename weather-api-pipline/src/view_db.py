from tabulate import tabulate # type: ignore
import sqlite3

# Connect to database and create cursor object for SQL execution
conn = sqlite3.connect("data/weather_database.db")
cursor = conn.cursor()

# Select statement for viewing all data in table, stored in cursor
cursor.execute("SELECT * FROM weather_data")

# Assign result set that cursor points to to a variable
rows = cursor.fetchall()
# Retrieve column names from cursor data with list comprehension
columns = [col[0] for col in cursor.description]

# Close connection to db
conn.close()

# Print statement using tabulate formatting
print(tabulate(rows, headers=columns, tablefmt="grid"))