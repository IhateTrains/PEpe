from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Databases(Base):
    __tablename__ = 'bases'
    id = Column(Integer, primary_key=True)
    name = Column(String, default="dupa")
