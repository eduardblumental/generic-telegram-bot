from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from .states import CHANGE_USER_DATA, FIND_MODELS, MY_MODELS, DELETE_ACCOUNT

registered_user_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Change username 📜', callback_data=CHANGE_USER_DATA),
            InlineKeyboardButton('Find new models 🧞‍♀️', callback_data=FIND_MODELS)
        ],
        [
            InlineKeyboardButton('My models 🧜🏻‍♀️', callback_data=MY_MODELS),
            InlineKeyboardButton('Delete account 👋🏻', callback_data=DELETE_ACCOUNT)
        ]
    ]
)