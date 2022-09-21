from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from .states import REGISTER, LEARN_MORE, REGISTER_USER, REGISTER_CONTENT_CREATOR


unregistered_user_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Register ', callback_data=REGISTER),
            InlineKeyboardButton('Learn more', callback_data=LEARN_MORE),
        ]
    ]
)

registration_type_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('I am looking for content 🧞‍♀️', callback_data=REGISTER_USER)
        ],
        [
            InlineKeyboardButton('I am a content creator 🧜🏻‍♀️', callback_data=REGISTER_CONTENT_CREATOR)
        ]
    ]
)