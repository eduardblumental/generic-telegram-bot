import os
import logging as log

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    filters
)

from handlers import *

log.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=log.INFO)


if __name__ == '__main__':
    app = ApplicationBuilder().token(os.environ.get('TELEGRAM_BOT_TOKEN')).build()

    unregistered_user_conversation = ConversationHandler(
        entry_points=[CommandHandler(command='start', callback=start)],
        states={
            CHOOSING_MODE: [
                CallbackQueryHandler(callback=register_user, pattern=f'^{REGISTER_USER}$'),
                CallbackQueryHandler(callback=register_content_creator, pattern=f'^{REGISTER_CONTENT_CREATOR}$')
            ],
            REGISTRATION: [

            ]
        },
        fallbacks=[CommandHandler(command='start', callback=start)]
    )
    app.add_handler(CommandHandler(command='start', callback=start))
    app.add_handler(CallbackQueryHandler(callback=register_user, pattern=f'^{REGISTER_USER}$'))
    app.add_handler(CallbackQueryHandler(callback=register_content_creator, pattern=f'^{REGISTER_CONTENT_CREATOR}$'))
    app.add_handler(MessageHandler(filters=filters.TEXT, callback=random_message))
    app.run_polling()
