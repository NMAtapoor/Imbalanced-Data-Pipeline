import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

def load_abalone_to_db(df: pd.DataFrame):
    
    # Load environment variables from .env
    load_dotenv(dotenv_path="../.env.dev")
    # Read DB credentials from .env
    username = os.getenv("SOURCE_DB_USER")
    password = os.getenv("SOURCE_DB_PASSWORD")
    host = os.getenv("SOURCE_DB_HOST")
    port = os.getenv("SOURCE_DB_PORT")
    database = os.getenv("SOURCE_DB_NAME")
    
    # Create SQLAlchemy engine
    db_engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}")

    # Write to PostgreSQL
    df.to_sql("atapoor_capstone_project", db_engine, schema="de_2506_a", if_exists="replace", index=False)
