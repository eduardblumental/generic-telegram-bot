from telegram import Update
from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

from keyboards import *
from db.models import Users, ContentCreators
from states import *

from unregistered_user.handlers import unregistered_user_handlers, unregistered_user_start
DEFAULT = ContextTypes.DEFAULT_TYPE


async def start(update: Update, context: DEFAULT):
    if Users.select().where(Users.user_id == update.effective_user.id):
        await update.message.reply_text(
            text="Welcome User!")
        return REGISTERED_USER
    elif ContentCreators.select().where(ContentCreators.content_creator_id == update.effective_user.id):
        await update.message.reply_text(
            text="Welcome Content Creator")
        return CONTENT_CREATOR
    else:
        await update.message.reply_text(
            text="Welcome unregistered user!")
        await unregistered_user_start(update, context)
        return UNREGISTERED_USER


async def random_message(update: Update, context: DEFAULT):
    await update.message.reply_text(
        text=f'I am not sure what "{update.message.text}" means 🤷🏻‍♀️\nPress /start to try again.')


main_conversation_handlers = [
    ConversationHandler(
        entry_points=[CommandHandler(command='start', callback=start)],
        states={
            UNREGISTERED_USER: unregistered_user_handlers,
            REGISTERED_USER: [],
            CONTENT_CREATOR: []
        },
        fallbacks=[CommandHandler(command='start', callback=start)]

    ),
    MessageHandler(filters=filters.TEXT, callback=random_message)
]
