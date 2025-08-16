import pandas as pd
#from src.extract.extract_transactions import extract_transactions
from src.extract.extract_abalone import extract_abalone
from src.utils.logging_utils import setup_logger

logger = setup_logger("extract_data", "extract_data.log")


def extract_data() -> pd.DataFrame:
    try:
        logger.info("Starting data extraction process")

        #transactions = extract_transactions()
        abalone_df = extract_abalone()

        logger.info(
            f"Data extraction completed successfully - "
            f"Customers: {abalone_df.shape}"
        )

        return abalone_df

    except Exception as e:
        logger.error(f"Data extraction failed: {str(e)}")
        raise
