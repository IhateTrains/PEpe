from sqlalchemy import create_engine
from database.Databases import Base, Databases
from sqlalchemy.orm import sessionmaker
from Topic import Topic


class DatabseManager:

    def __init__(self):
        self.engine = create_engine('sqlite:///databases.db?')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.topics = []

    def get_databases(self):
        return self.session.query(Databases).all()

    def add_to_database(self, name):
        old = self.get_databases()
        for n in old:
            if name == n.name:
                print("Baza już istnienje")
                return
        new_row = Databases(name=name)
        self.session.add(new_row)
        self.session.commit()
        print(f"Dodano nową bazę o nazwie {name}")

    def load_databases(self):
        self.topics = []
        databases = self.get_databases()
        for database in databases:
            self.topics.append(Topic(database.name))
            
    def get_topics(self, name):
        powrot = []
        print(f'self.topics: {self.topics}')
        for n in self.topics:
            print(f'Get topics: {n.name}')
            if n.name == name:
                powrot.append(n)
        return powrot

