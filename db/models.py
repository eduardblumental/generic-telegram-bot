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
    content_creator_id = IntegerField(primary_key=True)
    first_name = CharField()
    country = CharField()
    age = IntegerField()
    bio = TextField()
    profile_pic = CharField()
    channel_id = IntegerField(null=True)
    registration_date = DateTimeField(default=datetime.now())

    class Meta:
        database = db
        db_table = 'ContentCreators'


class Followings(Model):
    user_id = IntegerField()
    content_creator_id = IntegerField()
    following_date = DateTimeField(default=datetime.now())

    class Meta:
        database = db
        db_table = 'ContentCreators'
        primary_key = CompositeKey('user_id', 'content_creator_id')


db.create_tables([Users, ContentCreators, Followings])
