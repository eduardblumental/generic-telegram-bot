from telegram import InlineKeyboardMarkup, InlineKeyboardButton

REGISTER_USER, REGISTER_CONTENT_CREATOR = map(str, range(2))

unregistered_user_start_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('I am looking for content 🧞‍♀️', callback_data=REGISTER_USER)
        ],
        [
            InlineKeyboardButton('I am a content creator 🧜🏻‍♀️', callback_data=REGISTER_CONTENT_CREATOR)
        ]
    ]
)


registered_user_start_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Edit my profile 📜', callback_data=''),
            InlineKeyboardButton('Find new content 🧞‍♀️', callback_data='')
        ],
        [
            InlineKeyboardButton('My content creators 🧜🏻‍♀️', callback_data=''),
            InlineKeyboardButton('Delete account 👋🏻', callback_data='')
        ]
    ]
)
