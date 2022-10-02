from telegram import Update
from telegram.ext import (
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

from db.models import ContentCreator, Following

from ..keyboards import registered_user_keyboard
from ..states import FIND_MODELS, MY_MODELS

from .states import FOLLOW, UNFOLLOW, NEXT, PREVIOUS, BACK_TO_MENU
from .utils import display_model, load_models

DEFAULT = ContextTypes.DEFAULT_TYPE
END = ConversationHandler.END


async def q_handle_find_models(update: Update, context: DEFAULT):
    await load_models(update, context)
    await display_model(update, context)

    return FIND_MODELS


async def q_handle_my_models(update: Update, context: DEFAULT):
    await load_models(update, context)
    if context.user_data.get('cc_ids'):
        context.user_data['current_cc_id'] = context.user_data.get('cc_ids')[0]
        await display_model(update, context)
        return MY_MODELS
    else:
        await update.callback_query.edit_message_text(
            text="It seems like you haven't followed anyone yet 💁🏻‍♀️ Use /start command to continue."
        )


async def q_handle_follow(update: Update, context: DEFAULT):
    query = update.callback_query
    await query.answer()

    Following.create(
        user_id=context.user_data.get('user_id'),
        content_creator_id=context.user_data.get('cc_ids')[0]
    )

    await display_model(update, context)


async def q_handle_unfollow(update: Update, context: DEFAULT):
    query = update.callback_query
    await query.answer()

    Following.delete().where(
        Following.user_id == context.user_data.get('user_id'),
        Following.content_creator_id == context.user_data.get('cc_ids')[0]
    ).execute()

    await display_model(update, context)


async def q_handle_next(update: Update, context: DEFAULT):
    query = update.callback_query
    await query.answer()

    if len(context.user_data.get('cc_ids')) > 1:
        context.user_data['cc_ids'] = context.user_data['cc_ids'][1:] + [context.user_data['cc_ids'][0]]

    await display_model(update, context)


async def q_handle_previous(update: Update, context: DEFAULT):
    query = update.callback_query
    await query.answer()

    if len(context.user_data.get('cc_ids')) > 1:
        context.user_data['cc_ids'] = [context.user_data['cc_ids'][-1]] + context.user_data['cc_ids'][:-1]

    await display_model(update, context)


async def q_handle_back_to_menu(update: Update, context: DEFAULT):
    query = update.callback_query
    await query.answer()

    await query.delete_message()
    await context.bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=context.user_data.get('start_query_id'),
        text="I hope you were nice to the girls. Let me know what's on your mind 🧞‍♀️",
        reply_markup=registered_user_keyboard
    )

    return END


async def handle_error(update: Update, context: DEFAULT):
    await update.message.reply_text(f'I am not sure what "{update.message.text}" means. Consider using the buttons 💩')


scrolling_models_handlers = [
    CallbackQueryHandler(callback=q_handle_follow, pattern=f'^{FOLLOW}$'),
    CallbackQueryHandler(callback=q_handle_unfollow, pattern=f'^{UNFOLLOW}$'),
    CallbackQueryHandler(callback=q_handle_next, pattern=f'^{NEXT}$'),
    CallbackQueryHandler(callback=q_handle_previous, pattern=f'^{PREVIOUS}$'),
    CallbackQueryHandler(callback=q_handle_back_to_menu, pattern=f'^{BACK_TO_MENU}$')
]

scrolling_models_conversation = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(callback=q_handle_find_models, pattern=f'^{FIND_MODELS}$'),
        CallbackQueryHandler(callback=q_handle_my_models, pattern=f'^{MY_MODELS}$')
    ],
    states={
        FIND_MODELS: scrolling_models_handlers,
        MY_MODELS: scrolling_models_handlers
    },
    fallbacks=[MessageHandler(filters=filters.ALL, callback=handle_error)]
)
