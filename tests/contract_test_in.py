import sys
import os
import pandas as pd
import numpy as np
import pandera as pa
import pytest

# Add the root directory of the project to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.contract import BaseFinanceMetrics

def correct_contract_test():
    df_test = pd.dateFrame({
        "company_sector": ["VND_A1B2C3", "REP_X7Y8Z9", "MNT_4D5E6F"],
        "operating_revenue": [1000,1000,1000],
        "date": ["2023-01-01", "2023-01-01", "2023-01-01"],
        "tax_percent": [0.1, 0.1, 0.1],
        "operating_costs": [200,200,200]
    })

    BaseFinanceMetrics.validate(df_test)

def new_column_test():
    df_test = pd.dateFrame({
        "company_sector": ["VND_A1B2C3", "REP_X7Y8Z9", "MNT_4D5E6F"],
        "operating_revenue": [1000,1000,1000],
        "date": ["2023-01-01", "2023-01-01", "2023-01-01"],
        "tax_percent": [0.1, 0.1, 0.1],
        "operating_costs": [200,200,200],
        "dummy_column": [0,0,0]
    })

    with pytest.raises(pa.errors.SchemaError):
        BaseFinanceMetrics.validate(df_test)

def missing_column_test():
    df_test = pd.dateFrame({
        # The company_sector column was removed to test the method
        "operating_revenue": [1000,1000,1000],
        "date": ["2023-01-01", "2023-01-01", "2023-01-01"],
        "tax_percent": [0.1, 0.1, 0.1],
        "operating_costs": [200,200,200],
        "dummy_column": [0,0,0]
    })

    with pytest.raises(pa.errors.SchemaError):
        BaseFinanceMetrics.validate(df_test)

def missing_value_test():
    df_test = pd.dateFrame({
        "company_sector": [np.nan, "REP_X7Y8Z9", "MNT_4D5E6F"],
        "operating_revenue": [1000,1000,1000],
        "date": ["2023-01-01", "2023-01-01", "2023-01-01"],
        "tax_percent": [0.1, 0.1, 0.1],
        "operating_costs": [200,200,200]
    })

    with pytest.raises(pa.errors.SchemaError):
        BaseFinanceMetrics.validate(df_test)

def invalid_sector_test():
    df_test = pd.dateFrame({
        "company_sector": ["AAA_X7Y8Z9", "REP_X7Y8Z9", "MNT_4D5E6F"],
        "operating_revenue": [1000,1000,1000],
        "date": ["2023-01-01", "2023-01-01", "2023-01-01"],
        "tax_percent": [0.1, 0.1, 0.1],
        "operating_costs": [200,200,200]
    })

    with pytest.raises(pa.errors.SchemaError):
        BaseFinanceMetrics.validate(df_test)
    
def negative_revenue_test():
    df_test = pd.dateFrame({
        "company_sector": ["VND_A1B2C3", "REP_X7Y8Z9", "MNT_4D5E6F"],
        "operating_revenue": [-1000,1000,1000],
        "date": ["2023-01-01", "2023-01-01", "2023-01-01"],
        "tax_percent": [0.1, 0.1, 0.1],
        "operating_costs": [200,200,200]
    })

    with pytest.raises(pa.errors.SchemaError):
        BaseFinanceMetrics.validate(df_test)

def invalid_date_test():
    df_test = pd.dateFrame({
        "company_sector": ["VND_A1B2C3", "REP_X7Y8Z9", "MNT_4D5E6F"],
        "operating_revenue": [1000,1000,1000],
        "date": ["invalid date", "2023-01-01", "2023-01-01"],
        "tax_percent": [0.1, 0.1, 0.1],
        "operating_costs": [200,200,200]
    })

    with pytest.raises(pa.errors.SchemaError):
        BaseFinanceMetrics.validate(df_test)

def tax_percent_test():
    df_test = pd.dateFrame({
        "company_sector": ["VND_A1B2C3", "REP_X7Y8Z9", "MNT_4D5E6F"],
        "operating_revenue": [1000,1000,1000],
        "date": ["2023-01-01", "2023-01-01", "2023-01-01"],
        "tax_percent": [1.1, 0.1, 0.1],
        "operating_costs": [200,200,200]
    })

    with pytest.raises(pa.errors.SchemaError):
        BaseFinanceMetrics.validate(df_test)
        
def negative_costs_test():
    df_test = pd.dateFrame({
        "company_sector": ["VND_A1B2C3", "REP_X7Y8Z9", "MNT_4D5E6F"],
        "operating_revenue": [1000,1000,1000],
        "date": ["2023-01-01", "2023-01-01", "2023-01-01"],
        "tax_percent": [0.1, 0.1, 0.1],
        "operating_costs": [-200,200,200]
    })

    with pytest.raises(pa.errors.SchemaError):
        BaseFinanceMetrics.validate(df_test)