from dataclasses import dataclass
from aiogram import Bot


# Класс для хранения токенов и API ключей
@dataclass
class Secrets:
    token: str = '7498212949:AAHSGREejXrW6rUjvFupX92jr0DqnGtHLI8' # TG bot token
    admin_id: int = 123456789  # Telegram ID

bot = Bot(token=Secrets.token)
