import json
import requests
import argparse
import os
import logging
from pprint import pprint
from dotenv import load_dotenv


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p',
                        '--path',
                        help='Input path to json file with intents',
                        required=True)
    return parser


def deploy_intent(intent_name, intent):
    '''Deploy new intents for DialogFlow Agent'''
    url = 'https://api.dialogflow.com/v1/intents'
    token = os.getenv('dialog_flow_developer_token')
    headers = {
        'Authorization': f'Bearer {token}',
    }
    payload = {
        'v': 20150910,
        'lang': 'ru',
        'auto': True,
        'contexts': [],
        'name': intent_name,
        'userSays':[],
        'responses':[
            {
                'messages':[
                    {
                        'speech': intent['answer'],
                        'type': 0,
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
    response.raise_for_status()
    if not response.json()['status']['errorType'] == 'success':
        raise requests.exceptions.HTTPError(response.json()['status']['errorDetails'])


def deploy_intents_from_json_file(filename):
    with open(filename, 'r') as question_file:
        intents = json.load(question_file)
    for intent_name, intent in intents.items():
        try:
            deploy_intent(intent_name, intent)
        except requests.exceptions.HTTPError as http_err:
            logging.error(http_err, exc_info=True)


if __name__ == '__main__':
    load_dotenv()
    parser = create_parser()
    arguments = parser.parse_args()
    logging.basicConfig(format='Make intents: %(asctime)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    deploy_intents_from_json_file(arguments.path)
