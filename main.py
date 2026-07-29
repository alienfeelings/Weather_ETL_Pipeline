from extract import extract_weather_data
from transform import transform_data
from load import load_data

def run_pipeline():
    print("Starting ETL pipeline...")

    raw = extract_weather_data()
    clean = transform_data(raw)
    load_data(clean)

    print("Pipeline complete.")

if __name__ == "__main__":
    run_pipeline()