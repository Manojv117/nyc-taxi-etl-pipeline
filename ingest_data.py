
#!/usr/bin/env python3

import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm

# NYC Taxi CSV URL
prefix = (
    "https://github.com/DataTalksClub/nyc-tlc-data/"
    "releases/download/yellow/"
)
url = prefix + "yellow_tripdata_2021-01.csv.gz"

# Column data types
dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64",
}

# Date columns
parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
]

# PostgreSQL connection
engine = create_engine(
    "postgresql+psycopg://root:root@pgdatabase:5432/ny_taxi"
)

try:
    # Read a sample to inspect the data and create the table
    print("Reading sample data...")

    df_sample = pd.read_csv(
        url,
        nrows=100,
        dtype=dtype,
        parse_dates=parse_dates,
    )

    print("Sample data:")
    print(df_sample.head())
    print("\nData shape:", df_sample.shape)
    print("\nData types:")
    print(df_sample.dtypes)

    print("\nCreating PostgreSQL table...")

    df_sample.head(0).to_sql(
        name="yellow_taxi_data",
        con=engine,
        if_exists="fail",
        index=False,
    )

    # Read the full CSV in chunks
    print("\nStarting data ingestion...")

    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=100_000,
    )

    total_rows = 0

    for df_chunk in tqdm(df_iter, desc="Ingesting chunks"):
        df_chunk.to_sql(
            name="yellow_taxi_data",
            con=engine,
            if_exists="append",
            index=False,
        )

        total_rows += len(df_chunk)

    print("\nIngestion completed successfully!")
    print(f"Total rows inserted: {total_rows}")

finally:
    engine.dispose()
    print("Database connection closed.")
