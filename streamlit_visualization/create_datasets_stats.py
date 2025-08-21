
import pandas as pd

def datasets_stats(data_dic: dict[str, pd.DataFrame]):

    data = []
    for key, df in data_dic.items():
        col1 = key

        col2 = df["Class"].value_counts().get(1, 0)
        col3 = df["Class"].value_counts().get(0, 0)

        col4 = f"{(round(col2/col3,2)*100)}%"
        data.append([col1,col2,col3,col4])
    data_stat_df = pd.DataFrame(data, columns=["Name", "Minority", "Majority", "IR (min/maj)"])
    return data_stat_df