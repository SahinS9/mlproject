from sqlalchemy.engine import Engine

from src.database.base import Base
from src.database.engine import engine as database_engine
from src.database.models import ml_models, api_models
from src.database.schema import create_database_schemas
from src.exception import CustomException
from src.logger import logger

def initialize_database(engine: Engine) -> None:
    try:
        logger.info("Starting database initialization")

        create_database_schemas(engine)

        logger.info(
            "Registered database tables: %s"
            ,list(Base.metadata.tables.keys())
        )

        Base.metadata.create_all(bind=engine)

        logger.info(
                    "Database tables ensured successfully: %s",
                    list(Base.metadata.tables.keys()),
                )

        logger.info("Database initialization completed successfully")

    except Exception as exc:
        logger.exception("Database initialization failed")
        raise CustomException(exc) from exc

if __name__=="__main__":
    initialize_database(database_engine)