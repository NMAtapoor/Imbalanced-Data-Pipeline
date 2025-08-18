import pandas as pd
from typing import Tuple
#from src.transform.clean_transactions import clean_transactions
from src.transform.clean_abalone import clean_abalone
from src.utils.logging_utils import setup_logger
from encode_abalone import encode_abalone

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
        # Enrich and aggregate customer/transaction data
        logger.info("Encoding Abalone data...")
        encoded_abalone = encode_abalone(cleaned_abalone)
        logger.info("Abalone data encoded successfully.")

        return encoded_abalone
    except Exception as e:
        logger.error(f"Data transformation failed: {str(e)}")
        raise
