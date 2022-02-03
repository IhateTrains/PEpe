from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from database.Table import Table, Base


class Topic:

    def __init__(self, name):
        self.name = name
        self.engine = create_engine(f'sqlite:///{name}.db?')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def get_screens(self):
        return self.session.query(Table).all()

    def add_to_database(self, content, link):
        new_row = Table(content=content, link=link)
        self.session.add(new_row)
        self.session.commit()
