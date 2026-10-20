# NYC Yellow Taxi ETL Pipeline

A batch ETL pipeline that ingests NYC Yellow Taxi trip data into PostgreSQL using Python, Pandas, SQLAlchemy, and Docker. The project explores data ingestion, relational storage, SQL analysis, and data quality validation.

## Project Overview

This project processes the January 2021 NYC Yellow Taxi dataset from a public CSV source and loads the data into PostgreSQL in manageable batches.

It also uses the NYC Taxi Zones lookup dataset to map pickup and drop-off location IDs to readable borough and zone names.

## Architecture

```text
NYC Yellow Taxi CSV
        |
        v
Python + Pandas
(Batch Extraction and Loading)
        |
        v
PostgreSQL
        |
        v
SQL Analysis and Data Quality Checks
        |
        v
Analysis-Ready Data
```

Docker Compose is used to configure the PostgreSQL database and pgAdmin services.

## Tech Stack

- **Python** — ingestion logic
- **Pandas** — CSV processing in chunks
- **SQLAlchemy** — database connectivity and data loading
- **PostgreSQL** — relational data storage
- **Docker & Docker Compose** — containerized database environment
- **SQL** — joins, aggregations, and data quality checks
- **uv** — Python dependency and project management

## Dataset

- **Source:** [NYC Taxi & Limousine Commission data via DataTalksClub](https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/yellow)
- **Dataset:** Yellow Taxi trip records for January 2021
- **Format:** Compressed CSV
- **Lookup data:** NYC Taxi Zones

The original trip data is loaded into the `yellow_taxi_data` table, while zone information is stored in the `zones` table.

## Features

- Batch ingestion using Pandas with a configurable chunk size.
- PostgreSQL integration using SQLAlchemy.
- Docker-based database environment.
- SQL joins to retrieve pickup and drop-off zone details.
- Daily trip-count analysis using `GROUP BY`, `COUNT`, and date conversion.
- Data quality checks for missing location IDs, unmatched zones, invalid timestamps, suspicious distances, fares, and potential duplicate records.

## Project Structure

```text
pipeline/
├── src/
├── ingest_data.py
├── pipeline.py
├── Dockerfile
├── Dockerfile.ingest
├── Dockerfile.uv
├── docker_compose.yml
├── pyproject.toml
├── uv.lock
├── .python-version
├── .gitignore
└── README.md
```

## Prerequisites

- Python
- Docker Desktop
- Git
- PostgreSQL client or pgAdmin
- uv, if using the project's uv configuration

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Manojv117/nyc-taxi-etl-pipeline.git
cd nyc-taxi-etl-pipeline
```

### 2. Configure the database

Review `docker_compose.yml` and configure database credentials using environment variables or a local environment file. Do not commit passwords or other secrets.

Ensure the ingestion script uses the correct database connection settings.

### 3. Start the database services

```bash
docker compose -f docker_compose.yml up -d pgdatabase pgadmin
```

### 4. Run the ingestion script

After confirming that PostgreSQL is ready and the connection settings are correct:

```bash
python ingest_data.py
```

The script is designed to read the source dataset in batches and load it into PostgreSQL. Check the script's table-creation and insertion settings before rerunning it against an existing database.

### 5. Verify the data

Connect to the `ny_taxi` database and run:

```sql
SELECT COUNT(*)
FROM yellow_taxi_data;
```

Inspect a sample:

```sql
SELECT *
FROM yellow_taxi_data
LIMIT 10;
```

Example daily aggregation:

```sql
SELECT
    tpep_dropoff_datetime::DATE AS day,
    COUNT(*) AS total_trips
FROM yellow_taxi_data
GROUP BY tpep_dropoff_datetime::DATE
ORDER BY day;
```

## Data Quality and Analysis

The project includes SQL practice and validation for:

- Missing values using `IS NULL`.
- Unmatched pickup and drop-off IDs using the `zones` lookup.
- Invalid pickup/drop-off timestamp ordering.
- Negative or zero trip distances.
- Suspicious fare and total amounts.
- Potential duplicate groups.

These checks help identify records that may need further investigation before transformation.

## Learning Outcomes

- Building a Python-based batch ingestion workflow.
- Working with CSV files and chunked data processing.
- Connecting Python applications to PostgreSQL.
- Running database services using Docker Compose.
- Writing SQL joins, aggregations, and data quality queries.
- Understanding the ingestion and validation stages of an ETL pipeline.

## Future Improvements

- Add automated ingestion and transformation tests.
- Introduce Apache Airflow for scheduling and orchestration.
- Add dbt models for reusable SQL transformations.
- Explore PySpark for distributed data processing.
- Add structured logging, retry handling, and monitoring.
- Deploy the pipeline to a cloud environment.

## Author

**Manoj V V**

B.Tech Computer Science and Engineering (IoT) student interested in Data Engineering, AI/ML, and scalable data pipelines.

GitHub: [Manojv117](https://github.com/Manojv117)
