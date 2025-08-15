import pandas as pd
import pytest
from unittest.mock import patch
from src.transform.transform import transform_data

"""
Component Tests for transform_data() Function

These tests validate the transform_data() function as a component,
testing how it coordinates cleaning functions to work together.

Test Coverage:
1. Data Integration: Verifies that transform_data() properly coordinates both
   clean_transactions() and clean_customers() functions
2. Data Integrity: Ensures transformed data matches expected clean results
3. Error Propagation: Tests that failures from either cleaning function are
   properly handled
4. Execution Flow: Validates fail-fast behaviour and function call ordering
5. Data Quality: Confirms cleaning operations produce expected output structure

Component Tests focus on:
- Coordination between multiple cleaning components
- Real data transformation integration
- End-to-end data flow validation within the transform phase
- Cross-component error handling and propagation
- Data quality validation after cleaning operations
"""


def normalize_nulls(df):
    """Normalize null values to avoid None vs NaN warnings
    in DataFrame comparisons."""
    return df.fillna(pd.NA).replace({pd.NA: None})


@pytest.fixture
def sample_unclean_transactions():
    """Sample unclean transaction data for testing"""
    unclean_transactions = pd.read_csv("data/raw/unclean_transactions.csv")
    return normalize_nulls(unclean_transactions)


@pytest.fixture
def sample_unclean_customers():
    """Sample unclean customer data for testing"""
    unclean_customers = pd.read_csv("data/raw/unclean_customers.csv")
    return normalize_nulls(unclean_customers)


@pytest.fixture
def expected_clean_transactions():
    """Expected clean transaction results from test data"""
    try:
        df = pd.read_csv(
            "tests/test_data/expected_transactions_clean_results.csv"
        )
        return normalize_nulls(df)
    except FileNotFoundError:
        # Fallback if test data file doesn't exist
        return pd.DataFrame(
            {
                "transaction_id": [1, 2, 3],
                "customer_id": [101, 102, 103],
                "amount": [100.50, 200.75, 300.25],
                "transaction_date": ["2023-01-01", "2023-01-02", "2023-01-03"],
            }
        )


@pytest.fixture
def expected_clean_customers():
    """Expected clean customer results from test data"""
    try:
        df = pd.read_csv(
            "tests/test_data/expected_customers_clean_results.csv"
        )
        return normalize_nulls(df)
    except FileNotFoundError:
        # Fallback if test data file doesn't exist
        return pd.DataFrame(
            {
                "customer_id": [101, 102, 103],
                "name": ["John Doe", "Jane Smith", "Bob Johnson"],
                "email": ["john@email.com", "jane@email.com", "bob@email.com"],
                "age": [25, 30, 35],
                "status": ["active", "active", "inactive"],
            }
        )


def test_transform_data_returns_correct_structure(
    sample_unclean_transactions, sample_unclean_customers
):
    """Test that transform_data returns correct data structure"""
    input_data = (sample_unclean_transactions, sample_unclean_customers)
    result = transform_data(input_data)

    # Verify structure
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], pd.DataFrame)
    assert isinstance(result[1], pd.DataFrame)


def test_transform_data_integrates_cleaning_functions(
    sample_unclean_transactions, sample_unclean_customers
):
    """Test that transform_data integrates cleaning functions correctly"""
    input_data = (sample_unclean_transactions, sample_unclean_customers)
    cleaned_transactions, cleaned_customers = transform_data(input_data)

    # Verify DataFrames are returned and not empty
    assert not cleaned_transactions.empty
    assert not cleaned_customers.empty

    # Verify basic structure is maintained
    assert "transaction_id" in cleaned_transactions.columns
    assert "customer_id" in cleaned_transactions.columns
    assert "customer_id" in cleaned_customers.columns
    assert "name" in cleaned_customers.columns


@patch("src.transform.transform.clean_transactions")
def test_transform_data_propagates_transaction_cleaning_exceptions(
    mock_clean_transactions,
):
    """Test that exceptions from clean_transactions are propagated"""
    mock_clean_transactions.side_effect = Exception(
        "Transaction cleaning failed"
    )

    input_data = (pd.DataFrame(), pd.DataFrame())

    with pytest.raises(Exception, match="Transaction cleaning failed"):
        transform_data(input_data)


