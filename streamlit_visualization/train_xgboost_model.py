import xgboost as xgb
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelBinarizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix, 
    roc_auc_score, cohen_kappa_score, f1_score, precision_score, recall_score)

#--------------------------------
def train_xbg_model(data_dfs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    metrics = {
        "Dataset": [],
        "Accuracy": [],
        "F1_Score": [],
        "Precision": [],
        "Recall": [],
        "Kappa": [],
        "AUC": []
    }
    for key, value in data_dfs.items():
        X = value.drop(columns=["Class"])
        y = value["Class"]
        X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y)
    
        xgb_model = xgb.XGBClassifier(objective='multi:softmax',  # multi-class classification
                                    num_class=3,                # number of classes
                                    eval_metric='mlogloss',     # evaluation metric
                                    use_label_encoder=False,    # avoid warning
                                    learning_rate=0.1,
                                    max_depth=4,
                                    n_estimators=100,
                                    random_state=42
                                    )
        xgb_model.fit(X_train, y_train)

        xgb_y_pred = xgb_model.predict(X_test)
        xgb_y_prob = xgb_model.predict_proba(X_test)[:, 1] if len(y.unique()) == 2 else None
        
        metrics["Dataset"].append(key)
        metrics["Accuracy"].append(accuracy_score(y_test, xgb_y_pred))
        metrics["F1_Score"].append(f1_score(y_test, xgb_y_pred, average="weighted"))
        metrics["Precision"].append(precision_score(y_test, xgb_y_pred, average="weighted", zero_division=0))
        metrics["Recall"].append(recall_score(y_test, xgb_y_pred, average="weighted"))
        metrics["Kappa"].append(cohen_kappa_score(y_test, xgb_y_pred))
        metrics["AUC"].append(roc_auc_score(y_test, xgb_y_prob))
    xgb_metrics_df = pd.DataFrame(metrics)
        
    return xgb_metrics_df
