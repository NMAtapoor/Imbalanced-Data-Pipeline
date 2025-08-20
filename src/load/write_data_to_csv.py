
import os
import pandas as pd

def write_data_versions_to_csv(data_dic: dict[str, pd.DataFrame]):
    FILE_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "data",
    "data_versions"
    )
    for name, df in data_dic.items():
        df.to_csv(f"{FILE_PATH}/{name}.csv", index=False)