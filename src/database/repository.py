import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

from src.database.schema import ML_SCHEMA
from src.exception import CustomException
from src.logger import logger

RAW_LOAN_TABLE = "raw_loan_defaults"

def load_raw_loan_data(
        dataframe: pd.DataFrame
        ,engine: Engine
        ,replace_existing: bool = False
) -> int:
    try:
        if dataframe.empty:
            raise ValueError(
                "Cannot load raw loan data because DataFrame is empty"
            )
        row_count = len(dataframe)

        logger.info(
            "Starting raw loan data load: %s rows into %s.%s"
            ,row_count
            ,ML_SCHEMA
            ,RAW_LOAN_TABLE
        )

        with engine.begin() as connection:
            if replace_existing:
                logger.info(
                    "Truncating existing rows from %s.%s"
                    ,ML_SCHEMA
                    ,RAW_LOAN_TABLE
                )

                connection.execute(
                    text(
                        f'TRUNCATE TABLE "{ML_SCHEMA}".'
                        f'"{RAW_LOAN_TABLE}" RESTART IDENTITY'
                    )
                )

            logger.info(
                "Writing DataFrame to %s.%s in chunks"
                ,ML_SCHEMA
                ,RAW_LOAN_TABLE
            )

            dataframe.to_sql(
                name=RAW_LOAN_TABLE,
                con=connection,
                schema=ML_SCHEMA,
                if_exists="append",
                index=False,
                chunksize=500,
                method=None,
            )

        logger.info(
            "Raw loan data load completed successfully: %s rows"
            ,row_count
        )

        return row_count

    except SQLAlchemyError as exc:
        root_error = (
            str(exc.orig)
            if getattr(exc, "orig", None)
            else str(exc)
        )

        logger.error(
            "Database load failed for %s.%s: %s"
            ,ML_SCHEMA
            ,RAW_LOAN_TABLE
            ,root_error
        )

        clean_error = RuntimeError(
            f"Failed to laod data into "
            f"{ML_SCHEMA}.{RAW_LOAN_TABLE}: "
            f"{root_error}"
        )

        raise CustomException(clean_error) from None

    except Exception as exc:
        logger.exception(
            "Unexpected failure while loading data %s.%s"
            ,ML_SCHEMA
            ,RAW_LOAN_TABLE
        )
        raise CustomException(exc) from exc