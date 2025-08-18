
import pandas as pd

def add_tag_to_data_versions(data_dic : dict[str, pd.DataFrame] ) -> dict[str, pd.DataFrame]:
    tag = 5
    
    for name, df in data_dic.items():
        
        df["IR"] = tag
        tag += 5
    return data_dic