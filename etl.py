import os

import psycopg2
import requests
from dotenv import load_dotenv


load_dotenv()

API_URL = "https://api.open-meteo.com/v1/forecast"
CITY = "Chicago"

PARAMS = {
    "latitude": 41.8781,
    "longitude": -87.6298,
    "current": "temperature_2m,wind_speed_10m,weather_code",
    "temperature_unit": "celsius",
    "wind_speed_unit": "kmh",
    "timezone": "auto",
}


def extract_weather():
    response = requests.get(API_URL, params=PARAMS, timeout=30)
    response.raise_for_status()

    return response.json()


def transform_weather(raw_weather):
    current_weather = raw_weather["current"]

    transformed_weather = {
        "city": CITY,
        "temperature_celsius": current_weather["temperature_2m"],
        "wind_speed_kmh": current_weather["wind_speed_10m"],
        "weather_code": current_weather["weather_code"],
        "observed_at": current_weather["time"],
    }

    return transformed_weather


def load_weather(clean_weather):
    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

    cursor = connection.cursor()

    insert_query = """
        INSERT INTO weather_observations (
            city,
            temperature_celsius,
            wind_speed_kmh,
            weather_code,
            observed_at
        )
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
    """

    cursor.execute(
        insert_query,
        (
            clean_weather["city"],
            clean_weather["temperature_celsius"],
            clean_weather["wind_speed_kmh"],
            clean_weather["weather_code"],
            clean_weather["observed_at"],
        ),
    )

    inserted_id = cursor.fetchone()[0]

    connection.commit()
    cursor.close()
    connection.close()

    return inserted_id


if __name__ == "__main__":
    raw_weather = extract_weather()
    clean_weather = transform_weather(raw_weather)
    new_row_id = load_weather(clean_weather)

    print(f"Weather data loaded successfully. New row ID: {new_row_id}")