import os
import sys
import asyncio
import logging

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher

from app import handlers
from app.notification import scheduler_notification

load_dotenv()

bot = Bot(token=os.getenv('BOT_TOKEN'))


async def main():
    # bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher(bot=bot)
    dp.include_router(handlers.router)
    await dp.start_polling(bot)
    asyncio.create_task(scheduler_notification())


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
