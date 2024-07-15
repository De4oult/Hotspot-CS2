from aiogram.client.bot import DefaultBotProperties
from aiogram import Bot, Dispatcher

import os

bot: Bot = Bot(token = os.getenv('BOT_TOKEN'), default = DefaultBotProperties(parse_mode = 'HTML'))

dispatcher: Dispatcher = Dispatcher()