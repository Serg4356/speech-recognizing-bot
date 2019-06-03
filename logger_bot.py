import telegram
import logging
import argparse
import os


def proxy_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--proxy', action='store_true')
    return parser


def create_logger_bot(has_proxy):
    bot_token = os.getenv('logger_bot_token')
    if has_proxy:
        proxy_url = os.getenv('https_proxy')
        proxy = telegram.utils.request.Request(proxy_url=proxy_url)
        return telegram.Bot(token=bot_token, request=proxy)
    else:
        return telegram.Bot(token=bot_token)


class MyLogsHandler(logging.Handler):

    def __init__(self, telegram_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.telegram_bot = telegram_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.telegram_bot.send_message(chat_id=self.chat_id, text=log_entry)
