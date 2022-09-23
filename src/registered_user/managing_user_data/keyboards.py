from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from .states import YES, NO

delete_user_data_request_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Yes 🥲', callback_data=YES),
            InlineKeyboardButton('No 🥳', callback_data=NO)
        ]
    ]
)