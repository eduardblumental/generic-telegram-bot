from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from .states import *

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