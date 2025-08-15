import pytest
import pandas as pd
from scripts.run_etl import main


@pytest.fixture
def mock_logger(mocker):
    return mocker.patch("scripts.run_etl.logger")


@pytest.fixture
def mock_setup_env(mocker):
    return mocker.patch("scripts.run_etl.setup_env")


@pytest.fixture
def mock_extract_data(mocker):
    mock_data = (
        pd.DataFrame({"id": [1, 2]}),
        pd.DataFrame({"name": ["Alice", "Bob"]}),
    )
    return mocker.patch("scripts.run_etl.extract_data", return_value=mock_data)


@pytest.fixture
def mock_transform_data(mocker):
    mock_data = pd.DataFrame(
        [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
    )
    return mocker.patch(
        "scripts.run_etl.transform_data", return_value=mock_data
    )


def test_main_success(
    mock_logger, mock_setup_env, mock_extract_data, mock_transform_data, mocker
):
    """Test successful ETL pipeline execution"""
    mocker.patch.dict("os.environ", {"ENV": "test"})

    result = main()

    # Verify function calls
    mock_setup_env.assert_called_once()
    mock_extract_data.assert_called_once()
    mock_transform_data.assert_called_once()

    # Verify logging
    mock_logger.info.assert_any_call(
        "Starting ETL pipeline in test environment"
    )
    mock_logger.info.assert_any_call("Beginning data extraction phase")
    mock_logger.info.assert_any_call("Data extraction phase completed")
    mock_logger.info.assert_any_call("Beginning the data transformation phase")
    mock_logger.info.assert_any_call("Data transformation phase completed")
    mock_logger.info.assert_any_call(
        "ETL pipeline completed successfully in test environment"
    )

    # Verify return value
    assert result is not None


def test_main_handles_extraction_error(mock_logger, mock_setup_env, mocker):
    """Test ETL pipeline handles extraction errors"""
    mocker.patch(
        "scripts.run_etl.extract_data", side_effect=Exception("Extract failed")
    )

    with pytest.raises(SystemExit):
        main()

    mock_logger.error.assert_called_once_with(
        "ETL pipeline failed: Extract failed"
    )
