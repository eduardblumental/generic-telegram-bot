from telegram import Update
from telegram.ext import ContextTypes

from .keyboards import registered_user_keyboard

from .managing_user_data.handlers import managing_user_data_conversation
from .scrolling_models.handlers import scrolling_models_conversation

DEFAULT = ContextTypes.DEFAULT_TYPE


async def registered_user_start(update: Update, context: DEFAULT):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Let me know what's on your mind 🧞‍♀️",
        reply_markup=registered_user_keyboard)


registered_user_handlers = [
    managing_user_data_conversation,
    scrolling_models_conversation
]
