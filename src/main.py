import os
import logging as log

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters

from models import Users, ContentCreators
from keyboards import *

log.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=log.INFO)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in Users.select(Users.user_id):
        await update.message.reply_text(
            text="So, what's the plan?",
            reply_markup=registered_user_start_keyboard)
    else:
        await update.message.reply_text(
            text="Welcome to Secret Exchange!",
            reply_markup=unregistered_user_start_keyboard)


async def register_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(f'Your option is: {query.data}. Registering user.')
    await update.effective_message.reply_text(f'Your user id is: {query.from_user.id}')


async def register_content_creator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(f'Your option is: {query.data}. Registering content creator.')
    await update.effective_message.reply_text(f'Your user id is: {query.from_user.id}')


async def random_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text=f'I am not sure what "{update.message.text}" means 🤷🏻‍♀️\nPress /start to try again.')


if __name__ == '__main__':
    app = ApplicationBuilder().token(os.environ.get('TELEGRAM_BOT_TOKEN')).build()

    app.add_handler(CommandHandler(command='start', callback=start))
    app.add_handler(CallbackQueryHandler(callback=register_user, pattern=f'^{REGISTER_USER}$'))
    app.add_handler(CallbackQueryHandler(callback=register_content_creator, pattern=f'^{REGISTER_CONTENT_CREATOR}$'))
    app.add_handler(MessageHandler(filters=filters.TEXT, callback=random_message))
    app.run_polling()
