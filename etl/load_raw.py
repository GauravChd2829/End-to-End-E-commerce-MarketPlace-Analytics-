import pandas as pd
from sqlalchemy import create_engine

# -------------------------------
# Database Configuration
# -------------------------------

DB_CONFIG = {
    "user": "postgres",
    "password": "postgres123",   # your new password
    "host": "localhost",
    "port": "5432",
    "database": "olist_analytics"
}

def get_engine():
    """Create database engine."""
    connection_string = (
        f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )
    return create_engine(connection_string)

# -------------------------------
# Generic Loader Function
# -------------------------------

def load_csv_to_raw(csv_path, table_name):
    """
    Loads a CSV file into raw schema table.
    
    Parameters:
        csv_path (str): Path to CSV file
        table_name (str): Target table name in raw schema
    """
    print(f"\nReading file: {csv_path}")
    
    df = pd.read_csv(csv_path)
    print(f"Rows loaded from CSV: {len(df)}")

    engine = get_engine()

    print(f"Loading into raw.{table_name} ...")

    df.to_sql(
        name=table_name,
        con=engine,
        schema="raw",
        if_exists="append",
        index=False
    )

    print(f"Successfully loaded into raw.{table_name}")

# -------------------------------
# Main Execution
# -------------------------------

if __name__ == "__main__":

    files_to_tables = {
        "olist_customers_dataset.csv": "customers",
        "olist_orders_dataset.csv": "orders",
        "olist_order_items_dataset.csv": "order_items",
        "olist_order_payments_dataset.csv": "order_payments",
        "olist_order_reviews_dataset.csv": "order_reviews",
        "olist_products_dataset.csv": "products",
        "olist_sellers_dataset.csv": "sellers",
        "product_category_name_translation.csv": "product_category_name_translation"

    }

    for file_name, table_name in files_to_tables.items():
        csv_path = f"../data/incoming/{file_name}"
        load_csv_to_raw(csv_path, table_name)

