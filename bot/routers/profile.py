from aiogram.types import Message
from aiogram import Router, F

from fetch import supabase

router = Router()

@router.message(F.text.lower() == 'профиль')
async def start_command(message: Message) -> None:
    user: dict = (await supabase.get_by_id('players', message.from_user.id))[0]

    team_name = supabase.get_by_id('teams', user.get('team')) if user.get('team') else 'нет'

    await message.answer(
        '<b>%s</b> \n\nМатчей сыграно: <b>%s</b> \nМатчей выиграно: <b>%s</b> \nКоличество MVP: <b>%s</b> \nКоманда: <b>%s</b>' % (
            user.get('playername'),
            user.get('matches_count'),
            user.get('wins_count'),
            user.get('mvp_count'),
            team_name
        )
    )