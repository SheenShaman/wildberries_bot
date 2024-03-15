import asyncio
import aioschedule

from app import handlers


async def scheduler_notification():
    aioschedule.every(5).seconds.do(handlers.send_notification)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
