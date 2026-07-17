# Weather Data ETL Pipeline

A containerized ETL pipeline that extracts real-time weather data from the Open-Meteo API, transforms the API response with Python, and loads structured observations into PostgreSQL for SQL-based analysis.

## Project Overview

This project demonstrates a complete ETL workflow using a real-world public data source:

- **Extract:** Request current weather data from the Open-Meteo REST API.
- **Transform:** Select and standardize the required fields from the nested JSON response.
- **Load:** Insert the transformed record into a PostgreSQL database.
- **Analyze:** Query stored observations using SQL aggregate functions.

The current implementation collects weather observations for Chicago, Illinois.

## Technologies

| Technology | Purpose |
|---|---|
| Python | ETL pipeline and API integration |
| PostgreSQL | Relational data storage |
| SQL | Data retrieval and aggregation |
| Docker | Database containerization |
| Docker Compose | Local infrastructure configuration |
| Open-Meteo API | Public weather data source |

## Key Features

- Extracts live weather data from a public REST API
- Transforms nested JSON into a normalized database record
- Uses environment variables for database configuration
- Uses parameterized SQL statements for safe data insertion
- Runs PostgreSQL in a persistent Docker container
- Automatically initializes the database schema for new environments
- Includes reusable SQL queries for exploratory analysis
- Provides a reproducible Python environment through `requirements.txt`

## Project Structure

```text
weather-etl-project/
├── analysis.sql          # SQL queries for weather analysis
├── docker-compose.yml    # PostgreSQL container configuration
├── etl.py                # Extract, transform, and load pipeline
├── requirements.txt      # Python dependencies
├── schema.sql            # PostgreSQL table definition
├── .env.example          # Environment variable template
├── .gitignore            # Files excluded from version control
└── README.md             # Project documentation
```

## Data Model

Weather observations are stored in the `weather_observations` table.

| Column | Data Type | Description |
|---|---|---|
| `id` | `SERIAL` | Unique record identifier |
| `city` | `VARCHAR(100)` | Name of the observed city |
| `temperature_celsius` | `DECIMAL(5,2)` | Temperature in degrees Celsius |
| `wind_speed_kmh` | `DECIMAL(6,2)` | Wind speed in kilometers per hour |
| `weather_code` | `INTEGER` | Open-Meteo weather condition code |
| `observed_at` | `TIMESTAMP` | Time reported by the weather API |
| `loaded_at` | `TIMESTAMP` | Time the record was inserted into PostgreSQL |

## Getting Started

### Prerequisites

Install the following software before running the project:

- Python 3
- Docker Desktop
- Git

### 1. Clone the repository

```powershell
git clone <repository-url>
cd weather-etl-project
```

### 2. Start PostgreSQL

```powershell
docker compose up -d
```

Docker Compose will:

- Download the PostgreSQL 16 image if needed
- Create the `weather_db` database
- Create the `weather_user` database user
- Run `schema.sql` when initializing a new database volume
- Store PostgreSQL data in a persistent Docker volume

### 3. Create a Python virtual environment

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 5. Configure environment variables

Create a local `.env` file from the provided template:

```powershell
Copy-Item .env.example .env
```

For the default local Docker configuration, use:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=weather_db
DB_USER=weather_user
DB_PASSWORD=weather_password
```

The `.env` file is excluded from version control.

## Running the ETL Pipeline

Execute the pipeline with:

```powershell
python etl.py
```

The pipeline performs the following sequence:

```text
Open-Meteo API
      ↓
Extract JSON response
      ↓
Transform selected weather fields
      ↓
Connect to PostgreSQL
      ↓
Insert weather observation
```

Example output:

```text
Weather data loaded successfully. New row ID: 1
```

Each execution adds a new weather observation to the database.

## Querying the Database

View all stored observations:

```powershell
docker exec -it weather_postgres psql -U weather_user -d weather_db -c "SELECT * FROM weather_observations;"
```

Run the complete analysis file:

```powershell
Get-Content .\analysis.sql | docker exec -i weather_postgres psql -U weather_user -d weather_db
```

## SQL Analysis

The included SQL queries calculate:

- Total number of observations by city
- Average temperature
- Minimum recorded temperature
- Maximum recorded temperature
- Average wind speed
- Weather observations ordered from newest to oldest

Example analytical query:

```sql
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
```

## Example Record

```text
 id | city    | temperature_celsius | wind_speed_kmh | weather_code | observed_at
----+---------+---------------------+----------------+--------------+---------------------
  1 | Chicago | 27.60               | 6.10           | 3            | 2026-07-17 10:15:00
```

## Skills Demonstrated

- REST API integration
- JSON data processing
- ETL pipeline development
- Python database connectivity
- PostgreSQL schema design
- SQL aggregation and analysis
- Parameterized SQL queries
- Environment-variable configuration
- Docker container management
- Technical project documentation

## Potential Enhancements

Future versions could include:

- Collecting weather data for multiple cities
- Preventing duplicate observations
- Adding structured logging and improved exception handling
- Scheduling automated pipeline executions
- Creating database indexes for larger datasets
- Building a dashboard with historical weather trends
- Adding automated tests
- Deploying the pipeline to a cloud environment

## Data Source

Weather data is provided by the [Open-Meteo API](https://open-meteo.com/).
