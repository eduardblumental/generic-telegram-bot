from telegram import Update
from telegram.ext import ContextTypes

from keyboards import *
from models import Users, ContentCreators
from states import *


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in Users.select(Users.user_id):
        await update.message.reply_text(
            text="So, what's the plan?",
            reply_markup=registered_user_keyboard)
        return REGISTERED_USER
    else:
        await update.message.reply_text(
            text="Welcome to Secret Exchange!",
            reply_markup=unregistered_user_keyboard)
        return UNREGISTERED_USER


async def register_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(f"Okay, let's register you now.")
    await update.effective_message.reply_text(f'Your user id is: {query.from_user.id}')


async def register_content_creator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(f'Your option is: {query.data}. Registering content creator.')
    await update.effective_message.reply_text(f'Your user id is: {query.from_user.id}')


async def random_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text=f'I am not sure what "{update.message.text}" means 🤷🏻‍♀️\nPress /start to try again.')
