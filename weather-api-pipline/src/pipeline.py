from coordinates_api import get_coordinates
from weather_api import get_weather
from database import connect_db, create_table, insert_weather


def main():
    # Prompt user for zipcode
    zipcode = input("Enter zipcode: ")

    # Obtain coordinates from zipcode
    coordinates = get_coordinates(zipcode)

    print(type(coordinates), coordinates)

    # Obtain weather from coordinates
    weather = get_weather(coordinates)

    # Create connection object to local database, then create table if not exists
    conn = connect_db()
    create_table(conn)

    # Insert weather values into table
    insert_weather(conn, weather["temperature"], weather["windspeed"], weather["weathercode"])

    # Close connection
    conn.close()



if __name__ == "__main__":
    main()