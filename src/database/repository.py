import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine

from src.database.schema import ML_SCHEMA
from src.exception import CustomException
from src.logger import logger

RAW_LOAN_TABLE = "raw_loan_defaults"

def load_raw_loan_data(
        dataframe: pd.DataFrame
        ,engine: Engine
        ,replace_existing: bool=False
) -> int:
    try:
        row_count = len(dataframe)

        logger.info(
            "Starting raw loan-data load: %s rows into %s.%s"
            ,row_count
            ,ML_SCHEMA
            ,RAW_LOAN_TABLE
        )

        with engine.begin() as connection:
            if replace_existing:
                logger.info(
                    "Removing existing rows from %s.%s"
                    ,ML_SCHEMA
                    ,RAW_LOAN_TABLE
                )

                connection.execute(
                    text(
                        f""
                    )
                )