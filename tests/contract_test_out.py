import sys
import os
import pandas as pd
import numpy as np
import pandera as pa
import pytest

# Add the root directory of your project to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.contract import OutFinanceMetrics

def test_correct_contract():
    df_test = pd.DataFrame({
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

def test_correct_contract_optional_column():
    df_test = pd.DataFrame({
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

def test_missiing_column():
    df_test = pd.DataFrame({
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

def test_new_column():
    df_test = pd.DataFrame({
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

def test_missing_value():
    df_test = pd.DataFrame({
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

def test_operating_margin_metric():
    df_test = pd.DataFrame({
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