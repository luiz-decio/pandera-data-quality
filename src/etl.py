import pandas as pd
import pandera as pa
from contract import BaseFinanceMetrics

def extract_data(path_dir: str) -> pd.DataFrame:
    df = pd.read_csv(path_dir)

    try:
        BaseFinanceMetrics.validate(df, lazy = True)
    except pa.errors.SchemaErrors as exc:
        print("Error while trying to validate the data:")
        print(exc)

    return df

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    pass

def load_data(df: pd.DataFrame) -> None:
    pass

if __name__ == '__main__':
    path_dir = "data/finance_data.csv"
    df = extract_data(path_dir=path_dir)