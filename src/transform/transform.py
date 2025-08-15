import pandas as pd
from typing import Tuple
from src.transform.clean_transactions import clean_transactions
from src.transform.clean_customers import clean_customers
from src.utils.logging_utils import setup_logger

logger = setup_logger("transform_data", "transform_data.log")


def transform_data(data) -> Tuple[pd.DataFrame, pd.DataFrame]:
    try:
        logger.info("Starting data transformation process...")
        # Clean transaction data
        logger.info("Cleaning transaction data...")
        cleaned_transactions = clean_transactions(data[0])
        logger.info("Transaction data cleaned successfully.")
        # Clean customer data
        logger.info("Cleaning customer data...")
        cleaned_customers = clean_customers(data[1])
        logger.info("Customer data cleaned successfully.")
        # Enrich and aggregate customer/transaction data

        return (cleaned_transactions, cleaned_customers)
    except Exception as e:
        logger.error(f"Data transformation failed: {str(e)}")
        raise
