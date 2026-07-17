-- Show every weather observation, newest first
SELECT
    id,
    city,
    temperature_celsius,
    wind_speed_kmh,
    weather_code,
    observed_at,
    loaded_at
FROM weather_observations
ORDER BY observed_at DESC;


-- Show basic weather statistics for each city
SELECT
    city,
    COUNT(*) AS observation_count,
    ROUND(AVG(temperature_celsius), 2) AS average_temperature_celsius,
    MIN(temperature_celsius) AS minimum_temperature_celsius,
    MAX(temperature_celsius) AS maximum_temperature_celsius,
    ROUND(AVG(wind_speed_kmh), 2) AS average_wind_speed_kmh
FROM weather_observations
GROUP BY city
ORDER BY city;