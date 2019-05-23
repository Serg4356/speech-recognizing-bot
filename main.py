import telegram
import os
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import requests
import json
from pprint import pprint

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    '''Send a message when the command /start is issued.'''
    update.message.reply_text('Hi!')


def help(bot, update):
    '''Send a message when the command /help is issued.'''
    update.message.reply_text('Help!')


def speach(bot, update):
    '''Send a message as DialogFlow reply'''
    url = 'https://api.dialogflow.com/v1/query'
    token = os.getenv('dialog_flow_token')
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
    dialog_flow_response = response.json()
    update.message.reply_text(dialog_flow_response['result']['fulfillment']['speech'])


def deploy_intent(intent_name, intent):
    '''Deploy new intents for DialogFlow Agent'''
    url = 'https://api.dialogflow.com/v1/intents'
    token = os.getenv('dialog_flow_developer_token')
    headers = {
        'Authorization': f'Bearer {token}',
    }
    payload = {
        'v': 20150910,
        'auto': True,
        'contexts': [],
        'name': intent_name,
        'userSays':[],
        'responses':[
            {
                'messages':[
                    {
                        'speech': intent['answer'],
                    }
                ],
            },
        ],
    }
    for question in intent['questions']:
        user_say = {
            'data': [
                {
                    'text': question,
                }
            ]
        }
        payload['userSays'].append(user_say)
    response = requests.post(url, json=payload, headers=headers)
    pprint(response.json())


def deploy_intents_from_file(filename):
    with open(filename, 'r') as question_file:
        intents = json.load(question_file)
    for intent_name, intent in intents.items():
        deploy_intent(intent_name, intent)


def echo(bot, update):
    '''Echo the user message.'''
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    '''Log Errors caused by Updates.'''
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    '''Start the bot.'''
    # Create the EventHandler and pass it your bot's token.
    bot_token = os.getenv('bot_token')
    proxy = os.getenv('http_proxy')
    updater = Updater(bot_token, request_kwargs={'proxy_url': proxy})

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, speach))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    #main()
    load_dotenv()
    #deploy_intents_from_file('questions.json')

