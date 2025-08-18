from imblearn.over_sampling import BorderlineSMOTE
import pandas as pd


def generate_imb_data_version(df: pd.DataFrame)-> dict[str, pd.DataFrame]:
    imb_datasets_dic = {}
    ratio_values = [0.05,0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,
                    0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95,1.0]
    predictors = df.drop(columns=["Class"])  # predictors
    target = df["Class"] 
    for imb_ratio in ratio_values:
        dataset_version = resample_with_borderline_smote(predictors, target, imb_ratio)
        imb_datasets_dic[f"abalone_df_{int(imb_ratio * 100)}"] = dataset_version.copy()
    return imb_datasets_dic


def resample_with_borderline_smote(X, y, target_minority_ratio, kind='borderline-1', random_state=42):
    
    # Ensure y is Series
    y = pd.Series(y, name=y.name or "target")
    # Apply BorderlineSMOTE
    smote = BorderlineSMOTE(kind=kind, sampling_strategy=target_minority_ratio, random_state=random_state)
    X_resampled, y_resampled = smote.fit_resample(X, y)

    # Merge into a single DataFrame
    df_resampled = pd.DataFrame(X_resampled, columns=X.columns)
    df_resampled[y.name] = y_resampled
    return df_resampled
