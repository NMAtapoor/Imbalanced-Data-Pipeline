import pandas as pd
import pytest
import timeit
from unittest.mock import patch
from src.extract.extract_transactions import (
    extract_transactions,
    EXPECTED_IMPORT_RATE,
)

"""
Component Tests for extract_transactions() Function

These tests validate the extract_transactions() function as a complete 
component, testing its behaviour with real database connections and actual SQL
queries.

Test Coverage:
1. Data Integrity: Verifies extracted data matches expected database results 
exactly
2. Performance: Ensures extraction meets database query performance requirements
3. Database Connection Errors: Tests proper exception handling for connection 
failures
4. SQL Query Errors: Tests handling of malformed SQL syntax
5. Query Execution Errors: Tests handling of runtime database errors 
(missing tables, permissions)

Component tests differ from unit tests by:
- Using real database connections and SQL queries
- Testing the complete function behaviour end-to-end
- Validating integration with database, SQL utilities, and pandas
- Using mocking only for error simulation, not normal operation
- Ensuring production-like database performance requirements are met

Note: Null value normalization is used to handle differences between database 
NULL and pandas NaN values during DataFrame comparisons.
"""


def normalize_nulls(df):
    """Normalize null values to avoid None vs NaN
    warnings in DataFrame comparisons."""
    return df.fillna(pd.NA).replace({pd.NA: None})


@pytest.fixture
def expected_unclean_transactions():
    df = pd.read_csv("data/raw/unclean_transactions.csv")
    return normalize_nulls(df)


def test_extract_transactions_returns_correct_dataframe(
    expected_unclean_transactions,
):
    # Call the function to get the DataFrame
    df = extract_transactions()

    # Normalize null values to avoid None vs NaN warnings
    df = normalize_nulls(df)

    # Verify the DataFrame is the same as the expected unclean transactions
    pd.testing.assert_frame_equal(
        df, expected_unclean_transactions, check_dtype=False
    )


def test_extract_transaction_performance():
    # Note the change in the performance expectation
    # Measure the execution time
    execution_time = timeit.timeit(
        "extract_transactions()", globals=globals(), number=1
    )

    # Call the function to get the DataFrame
    df = extract_transactions()

    # Mean Time per Row
    actual_execution_time_per_row = execution_time / df.shape[0]

    # Assert that the execution time is within an acceptable range
    assert actual_execution_time_per_row <= EXPECTED_IMPORT_RATE, (
        f"Expected execution time to be less than or equal to "
        f"{str(EXPECTED_IMPORT_RATE)} seconds, but got "
        f"{str(actual_execution_time_per_row)} seconds"
    )


@patch("src.extract.extract_transactions.load_db_config")
def test_extract_transactions_database_connection_failure(mock_load_db_config):
    # Mock invalid database configuration
    mock_load_db_config.return_value = {
        "source_database": {
            "dbname": "nonexistent_db",
            "user": "invalid_user",
            "password": "wrong_password",
            "host": "invalid_host",
            "port": "9999",
        }
    }

    with pytest.raises(Exception, match="Failed to extract data"):
        extract_transactions()


@patch("src.extract.extract_transactions.import_sql_query")
def test_extract_transactions_sql_query_error(mock_import_sql_query):
    # Mock invalid SQL query
    mock_import_sql_query.return_value = "INVALID SQL SYNTAX SELECT FROM WHERE"

    with pytest.raises(Exception, match="Failed to extract data"):
        extract_transactions()


@patch("src.extract.extract_transactions.execute_extract_query")
def test_extract_transactions_query_execution_error(mock_execute_query):
    # Mock query execution failure
    mock_execute_query.side_effect = Exception(
        "Table 'transactions' doesn't exist"
    )

    with pytest.raises(Exception, match="Failed to extract data"):
        extract_transactions()
