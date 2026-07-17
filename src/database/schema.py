from sqlalchemy import text
from sqlalchemy.engine import Engine

from src.exception import CustomException
from src.logger import logger

ML_SCHEMA = "ml"
API_SCHEMA = "api"

def create_database_schemas(engine: Engine) -> None:
    try:
        logger.info("[schema.py] Ensuring database schemas exist: %s, %s"
                    ,ML_SCHEMA
                    ,API_SCHEMA)
        
        with engine.begin() as connection:
            connection.execute(
                text("CREATE SCHEMA IF NOT EXISTS ml")
            )

            connection.execute(
                text("CREATE SCHEMA IF NOT EXISTS api")
            )

            logger.info(
                "[schema.py] Database schemas ensured: %s, %s"
                ,ML_SCHEMA
                ,API_SCHEMA
            )

    except Exception as exc:
        logger.exception(
            "[schema.py] Failed to create database schemas: %s, %s"
            ,ML_SCHEMA
            ,API_SCHEMA
            )
        raise CustomException(exc) from exc