# Function to clean and format data / convert raw JSON into structured format.
def transform_data(raw_data):
    if not raw_data:
        return None

    # Package data into dictionary that's ready for database insertion.
    transformed = {
        'timestamp': raw_data.get('time'),
        'temperature_celsius': raw_data.get('temperature'),
        'wind_speed_kmh': raw_data.get('windspeed')
    }
    return transformed