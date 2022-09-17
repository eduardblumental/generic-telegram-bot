import os

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

    register_user_conversation = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_registration, pattern=f'^{REGISTER_USER}$')],
        states={
            FIRST_NAME: [MessageHandler(filters=filters.TEXT, callback=name)]
        },
        fallbacks=[CallbackQueryHandler(start_registration, pattern=f'^{REGISTER_USER}$')]
    )


    registration_handlers = [
        CallbackQueryHandler(register, pattern=f'^{REGISTER}$'),
        register_user_conversation,
        #register_content_creator_conversation
    ]

    main_conversation = ConversationHandler(
        entry_points=[CommandHandler(command='start', callback=start)],
        states={
            UNREGISTERED_USER: registration_handlers,
            REGISTER_USER: []
        },
        fallbacks=[CommandHandler(command='start', callback=start)]
    )

    app.add_handler(main_conversation)
    app.add_handler(MessageHandler(filters=filters.TEXT, callback=random_message))
    app.run_polling()
