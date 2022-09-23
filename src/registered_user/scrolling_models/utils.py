from telegram import Update, InputMediaPhoto
from telegram.ext import ContextTypes

from db.models import ContentCreators, Followings

from ..states import FIND_MODELS, MY_MODELS

from .keyboards import get_find_model_keyboard
from .states import FOLLOW, UNFOLLOW, NEXT, PREVIOUS

DEFAULT = ContextTypes.DEFAULT_TYPE


def is_following(user_id, cc_id):
    return Followings.select().where(Followings.user_id == user_id, Followings.content_creator_id == cc_id).exists()


async def display_model(update: Update, context: DEFAULT):
    user_id = context.user_data.get('user_id')
    cc_id = context.user_data.get('cc_ids')[0]

    cc: ContentCreators = ContentCreators.select().where(ContentCreators.content_creator_id == cc_id).get()
    caption = f"{cc.first_name}, {cc.age}, {cc.country}\n\n{cc.bio}"

    query = update.callback_query
    if query.data in [FIND_MODELS, MY_MODELS]:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=open(cc.profile_pic, 'rb'),
            caption=caption,
            reply_markup=get_find_model_keyboard(is_following(user_id, cc_id))
        )
    else:
        if query.data in [FOLLOW, UNFOLLOW]:
            await query.edit_message_reply_markup(
                reply_markup=get_find_model_keyboard(is_following(user_id, cc_id))
            )
        elif query.data in [NEXT, PREVIOUS]:
            await query.edit_message_media(
                media=InputMediaPhoto(open(cc.profile_pic, 'rb')),
                reply_markup=get_find_model_keyboard(is_following(user_id, cc_id))
            )
            await query.edit_message_caption(
                caption=caption,
                reply_markup=get_find_model_keyboard(is_following(user_id, cc_id))
            )


async def load_models(update: Update, context: DEFAULT):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text('Hello ladies 👯‍♀️')

    context.user_data['user_id'] = update.effective_user.id
    context.user_data['start_query_id'] = query.message.id

    if query.data == FIND_MODELS:
        context.user_data['cc_ids'] = [cc.content_creator_id for cc in ContentCreators.select()]
    elif query.data == MY_MODELS:
        context.user_data['cc_ids'] = [cc.content_creator_id
                                       for cc in ContentCreators.select()
                                       if is_following(context.user_data['user_id'], cc.content_creator_id)
                                       ]
