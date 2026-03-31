from coordinates_api import get_coordinates
from weather_api import get_weather
from database import connect_db, create_table, insert_weather


def main():
    # Prompt user for zipcode
    while True:
        zipcode = input("Enter ZIP code: ")

        try:
            coordinates = get_coordinates(zipcode)
            break  # success → exit loop

        except ValueError as e:
            print(e)  # show error description
            print("Please try again.\n")

    # Obtain coordinates from zipcode
    coordinates = get_coordinates(zipcode)

    # Obtain weather from coordinates
    weather = get_weather(coordinates[1], coordinates[2])

    # Create connection object to local database, then create table if not exists
    conn = connect_db()
    create_table(conn)

    # Insert weather values into table
    insert_weather(
        conn,
        coordinates[0],
        weather["temperature"],
        weather["windspeed"],
        weather["weathercode"]
    )

    # Close connection
    conn.close()

    # Summary
    print("\nData entered into database")
    print("--------------------------")
    print(f"city: {coordinates[0]}")
    for key, value in weather.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()