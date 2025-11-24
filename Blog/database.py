from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

DB_URL = "postgresql+psycopg2://postgres:Iamironman2268$@localhost:2657/fastapiProject"
engine = create_engine(DB_URL)
session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()