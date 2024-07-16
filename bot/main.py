from bot import bot, dispatcher
from routers import registration, profile, team

import asyncio

async def main() -> None:
    dispatcher.include_routers(
        registration.router, 
        profile.router,
        team.router
    )
    
    await bot.delete_webhook(drop_pending_updates = True)
    await dispatcher.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())