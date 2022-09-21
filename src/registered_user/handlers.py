from telegram import Update
from telegram.ext import ContextTypes

from .keyboards import registered_user_keyboard

from .changing_user_data.handlers import change_user_data_conversation

DEFAULT = ContextTypes.DEFAULT_TYPE


async def registered_user_start(update: Update, context: DEFAULT):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="So, what's the plan?",
        reply_markup=registered_user_keyboard)


registered_user_handlers = [
    change_user_data_conversation
]
