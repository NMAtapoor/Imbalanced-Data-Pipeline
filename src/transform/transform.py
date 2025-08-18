import pandas as pd
from typing import Tuple
from src.transform.clean_abalone import clean_abalone
from src.utils.logging_utils import setup_logger
from src.transform.encode_abalone import encode_abalone
from src.transform.standardize_abalone import standardize_data
from src.transform.resample_abalone import generate_imb_data_version
from src.transform.add_imbalance_tag import add_tag_to_data_versions
from src.transform.merge_abalone_data_versions import merge_abalone_df

logger = setup_logger("transform_data", "transform_data.log")


def transform_data(data) -> Tuple[pd.DataFrame, pd.DataFrame]:
    try:
        logger.info("Starting data transformation process...")
        # Clean transaction data
       # logger.info("Cleaning transaction data...")
        #cleaned_transactions = clean_transactions(data[0])
        #logger.info("Transaction data cleaned successfully.")
        # Clean customer data
        logger.info("Cleaning Abalone data...")
        cleaned_abalone = clean_abalone(data)
        logger.info("Customer data cleaned successfully.")
        
        # Standardize Abalone data
        logger.info("Standardizing Abalone data...")
        standardized_abalone = standardize_data(cleaned_abalone)
        logger.info("Abalone data was standardized successfully.")
        
        logger.info("Encoding Abalone data ...")
        encoded_abalone = encode_abalone(standardized_abalone)
        logger.info("Abalone data encoded successfully.")
        
        logger.info("Creating Abalone data versions...") 
        abalone_data_versions = generate_imb_data_version(encoded_abalone)
        logger.info("Abalone data versions created successfully.")
        
        logger.info("Adding IR Column to each data versions...")
        abalone_data_versions_with_tag = add_tag_to_data_versions(abalone_data_versions)
        logger.info("Tag to each data version added successfully.")
        
        logger.info("Merging abalone data version...")
        merged_abalone_data = merge_abalone_df(abalone_data_versions_with_tag)
        logger.info("Tag to each data version added successfully.")

        return merged_abalone_data
    except Exception as e:
        logger.error(f"Data transformation failed: {str(e)}")
        raise
