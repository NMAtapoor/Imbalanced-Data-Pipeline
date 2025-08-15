import pandas as pd
import logging
from src.utils.logging_utils import setup_logger
from src.utils.db_utils import QueryExecutionError

# Configure the logger
logger = setup_logger(__name__, "database_query.log", level=logging.DEBUG)


def execute_extract_query(query, connection):
    try:
        return pd.read_sql_query(query, connection)
    except pd.errors.DatabaseError as e:
        logger.setLevel(logging.ERROR)
        logger.error(f"Failed to execute query: {e}")
        logger.error(f"The query that failed was: {query}")
        raise QueryExecutionError(f"Failed to execute query: {e}")
