

import pandas as pd
from sklearn.preprocessing import OneHotEncoder

def encode_abalone(data: pd.DataFrame) -> pd.DataFrame:
    
    # separate predictors and target variables
    predictors = data.drop(columns=["Class"])  # predictors
    target = data["Class"]                # target

    # Select only 'Sex' column to encode
    encoder = OneHotEncoder(drop=None, sparse_output=False)
    sex_encoded = encoder.fit_transform(predictors[["Sex"]])

    target_encoded = data['Class'].map({'negative': 'N', 'positive': 'P'})
    # Convert to DataFrame with proper column names
    sex_encoded_df = pd.DataFrame(sex_encoded, columns=encoder.get_feature_names_out(["Sex"]))

    # Drop original 'Sex' column and concatenate encoded columns
    predictors_encoded = pd.concat([predictors.drop(columns=["Sex"]).reset_index(drop=True),
                       sex_encoded_df.reset_index(drop=True)], axis=1)

    # Combine with target column
    abalone_encoded_df = pd.concat([predictors_encoded, target_encoded.reset_index(drop=True)], axis=1)
    return abalone_encoded_df