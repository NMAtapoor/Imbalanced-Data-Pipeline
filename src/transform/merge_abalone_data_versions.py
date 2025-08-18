

import pandas as pd
def merge_abalone_df(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    
    merged_abalone_data = pd.concat(df.values(), axis=0)
    return merged_abalone_data