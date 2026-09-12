from __future__ import annotations

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from src.config import get_database_path


class Base(DeclarativeBase):
    pass


def get_engine(db_path: str | Path | None = None):
    target = db_path or get_database_path()
    database_url = f"sqlite:///{Path(target)}"
    return create_engine(database_url, connect_args={"check_same_thread": False}, future=True)


def get_session_factory(db_path: str | Path | None = None):
    return sessionmaker(bind=get_engine(db_path), autoflush=False, autocommit=False, future=True)


def get_db_session(db_path: str | Path | None = None):
    session_factory = get_session_factory(db_path)
    initialize_database(db_path)
    session = session_factory()
    try:
        yield session
    finally:
        session.close()


def initialize_database(db_path: str | Path | None = None):
    engine = get_engine(db_path)
    Base.metadata.create_all(bind=engine)
    return engine

