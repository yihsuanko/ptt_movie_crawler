from turtle import title
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship
from database import Base


class Movie(Base):
    __tablename__ = "movies"

    # id = Column(Integer, primary_key=True, index=True)
    author = Column(String, index=True)
    title = Column(String,primary_key=True, index=True)
    date = Column(String, index=True)
    comment = Column(Integer, index=True)  # Column(Numeric(10,2))

