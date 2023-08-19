from sqlalchemy.orm import declarative_base
from bootstrap_config import app_config, bootstrap_config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


if (app_config.get("DATABASE_URL", None) is None):
    bootstrap_config()

engine = create_engine(app_config["DATABASE_URL"], echo=True,
                       pool_size=20, max_overflow=30)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)


def get_db_script():
    try:
        db = SessionLocal()
        return db
    finally:
        db.close()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
