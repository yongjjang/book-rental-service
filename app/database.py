from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import DB_URL

engine = create_engine(DB_URL, encoding='utf-8', max_overflow=-1)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

base = declarative_base()
base.query = db_session.query_property()


def init_db():
    base.metadata.create_all(engine)
