import pandera as pa
from pandera.typing import Series

class BaseFinanceMetrics(pa.DataFrameModel):
    company_sector: Series[str]
    operating_revenue: Series[float] = pa.Field(ge = 0)
    date: Series[pa.DateTime]
    tax_percent: Series[float] = pa.Field(in_range = {"min_value": 0, "max_value": 1})
    operatiing_costs: Series[float] = pa.Field(ge = 0)

    class Config:
        strict = True
        coerce = True

    @pa.Check(
        "company_sector",
        name="Check the sector code",
        error="Sector code is not valid.")
    def sector_code_check(cls, code: Series[str]) -> Series[bool]:
        return code.str[:4].isin(["REP_", "MNT_", "VND_"])