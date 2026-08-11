# Import pandas
import pandas as pd


# Load Shiller data
shiller = pd.read_excel(
    "../data/raw/ie_data.xls",
    sheet_name="Data",
    skiprows=7
)


# Check column names
print(shiller.columns)