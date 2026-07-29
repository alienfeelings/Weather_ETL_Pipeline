import requests

# Function to fetch data / send a GET request to the API
def extract_weather_data():
    # Coordinates for Chicago
    url = "https://api.open-meteo.com/v1/forecast?latitude=41.85&longitude=-87.65&current_weather=true"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['current_weather']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None