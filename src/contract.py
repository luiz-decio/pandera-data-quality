import pandera as pa
import pandas as pd
from pandera.typing import Series
from typing import Optional

class BaseFinanceMetrics(pa.DataFrameModel):
    company_sector: Series[str]
    operating_revenue: Series[float] = pa.Field(ge = 0)
    date: Series[pa.DateTime]
    tax_percent: Series[float] = pa.Field(in_range = {"min_value": 0, "max_value": 1})
    operating_costs: Series[float] = pa.Field(ge = 0)

    class Config:
        strict = True
        coerce = True

    @pa.check(
        "company_sector",
        name = "Check the sector code",
        error = "Sector code is not valid.")
    def sector_code_check(cls, code: Series[str]) -> Series[bool]:
        return code.str[:4].isin(["REP_", "MNT_", "VND_"])
    
class OutFinanceMetrics(BaseFinanceMetrics):
    tax_value: Series[float] = pa.Field(ge = 0)
    total_cost: Series[float] = pa.Field(ge = 0)
    net_income: Series[float] = pa.Field(ge = 0)
    operating_margin: Series[float] = pa.Field(ge = 0)
    insert_date: Optional[pa.DateTime]

    @pa.dataframe_check
    def operating_margin_check(cls, df:pd.DataFrame) -> Series[bool]:
        return df["operating_margin"] == (df["net_income"] / df["operating_revenue"])