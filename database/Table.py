from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Table(Base):

    __tablename__ = 'PE'
    id = Column(Integer, primary_key=True)
    content = Column(String, default="dupa")
    link = Column(String, default="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/1024px-No_image_available.svg.png")

    def __repr__(self):
        return self.content
