from datetime import datetime
from peewee import *

db = SqliteDatabase('../db/database.db')


class Users(Model):
    user_id = IntegerField(primary_key=True)
    first_name = CharField()
    registration_date = DateTimeField(default=datetime.now())

    class Meta:
        database = db
        db_table = 'Users'


class ContentCreators(Model):
    user_id = IntegerField(primary_key=True)
    first_name = CharField()
    country = CharField()
    birth_date = DateField()
    bio = TextField()
    profile_pic = CharField()
    registration_date = DateTimeField(default=datetime.now())

    class Meta:
        database = db
        db_table = 'ContentCreators'


db.create_tables([Users, ContentCreators])
