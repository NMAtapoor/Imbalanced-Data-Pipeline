
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelBinarizer
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix, 
    roc_auc_score, cohen_kappa_score, f1_score, precision_score, recall_score)

def train_svm_model(data_dfs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    datasets = svm_accuracy = svm_f1 = svm_recall = svm_precision = svm_kappa =[]
    svm_auc= []
     
    for key, value in data_dfs.items():
        X = value.drop(columns=["Class"])
        y = value["Class"]
        X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y)
        svm_model = SVC(kernel='rbf', C=1.0, gamma='scale', probability=True, random_state=42)
        svm_model.fit(X_train, y_train)

        svm_y_pred = svm_model.predict(X_test)
        svm_y_prob = svm_model.predict_proba(X_test)[:, 1]  # probability for positive class
        datasets.append(key)
        
        svm_accuracy.append(accuracy_score(y_test, svm_y_pred))
        svm_auc.append(roc_auc_score(y_test, svm_y_prob))
        svm_f1.append(f1_score(y_test, svm_y_pred, average='weighted'))
        svm_precision.append(precision_score(y_test, svm_y_pred, average='weighted'))
        svm_recall.append(recall_score(y_test, svm_y_pred, average='weighted'))
        svm_auc.append(roc_auc_score(y_test, svm_y_prob))
        svm_kappa.append(cohen_kappa_score(y_test, svm_y_pred))
    
    svm_metrics_df =  pd.DataFrame({"name":datasets, "Accuracy": svm_accuracy,
                                  "F1_Score": svm_f1, "Precision": svm_precision,
                                  "Recall": svm_recall, "Kappa": svm_kappa, "AUC":svm_auc})
    print(svm_metrics_df)   
    return svm_metrics_df 