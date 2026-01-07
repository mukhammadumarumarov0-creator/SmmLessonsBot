import asyncio
from django.core.management.base import BaseCommand
from aiogram import Bot
from config import settings


class Command(BaseCommand):
    help = "Delete webhook and clear pending updates"

    def handle(self, *args, **kwargs):
        asyncio.run(self.delete_webhook())

    async def delete_webhook(self):
        bot = Bot(token=settings.BOT_TOKEN)

        try:
            await bot.delete_webhook(drop_pending_updates=True)
            print("🧹 Webhook DELETED and cache cleared")
        finally:
            await bot.session.close()
