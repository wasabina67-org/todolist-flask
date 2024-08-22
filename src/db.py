from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

url = "sqlite:///mydb.db"
engine = create_engine(url)
session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)  # noqa


@contextmanager
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
