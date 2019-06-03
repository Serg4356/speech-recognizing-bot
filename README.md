# Speach recognizing bot

### Description

There are two bots(telegram, and vk group) with auto text recognizing in this repo. Text recognizing is provided by Google's [DialogFlow](https://dialogflow.com/). Bots automatically recognize user's intent and response with one(or more) prepared answer. You can use it for make your personal auto helper or modify it to make more complex automatic response system for your company, blog, store etc.

You can easily make modifications and deploy it on your personal or open server platforms (like [Heroku](https://heroku.com/). Current version of bot doesn't support long conversations (one question - one answer), but it can be easily fixed too.

You can get chatting expirience by messaging my telegram bot - @serg4356_speach_recognizing_bot, or [here](https://vk.com/club182829172). Or simply look at gif below:  

![chatting-gif](https://media.giphy.com/media/YOTFIF9MhyGt01PoCx/giphy.gif)

Also you can expand your bot lexicon automatically through make_intents module.

### How to install

python has to be installed on your system. Use pip (or pip3 if there is conflict with Python 2) to install dependences.
```
pip install -r requirements.txt
```
It is recommended to use virtual environment [virtualenv/venv](https://docs.python.org/3/library/venv.html) to isolate your project.  

Besides that you must create `.env` file in your project's folder, containing environment variables. It should look like this(all data except environment variable's names are fake):  
```
bot_token=856723764:AAE_KBfkjsfesHJHKGHuiynd5Q0zEWg
logger_bot_token=8223467826:AAGvWCGPoWk5WGJgjgjhGGJYgJtdXMMMGc
chat_id=390153672
https_proxy=https://xxx.xxx.xxx.xxx:xxxx/
dialog_flow_client_token=d28a7f1f26sefse645461491sefs2fe8320aee217d46
dialog_flow_developer_token=0424fe1c82fessea234d4d82e95sefsefa0e9e03610e3
vk_group_token=8027e72504de2a1552e16b1fewfsvee67sefesf38902118df940343e97559fb7e75e5d20b030664a2
```
Variables description:  
`bot_token`, `logger_bot_token` - your telegram bot tokens, you would get it from [BotFather](https://telegram.me/BotFather) after you bot's been registered, first is the token of main bot for your users to chat with, second - is token of your personal support bot (which sends program execution logs to your telegram).   
`chat_id` - Your chat id. You can find out it from @userinfobot in Telegram.    
`dialog_flow_client_token`, `dialog_flow_developer_token` - tokens for interaction with your DialogFlow Project's API. More detailed description you can find [here](https://dialogflow.com/docs/reference/agent)
`vk_group_token` - your vk group token. Could be found in group [options](https://dvmn.org/media/filer_public/2f/11/2f11a34a-1de3-4acc-838d-d1be37bd6828/screenshot_from_2019-04-29_20-10-16.png)

Warnings! 
All of environment variables are required, except http_proxy. 
Version of DialogFlow API used in this project considered to be deprecated and would be unsupported after october'19. Prepare to migrate on v2 API.


### Quickstart

After installation and creating `.env` file - type into console:
```
$python speach_vk_bot.py
```
or:
```
$python speach_telegram_bot.py
```

If Telegram is blocked in your country - you can simply type `-p` after module name for proxy connection. (Note, in this case `https_proxy` variable in `.env` file required).

You can also push new intents into your DialogFlow Project. Just create `.json` file with following structure:
```
{
    "Устройство на работу": {
        "questions": [
            "Как устроиться к вам на работу?",
            "Как устроиться к вам?",
            "Как работать у вас?",
            "Хочу работать у вас",
            "Возможно-ли устроиться к вам?",
            "Можно-ли мне поработать у вас?",
            "Хочу работать редактором у вас"
        ],
        "answer": "Если вы хотите устроиться к нам, напишите на почту game-of-verbs@gmail.com мини-эссе о себе и прикрепите ваше портфолио."
    },
    ...
}
 
```
and type into console:
```
$python make_intents.py path/to/your/intents_file.json
```


### Deploing on Heroku

This bot can be deployed on Heroku platform. There is a Procfile in project's repository with all required instructions in it.   
   
Just do the following to make successfull deploy:  
   
1. Register on [Heroku](https://heroku.com)  
2. Add new app and name it.  
3. Fork this repository to your github account, and deploy it on Heroku. (You can also choose automatic github deploy, to refresh your project from latests commits).  
4. Turn on new proccess on your heroku account resourses page.   
5. Have fun)  


### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
