from numpy import str_
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric,DateTime
from sqlalchemy.orm import relationship
from database import Base
from setting import DATABASE_TABLE

class Movie(Base):
    __tablename__ = DATABASE_TABLE

    link = Column(String, primary_key=True, index=True)
    author = Column(String, index=True)
    title = Column(String, index=True)
    date = Column(DateTime)
    comment = Column(Integer, index=True)  # Column(Numeric(10,2))
    movie_type = Column(String, index=True)
