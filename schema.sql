CREATE TABLE IF NOT EXISTS weather_observations (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    temperature_celsius DECIMAL(5, 2) NOT NULL,
    wind_speed_kmh DECIMAL(6, 2),
    weather_code INTEGER,
    observed_at TIMESTAMP NOT NULL,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX IF NOT EXISTS unique_city_observation_idx
ON weather_observations (city, observed_at);
