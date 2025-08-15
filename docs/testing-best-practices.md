# Unit Testing Best Practices for ETL Functions

## Problem: Database Dependencies in Unit Tests

When testing ETL functions that interact with databases, you should **always mock external dependencies** to avoid:

- ❌ Actual database connections
- ❌ Real configuration files with sensitive data
- ❌ Network calls
- ❌ File system dependencies
- ❌ Slow test execution

## Solution: Mock All External Dependencies

### ✅ What to Mock in ETL Tests

1. **Database Connections**

   ```python
   mocker.patch("module.get_db_connection", return_value=mock_connection)
   ```

2. **Configuration Loading**

   ```python
   mocker.patch("module.load_db_config", return_value=mock_config)
   ```

3. **SQL Query Files**

   ```python
   mocker.patch("module.import_sql_query", return_value="SELECT * FROM test")
   ```

4. **Database Query Execution**

   ```python
   mocker.patch("module.execute_extract_query", return_value=mock_dataframe)
   ```

5. **File Operations**

   ```python
   mocker.patch("builtins.open", mock_open(read_data="test data"))
   ```

## Example: Fixed Test for extract_transactions

### Before (❌ Bad - Real Dependencies)

```python
def test_extract_transactions():
    # This will try to connect to real database!
    result = extract_transactions()  # FAILS with config errors
```

### After (✅ Good - Mocked Dependencies)

```python
def test_extract_transactions_execution_mocked(mocker):
    # Mock database config
    mock_db_config = {"source_database": {"host": "test", "port": "5432"}}
    mocker.patch("module.load_db_config", return_value=mock_db_config)
    
    # Mock SQL query
    mocker.patch("module.import_sql_query", return_value="SELECT * FROM test")
    
    # Mock database connection
    mock_connection = MagicMock()
    mocker.patch("module.get_db_connection", return_value=mock_connection)
    
    # Mock query execution result
    mock_df = pd.DataFrame({'id': [1, 2], 'amount': [100, 200]})
    mocker.patch("module.execute_extract_query", return_value=mock_df)
    
    # Test the function
    result = extract_transactions_execution()
    
    # Verify results
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    mock_connection.close.assert_called_once()
```

## Benefits of Proper Mocking

1. **Fast Tests** - No network or database delays
2. **Reliable Tests** - No external dependencies to fail
3. **Isolated Testing** - Test only your business logic
4. **Predictable Results** - Control exactly what data is returned
5. **Security** - No need for real database credentials in tests

## Integration vs Unit Tests

- **Unit Tests**: Mock everything external (database, files, network)
- **Integration Tests**: Test with real databases (separate test database)
- **End-to-End Tests**: Test full pipeline with real infrastructure

## Key Takeaway

**Unit tests should never touch real external resources.** Always mock:

- Database connections
- File system operations  
- Network requests
- Environment variables
- Configuration files
- Third-party APIs

This ensures your tests are fast, reliable, and focused on testing your code logic rather than external systems.
