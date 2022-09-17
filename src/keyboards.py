from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from states import *

start_menu_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Register', callback_data=REGISTER)
        ]
    ]
)


user_type_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('I am looking for content 🧞‍♀️', callback_data=REGISTER_USER)
        ],
        [
            InlineKeyboardButton('I am a content creator 🧜🏻‍♀️', callback_data=REGISTER_CONTENT_CREATOR)
        ]
    ]
)


registered_user_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Edit my profile 📜', callback_data='0'),
            InlineKeyboardButton('Find new content 🧞‍♀️', callback_data='0')
        ],
        [
            InlineKeyboardButton('My content creators 🧜🏻‍♀️', callback_data='0'),
            InlineKeyboardButton('Delete account 👋🏻', callback_data='0')
        ]
    ]
)
