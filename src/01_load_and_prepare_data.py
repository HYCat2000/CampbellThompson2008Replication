#Import the pandas library so we can work with spreadsheet style data
import pandas as pd

# Store the location of our raw Excel dataset
file_path = "../data/raw/PredictorData.xls"

# Read the "Monthly" sheet from Excel workbook into a Pandas DataFrame
df = pd.read_excel(file_path, sheet_name = "Monthly")

# Print the first five rows so we can check the data loaded correctly
print(df.head())

# -------------------------------
# Construct replication variables
# -------------------------------

# Construct the dividend-price ratio
df["dp"] = df["D12"] / df["Index"]

# Construct the earnings-price ratio.
df["ep"] = df["E12"] / df["Index"]

# Construct the term spread.
df["term_spread"] = df["lty"] - df["tbl"]

# Construct the realized excess stock return.
df["excess_return"] = df["CRSP_SPvw"] - df["Rfree"]

# Print the first five rows of the constructed variables to check they were created correctly.
print(df[["dp", "ep", "term_spread", "excess_return"]].head())

# Select observations from January 1927 and onward. Think df[ CONDITION ] = "Give me the rows of df that satisfy CONDITION."
df_1927 = df[df["yyyymm"] >= 192701]

# Print the first five observations from 1927 onward to check the constructed variables.
print(df_1927[["yyyymm", "dp", "ep", "term_spread", "excess_return"]].head())

# Save the processed data for later analysis
df.to_csv("../data/processed/constructed_predictors.csv", index=False)