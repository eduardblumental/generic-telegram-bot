import os
import logging as log

from telegram.ext import ApplicationBuilder

from handlers import main_conversation_handlers

log.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=log.INFO)


if __name__ == '__main__':
    app = ApplicationBuilder().token(os.environ.get('TELEGRAM_BOT_TOKEN')).build()

    app.add_handlers(main_conversation_handlers)
    app.run_polling()
