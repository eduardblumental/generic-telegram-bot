from datetime import datetime
import os

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
from .states import FIRST_NAME, COUNTRY, AGE, BIO, PROFILE_PIC
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
    context.user_data['content_creator_id'] = update.effective_user.id
    context.user_data['first_name'] = update.message.text

    await update.message.reply_text(
        text='Where are you from?')
    return COUNTRY


async def country(update: Update, context: DEFAULT):
    context.user_data['country'] = update.message.text

    await update.message.reply_text(
        text='How old are you?')
    return AGE


async def age(update: Update, context: DEFAULT):
    context.user_data['age'] = int(update.message.text)

    await update.message.reply_text(
        text='Tell us more about yourself.')
    return BIO


async def bio(update: Update, context: DEFAULT):
    context.user_data['bio'] = update.message.text

    await update.message.reply_text(
        text='Last, upload your profile pic.')
    return PROFILE_PIC


async def profile_pic(update: Update, context: DEFAULT):
    content_creator_id = context.user_data.get('content_creator_id')
    first_name = context.user_data.get('first_name')
    country = context.user_data.get('country')
    age = context.user_data.get('age')
    bio = context.user_data.get('bio')

    file = await update.message.photo[-1].get_file()
    profile_pic_path = os.path.join('..', 'static', f"{first_name}_{content_creator_id}.jpg")
    await file.download(profile_pic_path)

    ContentCreators.create(
        content_creator_id=content_creator_id, first_name=first_name,
        country=country, age=age, bio=bio, profile_pic=profile_pic_path).save()

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
        AGE: [MessageHandler(filters=(filters.TEXT & ~filters.COMMAND), callback=age)],
        BIO: [MessageHandler(filters=(filters.TEXT & ~filters.COMMAND), callback=bio)],
        PROFILE_PIC: [MessageHandler(filters=filters.PHOTO, callback=profile_pic)]
    },
    fallbacks=[MessageHandler(filters=filters.ALL, callback=error)]
)