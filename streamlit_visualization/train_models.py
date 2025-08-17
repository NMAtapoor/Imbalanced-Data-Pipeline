
import pandas as pd
from train_svm_model import train_svm_model
from read_abalone_csv_files import read_abalone_csv_files
from train_knn_model import train_knn_model
from train_randforest_model import train_randforest_model


def train_ML_models(path) -> dict[str, pd.DataFrame]:
    
    abalone_dic_df = read_abalone_csv_files(path)
    svm_perf_metrics_df = train_svm_model(abalone_dic_df)
    rn_perf_metrics_df = train_randforest_model(abalone_dic_df)
    knn_perf_metrics_df = train_knn_model(abalone_dic_df)
    
    metrics_dic = {"SVM": svm_perf_metrics_df,
                 "RF": rn_perf_metrics_df,
                 "KNN":knn_perf_metrics_df}
    return metrics_dic

metrics = train_ML_models("../data/data_versions/")
for key, value in metrics.items():
    value.to_csv(f"../data/metrics/{key}_metrics.csv")



