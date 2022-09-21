import os
import logging

from telegram.ext import ApplicationBuilder

from handlers import main_conversation_handler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('main_logger')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)


if __name__ == '__main__':
    app = ApplicationBuilder().token(os.environ.get('TELEGRAM_BOT_TOKEN')).build()
    app.add_handler(main_conversation_handler)
    app.run_polling()
