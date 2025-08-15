import pandas as pd
from src.extract.extract import extract_data
from src.transform.transform import transform_data

"""
Integration Tests for Extract-Transform Data Flow

These tests validate the integration between the extract and transform phases
of the ETL pipeline, ensuring data flows correctly between components.

Test Coverage:
1. Data Flow Integration: Verifies extracted data is properly consumed by transform
2. Data Consistency: Ensures data relationships are maintained across phases
3. Error Propagation: Tests how failures in one phase affect the other
4. Data Quality Validation: Confirms transform operations work on real extracted data
5. Cross-Phase Compatibility: Validates data structure compatibility between phases

Integration Tests focus on:
- Multiple components working together (extract + transform)
- Real data flow between phases using actual data sources
- Data integrity across component boundaries
- Error handling between integrated components
- Validation of data transformations on real extracted data

This differs from other test types by:
- Testing component interaction rather than isolation
- Using real data sources for realistic integration scenarios
- Validating data flow and compatibility between phases
- Testing cross-component error handling and data consistency
- Focusing on the handoff between extract and transform operations

Note: These tests use real database and CSV data sources to ensure
realistic integration scenarios and data compatibility validation.
"""




def test_extract_to_transform_data_flow():
    """Integration test: Extract data flows correctly into transform"""
    # Extract phase
    raw_transactions, raw_customers = extract_data()

    # Verify extract produced valid data
    assert isinstance(raw_transactions, pd.DataFrame)
    assert isinstance(raw_customers, pd.DataFrame)
    assert not raw_transactions.empty
    assert not raw_customers.empty

    # Transform phase using extracted data
    cleaned_transactions, cleaned_customers = transform_data(
        (raw_transactions, raw_customers)
    )

    # Verify transform processed the data
    assert isinstance(cleaned_transactions, pd.DataFrame)
    assert isinstance(cleaned_customers, pd.DataFrame)
    assert not cleaned_transactions.empty
    assert not cleaned_customers.empty

    # Verify data quality improvements
    assert len(cleaned_transactions) <= len(
        raw_transactions
    )  # Cleaning removes rows
    assert len(cleaned_customers) <= len(
        raw_customers
    )  # Cleaning removes rows

    # Verify expected columns after transformation
    assert "customer_id" in cleaned_transactions.columns
    assert "customer_id" in cleaned_customers.columns
    assert "is_active" in cleaned_customers.columns
    assert "age" not in cleaned_customers.columns  # Age should be removed


def test_extract_transform_error_handling():
    """Integration test: Error handling between extract and transform"""
    # This would test scenarios where extract succeeds but transform fails
    # with the actual extracted data structure
    raw_transactions, raw_customers = extract_data()

    # Corrupt the data to test error handling
    corrupted_customers = raw_customers.drop(columns=["country", "is_active"])

    try:
        transform_data((raw_transactions, corrupted_customers))
        assert False, "Expected transform to fail with missing columns"
    except KeyError as e:
        assert "country" in str(e) or "is_active" in str(e)


def test_extract_transform_data_consistency():
    """
    Integration test: Data consistency between extract and transform phases
    """
    raw_transactions, raw_customers = extract_data()
    cleaned_transactions, cleaned_customers = transform_data(
        (raw_transactions, raw_customers)
    )

    # Verify customer IDs are consistent
    raw_customer_ids = set(raw_customers["customer_id"].dropna())
    cleaned_customer_ids = set(cleaned_customers["customer_id"].dropna())

    # Cleaned should be subset of raw (some may be removed due to missing data)
    assert cleaned_customer_ids.issubset(raw_customer_ids)

    # Verify transaction customer IDs still reference valid customers
    transaction_customer_ids = set(
        cleaned_transactions["customer_id"].dropna()
    )
    # Some overlap should exist
    # (though not necessarily complete due to cleaning)
    assert len(transaction_customer_ids.intersection(cleaned_customer_ids)) > 0
