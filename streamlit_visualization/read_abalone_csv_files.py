
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelBinarizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix, 
    roc_auc_score, cohen_kappa_score, f1_score, precision_score, recall_score
)

def read_abalone_csv_files(file_path: str) -> dict[str, pd.DataFrame]:
    abalone_df_dic = { }
    
    for i in range(5, 101, 5):
        full_path = f"{file_path}abalone_df_{i}.csv"
        abalone_df = pd.read_csv(full_path)
        abalone_df["Class"] = abalone_df["Class"].astype('string')
        abalone_df_dic[f"abalone_df_{i}"] = abalone_df.copy()
        
    return abalone_df_dic