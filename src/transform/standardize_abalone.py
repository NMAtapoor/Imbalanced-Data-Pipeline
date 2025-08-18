import pandas as pd
from sklearn.preprocessing import StandardScaler

def standardize_data(df: pd.DataFrame) -> pd.DataFrame:
    # get the numeric features
    numeric_cols = df.columns.tolist()[1:8]
    scaler = StandardScaler()
    # Fit and transform the numeric columns
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    return df