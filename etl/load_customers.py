import pandas as pd
from sqlalchemy import create_engine

# -------------------------------
# 1. Database Connection Config
# -------------------------------

DB_USER = "postgres"
DB_PASSWORD = "postgres123"   # use your actual password
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "olist_analytics"

# Create connection string
engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# -------------------------------
# 2. Read CSV File
# -------------------------------

file_path = "../data/incoming/olist_customers_dataset.csv"

print("Reading CSV file...")

df = pd.read_csv(file_path)

print(f"CSV loaded successfully. Rows: {len(df)}")

# -------------------------------
# 3. Load into PostgreSQL
# -------------------------------

print("Loading data into raw.customers...")

df.to_sql(
    name="customers",
    con=engine,
    schema="raw",
    if_exists="append",
    index=False
)

print("Data loaded successfully into raw.customers!")
