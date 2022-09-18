from telegram import Update
from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

from .keyboards import unregistered_start_menu_keyboard, registration_type_keyboard
from .states import REGISTER, LEARN_MORE
from .user_registration.handlers import register_user_conversation_handler

DEFAULT = ContextTypes.DEFAULT_TYPE


async def unregistered_user_start(update: Update, context: DEFAULT):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="So, what's the plan?",
        reply_markup=unregistered_start_menu_keyboard)


async def register(update: Update, context: DEFAULT):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text='So, tell us why are you here?',
        reply_markup=registration_type_keyboard
    )


async def learn_more(update: Update, context: DEFAULT):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text('More info...')
    await unregistered_user_start(update, context)


unregistered_user_handlers = [
    CallbackQueryHandler(callback=register, pattern=f'^{REGISTER}$'),
    CallbackQueryHandler(callback=learn_more, pattern=f'^{LEARN_MORE}$'),
    register_user_conversation_handler
]