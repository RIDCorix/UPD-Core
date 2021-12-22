from typing import Optional

from PySide6.QtGui import QPixmap
from contextlib import contextmanager
from sqlalchemy import Column, Integer, String, Text, Sequence, ForeignKey, Date, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref, aliased

Base = declarative_base()
engine = create_engine('sqlite:///reminder.db')


class RBaseModel(Base):
    __abstract__ = True

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)

    def items(attr):
        if attr == 'objects':
            Session = sessionmaker(bind=engine)
            session = Session()
            return session.query(__class__)


class QuerySet:
    def __init__(self):
        self.fields = []
        self.filtrations = []

    def _copy(self):
        copy = QuerySet()
        copy.fields = self.fields
        copy.filtrations = self.filtrations
        return copy

    def all(self):
        return self._copy()

