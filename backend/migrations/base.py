from sqlalchemy.orm import DeclarativeBase

from csv_validator_pro.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
