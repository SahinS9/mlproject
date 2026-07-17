import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from src.exception import CustomException
from src.logger import logger

load_dotenv()


def create_database_engine() -> Engine:
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError(
            "DATABASE_URL is not configured in the [.env] file"
        )
    
    try:
        logger.info("Creating database engine")

        engine = create_engine(
            database_url
            ,pool_pre_ping=True
        )

        logger.info("Database engine created successfully")

        return engine
    
    except Exception as exc:
        logger.exception("Failed to create the database engine")
        raise CustomException(exc) from exc
    

def test_database_connection(engine: Engine) -> None:
    try:
        logger.info("Testing Neon PostgreSQL connection")

        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT 1")
            )

            result.scalar_one()

        logger.info("Neon PostgreSQL connection successful")

    except Exception(exc) as exc:
        logger.exception("Neon PostgreSQL connection failed")
        raise CustomException from exc
    

engine = create_database_engine()


if __name__=="__main__":
    test_database_connection(engine)