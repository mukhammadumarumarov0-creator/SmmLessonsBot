
from django.urls import path
from bot.views.webhook.get_webhook import handle_updates
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("webhook/<str:bot_id>/updates", csrf_exempt(handle_updates)),

]
