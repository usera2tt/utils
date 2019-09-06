"""
SQLAlchemy==1.3.8
"""

from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.schema import MetaData

SQLALCHEMY_DATABASE_URI = ''

db_engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=db_engine)
session = Session()

db_metadata = MetaData()
db_metadata.reflect(bind=db_engine, only=['user'])  # table name


class DefaultBase(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__

    def __repr__(self):
        return '<%s>' % type(self).__name__


Base = declarative_base(cls=DefaultBase)


class User(Base):
    __table__ = db_metadata.tables['user']
