from telegram import Update
from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

from db.models import Users, ContentCreators
from .states import FIRST_NAME
from ..states import REGISTER_USER

DEFAULT = ContextTypes.DEFAULT_TYPE
END = ConversationHandler.END


async def start_registration(update: Update, context: DEFAULT):
    query = update.callback_query
    await query.answer()
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Please, type in your first name.')
    return FIRST_NAME


async def name(update: Update, context: DEFAULT):
    user_id = update.effective_user.id
    first_name = update.message.text

    user = Users.create(user_id=user_id, first_name=first_name)
    user.save()

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Thank you for the registration! Use /start command to continue.')
    return END


async def error(update: Update, context: DEFAULT):
    await update.message.reply_text(f'I am not sure what "{update.message.text}" means. Please, try again.')


register_user_conversation_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(callback=start_registration, pattern=f'^{REGISTER_USER}$')],
    states={
        FIRST_NAME: [
            MessageHandler(filters=(filters.TEXT & ~filters.COMMAND), callback=name)
        ]
    },
    fallbacks=[MessageHandler(filters=filters.ALL, callback=error)]
)