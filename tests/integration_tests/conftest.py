import pytest
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from config.db_config import load_db_config

# Load test environment variables
project_root = Path(__file__).parent.parent.parent
test_env_path = project_root / ".env.test"
load_dotenv(test_env_path)


@pytest.fixture(scope="module", autouse=True)
def setup_test_transactions():
    """
    Set up the transactions table before integration tests in this module.
    This fixture runs once per test module for better performance.
    """
    config = load_db_config()
    target_db_config = config["target_database"]

    connection_string = (
        f"postgresql+psycopg://{target_db_config['user']}"
        f":{target_db_config['password']}@{target_db_config['host']}"
        f":{target_db_config['port']}/{target_db_config['dbname']}"
    )

    engine = create_engine(connection_string)
    sql_file_path = project_root / "data" / "raw" / "unclean_transactions.sql"

    try:
        with open(sql_file_path, "r") as file:
            sql_content = file.read()

        with engine.connect() as connection:
            # Drop table if exists and recreate
            connection.execute(text("DROP TABLE IF EXISTS transactions;"))
            connection.execute(text(sql_content))
            connection.commit()

    except Exception as e:
        # If there's an error, ensure we clean up properly
        with engine.connect() as connection:
            connection.rollback()
        raise RuntimeError(f"Failed to setup test transactions table: {e}")

    # Yield control to tests
    yield

    # Optional: Add cleanup after all tests in module complete
    # Uncomment if you want to clean up after each test module
    # try:
    #     with engine.connect() as connection:
    #         connection.execute(text("DROP TABLE IF EXISTS transactions;"))
    #         connection.commit()
    # except Exception:
    #     pass  # Ignore cleanup errors
