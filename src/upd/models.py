from typing import Optional

from PySide6.QtGui import QPixmap
from contextlib import contextmanager
from sqlalchemy import Column, Integer, String, Text, Sequence, ForeignKey, Date, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref, aliased

from peewee import *

db = SqliteDatabase('people.db')

class RBaseModel(Model):

    class Meta:
        database = db # This model uses the "people.db" database.
