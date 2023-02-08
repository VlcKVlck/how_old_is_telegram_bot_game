import logging

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, \
    Filters, Updater

import open_api_connect
from settings import bot_settings

logging.basicConfig(
    format='[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

updater = Updater(token=bot_settings.TOKEN, use_context=True)
dispatcher = updater.dispatcher


def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    logger.info(f"> Start chat #{chat_id}")
    context.bot.send_message(chat_id=chat_id, text="💣 Welcome! Let's play how old is! 💣")
    context.bot.send_message(chat_id=chat_id, text="Give me a name, and I'll tell you how old they are 💪")


def respond(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    text = update.message.text
    logger.info(f"= Got from user on chat #{chat_id}: {text!r}")
    response = open_api_connect.get_response(text)
    logger.info(f"= Got response on chat #{chat_id}: {response!r}")
    if response is None:
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="We don't know this person 🤨 Check your spelling or try another name")
    elif type(response) == list:
        buttons = [[KeyboardButton(name)] for name in response]
        intro_text = "We didnt find this name. Did you mean any of the following? You can type the name or select " \
                     "from the menu below."
        context.bot.send_message(chat_id=update.message.chat_id, text=intro_text)
        multi_text = "".join([f"{i+1}. {e}\n" for i, e in enumerate(response)])
        context.bot.send_message(chat_id=update.effective_chat.id, text=multi_text, reply_markup=ReplyKeyboardMarkup(buttons))
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text=response)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text, respond)
dispatcher.add_handler(echo_handler)

logger.info("* Start polling...")
updater.start_polling()  # Starts polling in a background thread.
updater.idle()  # Wait until Ctrl+C is pressed
logger.info("* Bye!")
