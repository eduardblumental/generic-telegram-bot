from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from .states import FOLLOW, UNFOLLOW, NEXT, PREVIOUS, BACK_TO_MENU


def get_find_model_keyboard(is_following):
    follow_button = InlineKeyboardButton('Follow ❤️', callback_data=FOLLOW)
    unfollow_button = InlineKeyboardButton('Unfollow 👋🏻 ', callback_data=UNFOLLOW)
    top_button = unfollow_button if is_following else follow_button

    return InlineKeyboardMarkup(
        [
            [top_button],
            [InlineKeyboardButton('⏪', callback_data=PREVIOUS), InlineKeyboardButton('⏩', callback_data=NEXT)],
            [InlineKeyboardButton('Back to menu 👀', callback_data=BACK_TO_MENU)]
        ]
    )
