from sqlalchemy import create_engine, text
from config.db_config import load_db_config


def test_transactions_table_exists():
    """Component test: Verify transactions table is properly set up."""
    config = load_db_config()
    target_db_config = config["target_database"]

    connection_string = (
        f"postgresql+psycopg://{target_db_config['user']}"
        f":{target_db_config['password']}@{target_db_config['host']}"
        f":{target_db_config['port']}/{target_db_config['dbname']}"
    )

    engine = create_engine(connection_string)

    with engine.connect() as connection:
        # Check table exists
        result = connection.execute(
            text(
                """
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'transactions'
            )
        """
            )
        )
        row = result.fetchone()
        assert row is not None and row[0] is True

        # Check it has data
        result = connection.execute(text("SELECT COUNT(*) FROM transactions"))
        row = result.fetchone()
        assert row is not None
        count = row[0]
        assert count == 10500
