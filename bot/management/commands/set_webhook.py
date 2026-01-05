import asyncio
import aiogram

from django.core.management.base import BaseCommand
from config import settings

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        """
        Set webhook for the bot.
        """
        print(settings.BOT_WEBHOOK_URL)
        asyncio.run(self.manage_webhook())

    async def manage_webhook(self):
        """
        Manage webhook for the bot.
        """
        bot = aiogram.Bot(token=settings.BOT_TOKEN)

        try:
            # Get current webhook info
            webhook_info = await bot.get_webhook_info()
            print("Current Webhook Info:", webhook_info)

            # Check if the current webhook URL is different from the desired one
            if webhook_info.url != settings.BOT_WEBHOOK_URL:
                await bot.set_webhook(settings.BOT_WEBHOOK_URL)
                print("Webhook set to:", settings.BOT_WEBHOOK_URL)
            else:
                print("Webhook URL is already set to the desired value.")
        finally:
            await bot.session.close()  # Ensure session is closed
