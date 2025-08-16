
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelBinarizer
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix, 
    roc_auc_score, cohen_kappa_score, f1_score, precision_score, recall_score
)

def train_randforest_model(data_dfs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    datasets = rf_accuracy = rf_f1 = rf_recall = rf_precision = rf_kappa =[]
    rf_auc= []
    for key, value in data_dfs.items():
        X = value.drop(columns=["Class"])
        y = value["Class"]
        X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y)
    
        rf_model = RandomForestClassifier( n_estimators=200, max_depth=None, 
        random_state=42, class_weight="balanced" )
        rf_model.fit(X_train, y_train)

        rf_y_pred = rf_model.predict(X_test)
        rf_y_prob = rf_model.predict_proba(X_test)[:, 1] if len(y.unique()) == 2 else None
        
        rf_accuracy.append(accuracy_score(y_test, rf_y_pred))
        rf_f1.append(f1_score(y_test, rf_y_pred, average="weighted"))
        rf_precision.append(precision_score(y_test, rf_y_pred, average="weighted"))
        rf_recall.append(recall_score(y_test, rf_y_pred, average="weighted"))
        rf_kappa.append(cohen_kappa_score(y_test, rf_y_pred))
        rf_auc(roc_auc_score(y_test, rf_y_prob))
        
    rf_metrics_df = pd.DataFrame({"name":datasets, "Accuracy": rf_accuracy,
                                  "F1_Score": rf_f1, "Precision": rf_precision,
                                  "Recall": rf_recall, "Kappa": rf_kappa, "AUC":rf_auc})
        
    return rf_metrics_df