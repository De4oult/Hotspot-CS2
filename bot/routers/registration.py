from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup
from aiogram import Router, F

from fetch import supabase

from urllib.parse import urlencode

import os

server_url: str = os.getenv('SERVER_URL')

router = Router()

@router.message(Command('start'))
async def start_command(message: Message) -> None:
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

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text = 'Далее',
        callback_data = 'registred'
    ))

    await message.answer(
        f'Добро пожаловать в <b>HotSpot</b>! \n\n<b>HotSpot</b> - сервис для проведения небольших турниров по игре Counter-Strike 2. \n\nДля регистрации <a href="{auth_url}">авторизуйтесь в Steam</a>', 
        disable_web_page_preview = True,
        reply_markup = builder.as_markup()
    )

@router.callback_query(F.data == 'registred')
async def registred_callback(callback: CallbackQuery) -> None:
    users = await supabase.get_by_id('players', callback.from_user.id)

    if len(users) == 0:
        await callback.answer(
            'Пройдите авторизацию', 
            show_alert = True
        )
        
        return
    
    if not users[0].get('beta'):
        await callback.answer(
            'Сожалеем, но у Вас нет доступа к закрытому тестированию', 
            show_alert = True
        )
        
        return

    
    menu_keyboard = [
        [KeyboardButton(text = 'Турниры')],
        [KeyboardButton(text = 'Команда'), KeyboardButton(text = 'Профиль')]
    ]

    await callback.message.answer(
        'Регистрация в успешно завершена \n\nТеперь Вы можете создать команду и участвовать в матчах \n\nДобро пожаловать в <b>HotSpot</b>!', 
        show_alert = True,
        reply_markup = ReplyKeyboardMarkup(keyboard = menu_keyboard, resize_keyboard = True)
    )

    await callback.answer()
