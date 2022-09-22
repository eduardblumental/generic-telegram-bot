from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

from db.models import ContentCreators, Followings

from ..keyboards import registered_user_keyboard
from ..states import FIND_MODELS

from .states import FOLLOW, UNFOLLOW, NEXT, PREVIOUS, BACK_TO_MENU
from .utils import display_model

DEFAULT = ContextTypes.DEFAULT_TYPE
END = ConversationHandler.END


async def q_handle_find_models(update: Update, context: DEFAULT):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text('Have fun 🤓')

    context.user_data['user_id'] = update.effective_user.id
    context.user_data['cc_ids'] = [cc.content_creator_id for cc in ContentCreators.select()]
    context.user_data['current_cc_id'] = context.user_data.get('cc_ids')[0]
    context.user_data['start_query_id'] = query.message.id

    await display_model(update, context)

    return FIND_MODELS


async def q_handle_follow(update: Update, context: DEFAULT):
    query = update.callback_query
    await query.answer()

    Followings.create(
        user_id=context.user_data.get('user_id'),
        content_creator_id=context.user_data.get('cc_ids')[0]
    )

    await display_model(update, context)


async def q_handle_unfollow(update: Update, context: DEFAULT):
    query = update.callback_query
    await query.answer()

    Followings.delete().where(
        Followings.user_id == context.user_data.get('user_id'),
        Followings.content_creator_id == context.user_data.get('cc_ids')[0]
    ).execute()

    await display_model(update, context)


async def q_handle_next(update: Update, context: DEFAULT):
    query = update.callback_query
    await query.answer()

    context.user_data['cc_ids'] = context.user_data['cc_ids'][1:] + [context.user_data['cc_ids'][0]]
    await display_model(update, context)


async def q_handle_previous(update: Update, context: DEFAULT):
    query = update.callback_query
    await query.answer()

    context.user_data['cc_ids'] = [context.user_data['cc_ids'][-1]] + context.user_data['cc_ids'][:-1]
    await display_model(update, context)


async def q_handle_back_to_menu(update: Update, context: DEFAULT):
    query = update.callback_query
    await query.answer()

    await query.delete_message()
    await context.bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=context.user_data.get('start_query_id'),
        text="Hope you have found some good stuff. What's now? 😉",
        reply_markup=registered_user_keyboard
    )

    return END


async def handle_error(update: Update, context: DEFAULT):
    await update.message.reply_text(f'I am not sure what "{update.message.text}" means. Consider using the buttons 💩')


find_models_conversation = ConversationHandler(
    entry_points=[CallbackQueryHandler(callback=q_handle_find_models, pattern=f'^{FIND_MODELS}$')],
    states={
        FIND_MODELS: [
            CallbackQueryHandler(callback=q_handle_follow, pattern=f'^{FOLLOW}$'),
            CallbackQueryHandler(callback=q_handle_unfollow, pattern=f'^{UNFOLLOW}$'),
            CallbackQueryHandler(callback=q_handle_next, pattern=f'^{NEXT}$'),
            CallbackQueryHandler(callback=q_handle_previous, pattern=f'^{PREVIOUS}$'),
            CallbackQueryHandler(callback=q_handle_back_to_menu, pattern=f'^{BACK_TO_MENU}$')
        ]
    },
    fallbacks=[MessageHandler(filters=filters.ALL, callback=handle_error)]
)
