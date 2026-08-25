from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Render injects DATABASE_URL automatically once a Postgres database is
# attached to this web service (see setup steps below). Falls back to local
# SQLite when that variable isn't set — e.g. running this on your own laptop
# without a Postgres instance — so local development still works with zero
# extra setup.
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Render (and Heroku) hand out connection strings starting with
    # "postgres://", but SQLAlchemy 1.4+ requires the "postgresql://" scheme —
    # without this swap, create_engine() raises immediately on startup.
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URL = DATABASE_URL
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
else:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./focusbubble.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
