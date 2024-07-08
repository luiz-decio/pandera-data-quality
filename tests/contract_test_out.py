import sys
import os
import pandas as pd
import numpy as np
import pandera as pa
import pytest

# Add the root directory of your project to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.contract import OutFinanceMetrics

def correct_contract_test():
    df_test = pd.dateFrame({
        "company_sector": ["VND_A1B2C3", "REP_X7Y8Z9", "MNT_4D5E6F"],
        "operating_revenue": [1000,1000,1000],
        "date": ["2023-01-01", "2023-01-01", "2023-01-01"],
        "tax_percent": [0.1, 0.1, 0.1],
        "operating_costs": [200,200,200],
        "tax_value": [100,100,100],
        "total_cost": [300,300,300],
        "net_income": [700,700,700],
        "operating_margin": [700/1000,700/1000,700/1000]
    })

    OutFinanceMetrics.validate(df_test)

def correct_contract_optional_column_test():
    df_test = pd.dateFrame({
        "company_sector": ["VND_A1B2C3", "REP_X7Y8Z9", "MNT_4D5E6F"],
        "operating_revenue": [1000,1000,1000],
        "date": ["2023-01-01", "2023-01-01", "2023-01-01"],
        "tax_percent": [0.1, 0.1, 0.1],
        "operating_costs": [200,200,200],
        "tax_value": [100,100,100],
        "total_cost": [300,300,300],
        "net_income": [700,700,700],
        "operating_margin": [700/1000,700/1000,700/1000],
        "insert_date": ["2024-01-01", "2024-01-01", "2024-01-01"]
    })

    OutFinanceMetrics.validate(df_test)

def missiing_column_test():
    df_test = pd.dateFrame({
        "company_sector": ["VND_A1B2C3", "REP_X7Y8Z9", "MNT_4D5E6F"],
        "operating_revenue": [1000,1000,1000],
        "date": ["2023-01-01", "2023-01-01", "2023-01-01"],
        "tax_percent": [0.1, 0.1, 0.1],
        "operating_costs": [200,200,200],
        "tax_value": [100,100,100],
        # The total_cost column was removed to test the method
        "net_income": [700,700,700],
        "operating_margin": [700/1000,700/1000,700/1000]
    })

    with pytest.raises(pa.errors.SchemaError):
        OutFinanceMetrics.validate(df_test)

def new_column_test():
    df_test = pd.dateFrame({
        "company_sector": ["VND_A1B2C3", "REP_X7Y8Z9", "MNT_4D5E6F"],
        "operating_revenue": [1000,1000,1000],
        "date": ["2023-01-01", "2023-01-01", "2023-01-01"],
        "tax_percent": [0.1, 0.1, 0.1],
        "operating_costs": [200,200,200],
        "tax_value": [100,100,100],
        "total_cost": [300,300,300],
        "net_income": [700,700,700],
        "operating_margin": [700/1000,700/1000,700/1000],
        "dummy_column": [0,0,0]
    })


    with pytest.raises(pa.errors.SchemaError):
        OutFinanceMetrics.validate(df_test)

def missing_value_test():
    df_test = pd.dateFrame({
        "company_sector": ["VND_A1B2C3", "REP_X7Y8Z9", "MNT_4D5E6F"],
        "operating_revenue": [1000,1000,1000],
        "date": ["2023-01-01", "2023-01-01", "2023-01-01"],
        "tax_percent": [0.1, 0.1, 0.1],
        "operating_costs": [200,200,200],
        "tax_value": [100,100,100],
        "total_cost": [300,300,300],
        "net_income": [np.nan,700,700],
        "operating_margin": [700/1000,700/1000,700/1000],
    })


    with pytest.raises(pa.errors.SchemaError):
        OutFinanceMetrics.validate(df_test)

def operating_margin_metric_test():
    df_test = pd.dateFrame({
        "company_sector": ["VND_A1B2C3", "REP_X7Y8Z9", "MNT_4D5E6F"],
        "operating_revenue": [1000,1000,1000],
        "date": ["2023-01-01", "2023-01-01", "2023-01-01"],
        "tax_percent": [0.1, 0.1, 0.1],
        "operating_costs": [200,200,200],
        "tax_value": [100,100,100],
        "total_cost": [300,300,300],
        "net_income": [700,700,700],
        "operating_margin": [50,700/1000,700/1000],
    })


    with pytest.raises(pa.errors.SchemaError):
        OutFinanceMetrics.validate(df_test)