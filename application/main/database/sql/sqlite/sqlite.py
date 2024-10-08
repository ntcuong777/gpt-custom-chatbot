from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

sqlite_engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sqlite_engine)

Base = declarative_base()


# Dependency
def get_db_session():
    """Get a single DB session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
