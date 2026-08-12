import pandas as pd

# Import statsmodels for OLS regression
import statsmodels.api as sm

# Load the processed dataset created in 01_load_and_prepare_data.py
df = pd.read_csv("../data/processed/merged_predictor_returns.csv")

# Check that the data loaded correctly
print(df.head())

# Align next month's excess return with today's predictor variables
# dp_t predicts r_(t+1)^e
df["future_excess_return"] = df["excess_return"].shift(-1)

# Remove rows where predictor or future return is missing
# dropna() is a pandas function that means: drop rows containing missing values (NaN).
# The subset=[...] part tells pandas which columns it should inspect for missing values.
# Go through df. If a row has a missing value in either dp OR future_excess_return, remove that entire row.
df = df.dropna(
    subset = ["dp", "future_excess_return"],
)

# Keep the sample period used in Campbell and Thompson (2008)
df = df[
    (df["yyyymm"] >= 192701)
    &
    (df["yyyymm"] <= 200512)
]

# Dependent Variable
y = df["future_excess_return"]

# Independent Variable
X = df["dp"]

# Add intercept term a
X = sm.add_constant(X)

# Estimate predictive regression
model = sm.OLS(y, X).fit(
    cov_type = "HC1"
)

# Print regression results
print(model.summary())

# Extract coefficient of dp
beta = model.params["dp"]

# Extract t-statistic
t_stat = model.tvalues["dp"]

# Extract R-squared
r_squared = model.rsquared

print("predictive coefficient:", beta)
print("t-statistic:", t_stat)
print("r-squared:", r_squared)