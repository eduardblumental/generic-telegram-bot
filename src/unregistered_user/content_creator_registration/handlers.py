import os

from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

from db.models import ContentCreator
from .states import FIRST_NAME, LAST_NAME, EMAIL, BIRTH_DATE, COUNTRY
from ..states import REGISTER_CONTENT_CREATOR

DEFAULT = ContextTypes.DEFAULT_TYPE
END = ConversationHandler.END


async def q_handle_start_registration(update: Update, context: DEFAULT):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text='Please, type in your first name.')
    return FIRST_NAME


async def handle_first_name_error(update: Update, context: DEFAULT):
    pass


async def handle_first_name(update: Update, context: DEFAULT):
    context.user_data['content_creator_id'] = update.effective_user.id
    context.user_data['first_name'] = update.message.text

    await update.message.reply_text(
        text='Please, type in your last name.')
    return LAST_NAME


async def handle_last_name_error(update: Update, context: DEFAULT):
    pass


async def handle_last_name(update: Update, context: DEFAULT):
    context.user_data['last_name'] = update.message.text

    await update.message.reply_text(
        text='Where country are you from?')
    return EMAIL


async def handle_email_error(update: Update, context: DEFAULT):
    pass


async def handle_email(update: Update, context: DEFAULT):
    context.user_data['email'] = update.message.text

    await update.message.reply_text(
        text='Please, type in your birthday in a **dd/mm/yyyy** format.')
    return BIRTH_DATE


async def handle_birth_date_error(update: Update, context: DEFAULT):
    pass


async def handle_birth_date(update: Update, context: DEFAULT):
    context.user_data['birth_date'] = int(update.message.text)

    await update.message.reply_text(
        text='Tell us more about yourself.')
    return COUNTRY


async def handle_country_error(update: Update, context: DEFAULT):
    pass


async def handle_country(update: Update, context: DEFAULT):
    context.user_data['country'] = update.message.text

    content_creator_id = context.user_data.get('content_creator_id')
    first_name = context.user_data.get('first_name')
    last_name = context.user_data.get('last_name')
    email = context.user_data.get('email')
    birth_date = context.user_data.get('birth_date')
    country = context.user_data.get('country')

    ContentCreator.create(
        content_creator_id=content_creator_id, first_name=first_name, last_name=last_name,
        email=email, birth_date=birth_date, country=country).save()

    await update.message.reply_text(
        text=f'Welcome to the club {first_name}! Use /start command to continue.')
    return END


async def handle_error(update: Update, context: DEFAULT):
    await update.message.reply_text(
        text=f'I am not sure what "{update.message.text}" means. Please, use /start command to try again.')

    return END


register_content_creator_conversation = ConversationHandler(
    entry_points=[CallbackQueryHandler(callback=q_handle_start_registration, pattern=f'^{REGISTER_CONTENT_CREATOR}$')],
    states={
        FIRST_NAME: [
            MessageHandler(filters=(filters.TEXT and ~filters.COMMAND), callback=handle_first_name)
        ],
        LAST_NAME: [
            MessageHandler(filters=(filters.TEXT and ~filters.COMMAND), callback=handle_last_name)
        ],
        EMAIL: [
            MessageHandler(filters=(filters.TEXT and ~filters.COMMAND), callback=handle_email)
        ],
        BIRTH_DATE: [
            MessageHandler(filters=(filters.TEXT and ~filters.COMMAND), callback=handle_birth_date)
        ],
        COUNTRY: [
            MessageHandler(filters=filters.TEXT, callback=handle_country)
        ]
    },
    fallbacks=[MessageHandler(filters=filters.ALL, callback=handle_error)]
)
