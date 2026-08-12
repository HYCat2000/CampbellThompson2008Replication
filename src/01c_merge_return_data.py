import pandas as pd

# Load processed Welch-Goyal data
wg = pd.read_csv(
    "../data/processed/constructed_predictors.csv"
)

# Display every column loaded from the processed Welch–Goyal file.
print("Welch–Goyal columns:")
print(wg.columns.tolist())

# Stop immediately if the dividend-price ratio was not retained
# during the earlier Welch–Goyal processing step.
if "dp" not in wg.columns:
    raise ValueError(
        "The column 'dp' is missing from constructed_predictors.csv. "
        "It must be created in the Welch–Goyal processing script."
    )

# Inspect the first dividend-price observations before merging.
print("\nWelch–Goyal dividend-price data:")
print(
    wg[
        [
            "yyyymm",
            "dp",
        ]
    ].head(15)
)
# Load processed Shiller returns
shiller = pd.read_csv(
    "../data/processed/shiller_returns.csv"
)

# Merge Shiller returns into Welch-Goyal data by month
df = wg.merge(shiller, on = "yyyymm", how = "left")

# Merge Shiller's reconstructed returns into the Welch–Goyal data.
# All Welch–Goyal columns, including dp, should remain in the result.
df = wg.merge(
    shiller,
    on="yyyymm",
    how="left",
    validate="one_to_one",
)

# Confirm that the dividend-price ratio survived the merge.
if "dp" not in df.columns:
    raise ValueError(
        "The column 'dp' is unexpectedly missing after the merge."
    )

# Inspect the merged predictor and return data.
print("\nMerged data:")
print(
    df[
        [
            "yyyymm",
            "dp",
            "shiller_return",
            "CRSP_SPvw",
        ]
    ].head(15)
)

# Start with CRSP stock returns
df["stock_return"] = df["CRSP_SPvw"]


# Use Shiller returns before January 1927
df.loc[
    df["yyyymm"] < 192701,
    "stock_return"
] = df["shiller_return"]

# Check the Shiller-to-CRSP transition
print(
    df.loc[
        (df["yyyymm"] >= 192610)
        & (df["yyyymm"] <= 192703),
        [
            "yyyymm",
            "shiller_return",
            "CRSP_SPvw",
            "stock_return"
        ]
    ]
)

print(df[["yyyymm", "stock_return"]].head())
print(df[["yyyymm", "stock_return"]].tail())
print(df["stock_return"].isna().sum())

print(
    df[
        [
            "yyyymm",
            "stock_return",
            "Rfree"
        ]
    ].head(10)
)

# Construct monthly excess return

df["excess_return"] = (df["stock_return"] - df["Rfree"])

# Display the variables that will enter the predictive regression.
print(
    df[
        [
            "yyyymm",
            "dp",
            "stock_return",
            "Rfree",
            "excess_return",
        ]
    ].head(10)
)

df.to_csv("../data/processed/merged_predictor_returns.csv", index=False)