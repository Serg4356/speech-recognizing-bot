import os
from dotenv import load_dotenv
import logging
import vk_api
import random
import telegram
import requests
import argparse
from vk_api.longpoll import VkLongPoll, VkEventType
from logger_bot import MyLogsHandler, create_logger_bot, proxy_parser


def echo(event, vk_api):
    '''Send a message as DialogFlow reply'''
    url = 'https://api.dialogflow.com/v1/query'
    token = os.getenv('dialog_flow_client_token')
    headers = {
        'Authorization': f'Bearer {token}',
    }
    params = {
        'v': 20150910,
        'sessionId': event.user_id,
        'query': event.text,
        'lang': 'ru',
    }
    response = requests.get(url, headers=headers, params=params)
    dialog_flow_response = response.json()
    if not dialog_flow_response['result']['metadata']['intentName'] == 'Default Fallback Intent':
        vk_api.messages.send(
                    user_id=event.user_id,
                    message=dialog_flow_response['result']['fulfillment']['speech'],
                    random_id=random.randint(1,1000)
                )


def main():
    parser = proxy_parser()
    vk_group_token = os.getenv('vk_group_token')
    chat_id = os.getenv('chat_id')
    vk_session = vk_api.VkApi(token=vk_group_token)
    api_vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    logger = logging.getLogger()
    formatter = logging.Formatter('Speach vk bot %(asctime)s - %(levelname)s - %(message)s')
    logger.setLevel(logging.INFO)
    while True:
        try:
            bot_loger = create_logger_bot(parser.parse_args().proxy)
            handler = MyLogsHandler(bot_loger, chat_id)
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.info('Bot has been started')
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    echo(event, api_vk)
        except Exception as err:
            logger.error(err)


if __name__ == '__main__':
    load_dotenv()
    main()

