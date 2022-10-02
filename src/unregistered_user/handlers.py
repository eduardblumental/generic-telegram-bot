from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes

from .keyboards import unregistered_user_keyboard, registration_type_keyboard
from .states import REGISTER, LEARN_MORE

from .user_registration.handlers import register_user_conversation
from .content_creator_registration.handlers import register_content_creator_conversation

DEFAULT = ContextTypes.DEFAULT_TYPE


async def unregistered_user_start(update: Update, context: DEFAULT):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Welcome to Secret Exchange 🧞‍♀️ "
             "We are a growing community of explorers and content creators from all over the world 🌍 "
             "We hope you will enjoy your time being with us. "
             "Ready to join?",
        reply_markup=unregistered_user_keyboard)


async def q_handle_register(update: Update, context: DEFAULT):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text='Why are you here?',
        reply_markup=registration_type_keyboard
    )


async def q_handle_learn_more(update: Update, context: DEFAULT):
    query = update.callback_query
    await query.answer()

    await unregistered_user_start(update, context)


unregistered_user_handlers = [
    CallbackQueryHandler(callback=q_handle_register, pattern=f'^{REGISTER}$'),
    CallbackQueryHandler(callback=q_handle_learn_more, pattern=f'^{LEARN_MORE}$'),
    register_user_conversation,
    register_content_creator_conversation
]
