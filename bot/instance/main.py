from aiogram import Bot, Dispatcher, types
from bot.instance.handlers import user_router

webhook_dp = Dispatcher()
webhook_dp.include_router(user_router)

async def feed_update(token: str, update: dict):
    bot = Bot(token=token)
    try:
        aiogram_update = types.Update(**update)
        await webhook_dp.feed_update(
            bot=bot,
            update=aiogram_update
        )
    finally:
        await bot.session.close()
