
import pandas as pd
from train_svm_model import train_svm_model
from read_abalone_csv_files import read_abalone_csv_files
from train_knn_model import train_knn_model
from train_randforest_model import train_randforest_model

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelBinarizer
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix, 
    roc_auc_score, cohen_kappa_score, f1_score, precision_score, recall_score
)
def train_ML_models():
    files_path = ""
    abalone_dic_df = read_abalone_csv_files(files_path)
    svm_perf_metrics_df = train_svm_model(abalone_dic_df)
    rn_perf_metrics_df = train_randforest_model(abalone_dic_df)
    knn_perf_metrics_df = train_knn_model(abalone_dic_df)
    return ""
    


