from peewee import *

db = SqliteDatabase('people.db')

class RBaseModel(Model):

    class Meta:
        database = db # This model uses the "people.db" database just for test.

    removed = BooleanField(default=False) # for redo purposes
