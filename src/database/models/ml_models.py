from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Float, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.database.base import Base
from src.exception import CustomException
from src.logger import logger

from src.database.schema import ML_SCHEMA



class RawLoadDefault(Base):
    __tablename__ = "raw_loan_defaults"
    __table_args__ = {"schema": ML_SCHEMA}

    id: Mapped[int] = mapped_column(
        BigInteger
        ,primary_key=True
        ,autoincrement=True
    )

    loan_id: Mapped[str | None] = mapped_column(
        String
        ,nullable=True
        ,index=True
    )

    age: Mapped[int | None] = mapped_column(
        Integer
        ,nullable=True
    )

    income: Mapped[int | None] = mapped_column(
        BigInteger
        ,nullable=True
    )

    loan_amount: Mapped[int | None] = mapped_column(
        BigInteger
        ,nullable=True
    )

    credit_score: Mapped[int | None] = mapped_column(
        Integer
        ,nullable=True
    )

    months_employed: Mapped[int | None] = mapped_column(
        Integer
        ,nullable=True
    )

    num_credit_lines: Mapped[int | None] = mapped_column(
        Integer
        ,nullable=True
    )

    interest_rate: Mapped[float | None] = mapped_column(
        Float
        ,nullable=True
    )

    loan_term: Mapped[int | None] = mapped_column(
        Integer
        ,nullable=True
    )

    dti_ratio: Mapped[float | None] = mapped_column(
        Float
        ,nullable=True
    )

    education: Mapped[str | None] = mapped_column(
        String
        ,nullable=True
    )

    employment_type: Mapped[str | None] = mapped_column(
        String
        ,nullable=True
    )

    marital_status: Mapped[str | None] = mapped_column(
        String
        ,nullable=True
    )

    has_mortgage: Mapped[str | None] = mapped_column(
        String
        ,nullable=True
    )

    has_dependents: Mapped[str | None] = mapped_column(
        String
        ,nullable=True
    )

    loan_purpose: Mapped[str | None] = mapped_column(
        String
        ,nullable=True
    )

    has_cosigner: Mapped[str | None] = mapped_column(
        String
        ,nullable=True
    )

    default: Mapped[int | None] = mapped_column(
        Integer
        ,nullable=False
    )

    ingested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True)
        ,server_default=func.now()
        ,nullable=False
    )


