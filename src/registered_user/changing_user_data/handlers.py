from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

from db.models import Users

from ..states import CHANGE_USER_DATA
from .states import USERNAME

DEFAULT = ContextTypes.DEFAULT_TYPE
END = ConversationHandler.END


async def q_handle_change_user_data(update: Update, context: DEFAULT):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text('Okay, type in a new username.')

    return USERNAME


async def handle_change_username(update: Update, context: DEFAULT):
    user_id = update.effective_user.id
    new_username = update.message.text

    q = Users.update({Users.username: new_username}).where(Users.user_id == user_id)
    q.execute()

    await update.message.reply_text(
        text=f'Nice! You username is now {new_username}. Use /start command to continue.')
    return END


async def handle_error(update: Update, context: DEFAULT):
    await update.message.reply_text(f'I am not sure what "{update.message.text}" means. Please, retype your new username.')


change_user_data_conversation = ConversationHandler(
    entry_points=[CallbackQueryHandler(callback=q_handle_change_user_data, pattern=f'^{CHANGE_USER_DATA}$')],
    states={
        USERNAME: [
            MessageHandler(filters=filters.TEXT and ~filters.COMMAND, callback=handle_change_username)
        ]
    },
    fallbacks=[MessageHandler(filters=filters.ALL, callback=handle_error)]
)
