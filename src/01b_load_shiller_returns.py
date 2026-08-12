import pandas as pd

shiller = pd.read_excel(
    "../data/raw/ie_data.xls",
    sheet_name="Data",
    skiprows=7
)

# Keep only the variables needed to construct nominal stock returns
shiller = shiller[
    [
        "Date",
        "P",
        "D",
    ]
].copy()

# Construct nominal monthly stock return
# D is an annual dividend amount, so D / 12 approximates the dividend for one month
shiller["shiller_return"] = (
    (shiller["P"] + shiller["D"] / 12)
    / shiller["P"].shift(1)
    -1
)

# Display the first 15 observations
print(shiller.head(15))

# Remove rows where Date is missing.
# "Look specifically at the Date column. If Date is NaN for a row, delete that entire row."
shiller = shiller.dropna(subset=["Date"])

# Convert Shiller date format (1871.01) into yyyymm format (187101)
# Extract the year from Shiller's decimal rate
shiller["year"] = shiller["Date"].astype(int)

# Extract the month from the decimal part of the date
shiller["month"] = (
    (shiller["Date"] - shiller["year"]) * 100
).round().astype(int)

# Combine year and month into yyyymm format
shiller["yyyymm"] = (
    shiller["year"] * 100
    + shiller["month"]
)

# Remove future observations
shiller = shiller[shiller["yyyymm"] <= 192612]

# Keep only date and return
shiller = shiller[["yyyymm", "shiller_return"]]

# Check the first and last observations
print(shiller.head())
print(shiller.tail())

# Save processed Shiller return data
shiller.to_csv("../data/processed/shiller_returns.csv", index=False)