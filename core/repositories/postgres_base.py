from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


SQLite_test = 'sqlite:///./vacancies.db'

Base = declarative_base()

engine = create_engine(
    SQLite_test,
    echo=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


@contextmanager
def get_db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def create_tables():
    with engine.begin() as conn:
        Base.metadata.create_all(conn)


def init_db():
    create_tables()
