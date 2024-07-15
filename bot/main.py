from bot import bot, dispatcher
from routers import registration

import asyncio

async def main() -> None:
    dispatcher.include_routers(registration.router)
    
    await bot.delete_webhook(drop_pending_updates = True)
    await dispatcher.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())