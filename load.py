import psycopg2

# Function to load & store the data.
def load_data(clean_data):
    if not clean_data:
        print("No data to load.")
        return

    conn = None
    cursor = None

    try:
        # Connect to local PostgreSQL server.
        conn = psycopg2.connect(
            host="localhost",
            database="weather_etl_split",
            user="username",
            password="password"
        )
        cursor = conn.cursor()

        # Creates table if it doesn't exist.
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather (
                id SERIAL PRIMARY KEY,
                timestamp VARCHAR(50),
                temperature REAL,
                windspeed REAL
            )
        ''')

        # Insert the data
        cursor.execute('''
            INSERT INTO weather (timestamp, temperature, windspeed)
            VALUES (%s, %s, %s)
        ''', (clean_data['timestamp'],
              clean_data['temperature_celsius'],
              clean_data['wind_speed_kmh'])
                       )
        # Commit changes
        conn.commit()
        print("Data successfully loaded into PostgreSQL.")

    except psycopg2.Error as e:
        print(f"Database error: {e}")
    finally:
        # The finally block ensures the connection closes even if an error occurs
        # Safely check both variables before closing
        if conn:
            conn.close()
        if cursor:
            cursor.close()