import requests
import json
import sqlite3

# Function to fetch data / send a GET request to the API
def extract_weather_data():
    # Coordinates for Chicago
    url = "https://api.open-meteo.com/v1/forecast?latitude=41.85&longitude=-87.65&current_weather=true"

    try:
        response = requests.get(url)
        response.raise_for_status() # Check for HTTP errors. .raise_for_status() is part of the requests library; forces the script to check code for error.
                                    # If error, it's routed to except block.
        data = response.json() # .json() parses raw text data and converts to native Python dictionary.
        return data['current_weather'] # Brackets are used to look up specific value by its key since the 'data' variable is a dict.
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    
# Test the extraction
raw_data = extract_weather_data()
print(raw_data)

# Function to clean and format data / convert raw JSON into structured format.
def transform_data(raw_data):
    if not raw_data: # Safety check; this guard clause stops execution early, preventing a crash if no data is found.
        return None

    # Package data into dictionary that's ready for database insertion.
    transformed = {
        'timestamp': raw_data.get('time'),
        'temperature_celsius': raw_data.get('temperature'),
        'wind_speed_kmh': raw_data.get('windspeed')
    }
    return transformed

# Test the transformation
clean_data = transform_data(raw_data)
print(clean_data)

# Function to load & store the data
def load_data(clean_data):
    if not clean_data:
        print("No data to load.")
        return

    # Connect to SQLite database (creates the file if it doesn't exist)
    conn = sqlite3.connect('weather_data.db') # Opens connection to the database.
    cursor = conn.cursor() # Messenger that carries SQL commands and brings back results.

    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            temperature REAL,
            windspeed REAL
        )
    ''')

    # Insert the data
    cursor.execute('''
        INSERT INTO weather (timestamp, temperature, windspeed)
        VALUES (?, ?, ?)
    ''', (clean_data['timestamp'],
          clean_data['temperature_celsius'],
          clean_data['wind_speed_kmh'])
                   )
    # Commit changes and close
    conn.commit()
    conn.close()
    print("Data successfully loaded into database.")

# Test the load
load_data(clean_data)

# Main function to wrap all functions and orchestrate pipeline
def run_etl_pipeline():
    print("Starting ETL pipeline...")

    print("Extracting...")
    raw = extract_weather_data()

    print("Transforming...")
    clean = transform_data(raw)

    print("Loading...")
    load_data(clean)

    print("Pipeline complete.")

if __name__ == "__main__":
    run_etl_pipeline()

# next: split into different files