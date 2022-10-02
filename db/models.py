from datetime import datetime
import json
import logging

from peewee import *

db = SqliteDatabase('../db/database.db')

logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)


class User(Model):
    user_id = IntegerField(primary_key=True)
    username = CharField()
    registration_date = DateTimeField(default=datetime.now())

    class Meta:
        database = db
        db_table = 'Users'


class ContentCreator(Model):
    content_creator_id = IntegerField(primary_key=True)
    first_name = CharField()
    last_name = CharField()
    email = CharField()
    birth_date = DateTimeField()
    country = CharField()
    registration_date = DateTimeField(default=datetime.now())

    class Meta:
        database = db
        db_table = 'ContentCreators'


class Channel(Model):
    channel_id = IntegerField(primary_key=True)
    owner_id = ForeignKeyField(ContentCreator, backref='channels')
    category = CharField()
    name = CharField()
    head_line = CharField()
    description = TextField()
    creation_date = DateTimeField(default=datetime.now())

    class Meta:
        database = db
        db_table = 'Channels'


class Following(Model):
    user_id = ForeignKeyField(User, backref='following')
    channel_id = ForeignKeyField(Channel, backref='followers')
    following_date = DateTimeField(default=datetime.now())

    class Meta:
        database = db
        db_table = 'Followings'
        primary_key = CompositeKey('user_id', 'content_creator_id')


db.create_tables([User, ContentCreator, Channel, Following])


def populate_tables_with_dummy_data(dummy_data_file='../db/dummy_data.json'):
    with open(dummy_data_file, 'r', encoding='utf-8') as f:
        dummy_data = json.load(f)

    for user in dummy_data.get('users'):
        User.create(
            user_id=user.get('user_id'),
            username=user.get('username')
        ).save()

    for content_creator in dummy_data.get('content_creators'):
        ContentCreator.create(
            content_creator_id=content_creator.get('content_creator_id'),
            first_name=content_creator.get('first_name'),
            country=content_creator.get('country'),
            age=content_creator.get('age'),
            bio=content_creator.get('bio'),
            profile_pic=f"../static/{content_creator.get('content_creator_id')}.jpg"
        ).save()


# populate_tables_with_dummy_data()
