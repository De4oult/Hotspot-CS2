from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram import Router, F

from fetch import supabase


router = Router()

@router.message(F.text.lower() == 'команда')
async def start_command(message: Message) -> None:
    user: dict = (await supabase.get_by_id('players', message.from_user.id))[0]

    if not user.get('team_id'):
        builder = InlineKeyboardBuilder()
    
        builder.row(
            InlineKeyboardButton(
                text = 'Создать',
                callback_data = 'create_team'
            ),
            InlineKeyboardButton(
                text = 'Присоединиться',
                callback_data = 'join_team'
            )
        )

        await message.answer(
            '<b>У Вас нет команды</b> \n\nВы можете создать ее сами или присоединиться к существующей. \n\nP.S. Человек, создавший команду, по умолчанию становится ее капитаном',
            reply_markup = builder.as_markup()
        )

    team: dict = (await supabase.get_by_id('teams', user.get('team_id')))[0]

    team_players: dict = await supabase.get_by_key('players', 'team_id', team.get('id'))

    await message.answer(
        '<b>%s</b> \n\nУчастники:\n%s' % (
            team.get('name'), 
            '\n'.join(['- <b>%s</b>' % player.get('playername') for player in team_players])
        )
    )

@router.callback_query(F.data == 'create_team')
async def create_team(callback: CallbackQuery) -> None:
    users = await supabase.get_by_id('players', callback.from_user.id)

    
@router.callback_query(F.data == 'join_team')
async def join_team(callback: CallbackQuery) -> None:
    users = await supabase.get_by_id('players', callback.from_user.id)