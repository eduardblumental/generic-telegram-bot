from telegram import Update
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

from db.models import Users, ContentCreators
from states import *

from unregistered_user.handlers import unregistered_user_handlers, unregistered_user_start
from registered_user.handlers import registered_user_handlers, registered_user_start


DEFAULT = ContextTypes.DEFAULT_TYPE


async def start(update: Update, context: DEFAULT):
    if Users.select().where(Users.user_id == update.effective_user.id):
        await registered_user_start(update, context)
        return REGISTERED_USER
    elif ContentCreators.select().where(ContentCreators.content_creator_id == update.effective_user.id):
        await update.message.reply_text(
            text="Welcome Content Creator")
        return CONTENT_CREATOR
    else:
        await unregistered_user_start(update, context)
        return UNREGISTERED_USER


async def handle_random_message(update: Update, context: DEFAULT):
    await update.message.reply_text(
        text=f'I am not sure what "{update.message.text}" means 🤷🏻‍♀️\nPress /start to try again.')


main_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler(command='start', callback=start)],
    states={
        UNREGISTERED_USER: unregistered_user_handlers,
        REGISTERED_USER: registered_user_handlers,
        CONTENT_CREATOR: []
    },
    fallbacks=[
        CommandHandler(command='start', callback=start),
        MessageHandler(filters=filters.TEXT, callback=handle_random_message)
    ]
)

