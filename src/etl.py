import pandas as pd
import pandera as pa
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from datetime import datetime
from contract import BaseFinanceMetrics, OutFinanceMetrics

def extract_data(path_dir: str) -> pd.DataFrame:
    df = pd.read_csv(path_dir)

    try:
        BaseFinanceMetrics.validate(df, lazy = True)
    except pa.errors.SchemaErrors as exc:
        print("Error while trying to validate the data:")
        print(exc)

    return df

@pa.check_output(OutFinanceMetrics, lazy = True)
def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    df_transformed = df.copy()
    df_transformed["tax_value"] = df_transformed["tax_percent"] * df_transformed["operating_revenue"]
    df_transformed["total_cost"] = df_transformed["tax_value"] + df_transformed["operating_costs"]
    df_transformed["net_income"] = df_transformed["operating_revenue"] - df_transformed["total_cost"]
    df_transformed["operating_margin"] = (df_transformed["net_income"] / df_transformed["operating_revenue"])
    df_transformed["insert_date"] = datetime.now()

    return df_transformed

def load_data(df: pd.DataFrame) -> None:
    load_dotenv()

    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    POSTGRES_DB = os.getenv("POSTGRES_DB")

    POSTGRES_DB_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

    # Create the PostgreSQL engine and deine the table name
    engine = create_engine(POSTGRES_DB_URL)
    table_name = "finance_metrics"

    try:
        df.to_sql(table_name, engine, if_exists = "replace", index = False)
    except Exception as e:
        print(f"Error while trying to load table: {e}")

if __name__ == '__main__':
    path_dir = "data/finance_data.csv"
    df = extract_data(path_dir=path_dir)
    df_transformed = transform_data(df)
    load_data(df_transformed)