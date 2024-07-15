from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router

from fetch import supabase

from urllib.parse import urlencode

import os

server_url: str = os.getenv('SERVER_URL')

router = Router()

@router.message(Command('start'))
async def start_command(message: Message, state) -> None:
    if len(await supabase.get_by_id('players', message.from_user.id)) != 0:
        return

    steam_auth_params = {
        'openid.ns': 'http://specs.openid.net/auth/2.0',
        'openid.mode': 'checkid_setup',
        'openid.return_to': f'{server_url}/confirm_steam?tg_id={message.from_user.id}&username={message.from_user.username}',
        'openid.realm': server_url,
        'openid.identity': 'http://specs.openid.net/auth/2.0/identifier_select',
        'openid.claimed_id': 'http://specs.openid.net/auth/2.0/identifier_select'
    }

    auth_url = f'https://steamcommunity.com/openid/login?{urlencode(steam_auth_params)}'

    await message.answer(f'Добро пожаловать в <b>HotSpot</b>! \n\n<b>HotSpot</b> - сервис для проведения небольших турниров по игре Counter-Strike 2. \n\nДля регистрации <a href="{auth_url}">авторизуйтесь в Steam</a>', disable_web_page_preview = True)

@router.message(lambda message: 'event:registration_complete' in message.text)
async def handle_registration_event(message: Message):
    data = message.text.split(',')
    event_type = data[0].split(':')[1]
    playername = data[1].split(':')[1]

    if event_type == 'registration_complete':
        await message.answer(f'Регистрация завершена! \nПривет, <b>{playername}</b>')

    #fix