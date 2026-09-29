import pandas as pd

df = pd.read_csv("data/raw/energydata_complete.csv", parse_dates=["date"])
print(df.dtypes)
print(df.columns.tolist())