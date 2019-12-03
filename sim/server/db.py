from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

db = SQLAlchemy()

Base = declarative_base()


class Animal(Base):
    __tablename__ = 'animals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    species = db.Column(db.String)

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'species': self.species,
        }


class Database(object):
    def __init__(self, config):
        self.config = config
        connection_string = 'sqlite:///{0}'.format(self.config['db'])
        self._engine = create_engine(connection_string)
        self._sessionmaker = sessionmaker(bind=self._engine)

    def create_session(self):
        return self._sessionmaker()
