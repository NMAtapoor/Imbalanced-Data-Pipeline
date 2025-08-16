import os
import logging
import pandas as pd
import timeit
from src.utils.logging_utils import setup_logger, log_extract_success

# Define the file path for the customers CSV file
FILE_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "data",
    "raw",
    "unclean_abalone.csv",
)

# Configure the logger
logger = setup_logger(__name__, "extract_data.log", level=logging.DEBUG)

EXPECTED_PERFORMANCE = 0.0001

TYPE = "ABALONE from CSV"


def extract_abalone() -> pd.DataFrame:
    start_time = timeit.default_timer()

    try:
        abalone_df = pd.read_csv(FILE_PATH)
        extract_abalone_execution_time = timeit.default_timer() - start_time
        log_extract_success(
            logger,
            TYPE,
            abalone_df.shape,
            extract_abalone_execution_time,
            EXPECTED_PERFORMANCE,
        )
        return abalone_df
    except Exception as e:
        logger.setLevel(logging.ERROR)
        logger.error(f"Error loading {FILE_PATH}: {e}")
        raise Exception(f"Failed to load CSV file: {FILE_PATH}")
