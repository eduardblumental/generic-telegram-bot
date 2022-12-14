from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from .states import REGISTER, LEARN_MORE, REGISTER_USER, REGISTER_CONTENT_CREATOR


unregistered_user_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Register π¦Έπ»ββοΈ', callback_data=REGISTER),
            InlineKeyboardButton('Learn more π¨π»βπ»', callback_data=LEARN_MORE, url='https://en.wikipedia.org')
        ]
    ]
)

registration_type_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('I am looking for content π¦Έπ»ββοΈ', callback_data=REGISTER_USER)
        ],
        [
            InlineKeyboardButton('I am a content creator π§π»ββοΈ', callback_data=REGISTER_CONTENT_CREATOR)
        ]
    ]
)