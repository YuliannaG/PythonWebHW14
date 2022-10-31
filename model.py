from datetime import datetime

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import DateTime

Base = declarative_base()


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, autoincrement=True)
    img_url = Column(String(250), nullable=False)
    rating = Column(Integer, nullable=False)
    title = Column(String(150), nullable=False, unique=False)
    created = Column(DateTime, default=datetime.now())
    author = Column(String(150), nullable=True, unique=False)
    category = Column(String(150), nullable=False, unique=False)
    position_in_category = Column(Integer)
    available = Column(String(150), nullable=False, unique=False)

