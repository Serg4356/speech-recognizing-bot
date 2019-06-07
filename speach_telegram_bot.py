import telegram
import os
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import requests
from logger_bot import MyLogsHandler, create_logger_bot, proxy_parser


def speach(bot, update):
    '''Send a message as DialogFlow reply'''
    url = 'https://api.dialogflow.com/v1/query'
    token = os.getenv('dialog_flow_client_token')
    headers = {
        'Authorization': f'Bearer {token}',
    }
    params = {
        'v': 20150910,
        'sessionId': update.message.chat_id,
        'query': update.message.text,
        'lang': 'ru',
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    dialog_flow_response = response.json()
    if not dialog_flow_response['status']['errorType'] == 'success':
        raise requests.exceptions.HTTPError(dialog_flow_response['status']['errorType'])
    update.message.reply_text(dialog_flow_response['result']['fulfillment']['speech'])


def error(bot, update, error):
    '''Log Errors caused by Updates.'''
    logger.error(error, exc_info=True)


def main():
    '''Start the bot.'''
    # Enable logging
    logging.basicConfig(format='Speach telegram bot %(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    logger = logging.getLogger(__name__)

    logger_bot_chat_id = os.getenv('logger_bot_chat_id')
    logger.setLevel(logging.INFO)

    parser = proxy_parser()
    has_proxy = parser.parse_args().proxy
    logger_bot_chat_id = os.getenv('chat_id')
    logger_bot = create_logger_bot(has_proxy)
    handler = MyLogsHandler(logger_bot, logger_bot_chat_id)

    # Create the EventHandler and pass it your bot's token.
    bot_token = os.getenv('bot_token')
    if has_proxy:
        proxy = os.getenv('https_proxy')
        updater = Updater(bot_token, request_kwargs={'proxy_url': proxy})
    else:
        updater = Updater(bot_token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, speach))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    load_dotenv()
    main()