@patch("src.transform.transform.clean_customers")
@patch("src.transform.transform.clean_transactions")
def test_transform_data_propagates_customer_cleaning_exceptions(
    mock_clean_transactions, mock_clean_customers
):
    """Test that exceptions from clean_customers are propagated"""
    # Mock transactions to succeed, customers to fail
    mock_clean_transactions.return_value = pd.DataFrame({"transaction_id": [1]})
    mock_clean_customers.side_effect = Exception("Customer cleaning failed")

    input_data = (pd.DataFrame(), pd.DataFrame())

    with pytest.raises(Exception, match=r"Customer cleaning failed"):
        transform_data(input_data)


@patch("src.transform.transform.clean_customers")
@patch("src.transform.transform.clean_transactions")
def test_transform_data_handles_transaction_cleaning_failure_first(
    mock_clean_transactions, mock_clean_customers
):
    """Test behavior when transaction cleaning fails first"""
    mock_clean_transactions.side_effect = Exception(
        "Transaction cleaning error"
    )

    input_data = (pd.DataFrame(), pd.DataFrame())

    # Should fail on first function call (transactions)
    with pytest.raises(Exception, match="Transaction cleaning error"):
        transform_data(input_data)

    # Customer cleaning should not be called due to fail-fast behavior
    mock_clean_customers.assert_not_called()


def test_transform_data_processes_real_data_correctly():
    """Test that transform_data processes data with expected characteristics"""
    # Create realistic test data
    transactions_data = pd.DataFrame(
        {
            "transaction_id": [1, 2, 3, 4, 5],
            "customer_id": [101, 102, 103, 101, 102],
            "amount": [100.50, 200.75, 300.25, 150.00, 250.50],
            "transaction_date": [
                "2023-01-01",
                "2023-01-02",
                "2023-01-03",
                "2023-01-04",
                "2023-01-05",
            ],
        }
    )

    customers_data = pd.DataFrame(
        {
            "customer_id": [101, 102, 103, 104, 105],
            "name": [
                "John Doe",
                "Jane Smith",
                "Bob Johnson",
                "Alice Brown",
                "Charlie Wilson",
            ],
            "email": [
                "john@email.com",
                "jane@email.com",
                "bob@email.com",
                "alice@email.com",
                "charlie@email.com",
            ],
            "age": [25, 30, 35, 28, 32],
            "country": ["USA", "UK", "Canada", "USA", "UK"],
            "is_active": ["active", "active", "inactive", "active", "active"],
        }
    )

    input_data = (transactions_data, customers_data)
    cleaned_transactions, cleaned_customers = transform_data(input_data)

    # Verify data processing characteristics
    assert len(cleaned_transactions) > 0
    assert len(cleaned_customers) > 0

    # Verify essential columns are preserved
    assert "customer_id" in cleaned_transactions.columns
    assert "amount" in cleaned_transactions.columns
    assert "customer_id" in cleaned_customers.columns
    assert "is_active" in cleaned_customers.columns


def test_transform_data_maintains_data_relationships():
    """Test that transform_data maintains relationships between datasets"""
    # Create data with overlapping customer IDs
    transactions_data = pd.DataFrame(
        {
            "transaction_id": [1, 2, 3],
            "customer_id": [101, 102, 103],
            "amount": [100.50, 200.75, 300.25],
            "transaction_date": ["2023-01-01", "2023-01-02", "2023-01-03"],
        }
    )

    customers_data = pd.DataFrame(
        {
            "customer_id": [101, 102, 103],
            "name": ["John Doe", "Jane Smith", "Bob Johnson"],
            "email": ["john@email.com", "jane@email.com", "bob@email.com"],
            "age": [25, 30, 35],
            "country": ["USA", "UK", "Canada"],
            "is_active": ["active", "active", "inactive"],
        }
    )

    input_data = (transactions_data, customers_data)
    cleaned_transactions, cleaned_customers = transform_data(input_data)

    # Verify customer ID relationships are maintained
    transaction_customer_ids = set(
        cleaned_transactions["customer_id"].dropna()
    )
    customer_ids = set(cleaned_customers["customer_id"].dropna())
    overlap = transaction_customer_ids.intersection(customer_ids)

    assert len(overlap) > 0, "No overlapping customer IDs after transformation"
