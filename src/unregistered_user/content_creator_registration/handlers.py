from datetime import datetime

from telegram import Update
from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

from db.models import ContentCreators
from .states import FIRST_NAME, COUNTRY, BIRTH_DATE, BIO, PROFILE_PIC
from ..states import REGISTER_CONTENT_CREATOR

DEFAULT = ContextTypes.DEFAULT_TYPE
END = ConversationHandler.END


async def start_registration(update: Update, context: DEFAULT):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text='Please, type in your first name.')
    return FIRST_NAME


async def name(update: Update, context: DEFAULT):
    context.user_data['user_id'] = update.effective_user.id
    context.user_data['first_name'] = update.message.text

    await update.message.reply_text(
        text='Where are you from?')
    return COUNTRY


async def country(update: Update, context: DEFAULT):
    context.user_data['country'] = update.message.text

    await update.message.reply_text(
        text='Select your birth date.')
    return BIRTH_DATE


async def birth_date(update: Update, context: DEFAULT):
    context.user_data['birth_date'] = datetime.strptime(update.message.text, '%d/%m/%Y')

    await update.message.reply_text(
        text='Tell us more about yourself.')
    return BIO


async def bio(update: Update, context: DEFAULT):
    context.user_data['bio'] = update.message.text

    await update.message.reply_text(
        text='Last, upload your profile pic.')
    return PROFILE_PIC


async def profile_pic(update: Update, context: DEFAULT):
    context.user_data['profile_pic'] = update.message.photo[-1].file_id

    ContentCreators.create(
        user_id=context.user_data.get('user_id'),
        first_name=context.user_data.get('first_name'),
        country=context.user_data.get('country'),
        birth_date=context.user_data.get('birth_date'),
        bio=context.user_data.get('bio'),
        profile_pic=context.user_data.get('profile_pic')
    ).save()

    await update.message.reply_text(
        text='Thank you for the registration! Use /start command to continue.')
    return END


async def error(update: Update, context: DEFAULT):
    await update.message.reply_text(f'I am not sure what "{update.message.text}" means. Please, try again.')


register_content_creator_conversation = ConversationHandler(
    entry_points=[CallbackQueryHandler(callback=start_registration, pattern=f'^{REGISTER_CONTENT_CREATOR}$')],
    states={
        FIRST_NAME: [MessageHandler(filters=(filters.TEXT & ~filters.COMMAND), callback=name)],
        COUNTRY: [MessageHandler(filters=(filters.TEXT & ~filters.COMMAND), callback=country)],
        BIRTH_DATE: [MessageHandler(filters=(filters.TEXT & ~filters.COMMAND), callback=birth_date)],
        BIO: [MessageHandler(filters=(filters.TEXT & ~filters.COMMAND), callback=bio)],
        PROFILE_PIC: [MessageHandler(filters=filters.PHOTO, callback=profile_pic)]
    },
    fallbacks=[MessageHandler(filters=filters.ALL, callback=error)]
)