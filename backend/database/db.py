from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import settings


engine = create_engine(settings.DATABASE_URL,
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
