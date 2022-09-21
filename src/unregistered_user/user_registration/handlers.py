from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

from db.models import Users
from .states import USERNAME
from ..states import REGISTER_USER

DEFAULT = ContextTypes.DEFAULT_TYPE
END = ConversationHandler.END


async def q_handle_start_registration(update: Update, context: DEFAULT):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text="Please, type in your username. Don't hesitate to get creative 😉")
    return USERNAME


async def handle_username(update: Update, context: DEFAULT):
    user_id = update.effective_user.id
    username = update.message.text

    user = Users.create(user_id=user_id, username=username)
    user.save()

    await update.message.reply_text(
        text=f'Welcome to the club {username}! Use /start command to continue.')
    return END


async def handle_error(update: Update, context: DEFAULT):
    await update.message.reply_text(f'I am not sure what "{update.message.text}" means. Please, retype your username.')


register_user_conversation = ConversationHandler(
    entry_points=[CallbackQueryHandler(callback=q_handle_start_registration, pattern=f'^{REGISTER_USER}$')],
    states={
        USERNAME: [
            MessageHandler(filters=(filters.TEXT and ~filters.COMMAND), callback=handle_username)
        ]
    },
    fallbacks=[MessageHandler(filters=filters.ALL, callback=handle_error)]
)