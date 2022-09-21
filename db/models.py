from datetime import datetime
import json
import logging

from peewee import *

db = SqliteDatabase('../db/database.db')

logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


class Users(Model):
    user_id = IntegerField(primary_key=True)
    username = CharField()
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
    registration_date = DateTimeField(default=datetime.now())

    class Meta:
        database = db
        db_table = 'ContentCreators'


class Followings(Model):
    user_id = ForeignKeyField(Users, backref='following')
    content_creator_id = ForeignKeyField(ContentCreators, backref='followers')
    following_date = DateTimeField(default=datetime.now())

    class Meta:
        database = db
        db_table = 'Followings'
        primary_key = CompositeKey('user_id', 'content_creator_id')


db.create_tables([Users, ContentCreators, Followings])


def populate_tables_with_dummy_data(dummy_data_file='../db/dummy_data.json'):
    with open(dummy_data_file, 'r', encoding='utf-8') as f:
        dummy_data = json.load(f)

    for user in dummy_data.get('users'):
        Users.create(
            user_id=user.get('user_id'),
            username=user.get('username')
        ).save()

    for content_creator in dummy_data.get('content_creators'):
        ContentCreators.create(
            content_creator_id=content_creator.get('content_creator_id'),
            first_name=content_creator.get('first_name'),
            country=content_creator.get('country'),
            age=content_creator.get('age'),
            bio=content_creator.get('bio'),
            profile_pic=f"../static/{content_creator.get('content_creator_id')}.jpg"
        ).save()


# populate_tables_with_dummy_data()
