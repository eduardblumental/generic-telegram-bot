import logging as log

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from keyboards import *
from models import Users, ContentCreators
from states import *


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    existing_user_ids = list(user.user_id for user in Users.select())
    if update.effective_user.id in existing_user_ids:
        await update.message.reply_text(
            text="So, what's the plan?",
            reply_markup=registered_user_keyboard)
        return REGISTERED_USER
    else:
        await update.message.reply_text(
            text="Welcome to Secret Exchange! Please, register.",
            reply_markup=start_menu_keyboard)
        return UNREGISTERED_USER


async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await update.effective_message.reply_text(text=f"Okay, let's register you now.", reply_markup=user_type_keyboard)


async def start_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer('👍🏻')
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Please, type in your first name.')
    return FIRST_NAME


async def name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    first_name = update.message.text

    user = Users.create(user_id=user_id, first_name=first_name)
    user.save()

    await context.bot.send_message(chat_id=update.effective_chat.id, text='Thank you for the registration!')
    return ConversationHandler.END


async def random_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text=f'I am not sure what "{update.message.text}" means 🤷🏻‍♀️\nPress /start to try again.')
