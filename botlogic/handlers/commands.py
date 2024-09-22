from aiogram import Router, types
from aiogram.filters import Command
from botlogic.config import tg_message_lenght

# Создаем роутер для обработки сообщений
router = Router()


@router.message(Command("start"))
async def start(message: types.Message):
    # Проверка, что сообщение отправлено в личный чат
    if message.chat.type == "private":
        await message.answer(f"Добро пожаловать. Это бот помощник для расшифровки звуковых сообщений и аудиодорожек из видео в YouTube. Отправь голосовое сообщение или ссылку на YouTube.")
    else:
        # Если команда "/start" вызвана не в личном чате (например, в группе), бот может либо игнорировать ее,
        # либо отправить другое сообщение, либо вообще ничего не делать.
       await message.answer(f"Добро пожаловать. Это бот помощник для расшифровки звуковых сообщений. Любое звуковое сообщение в чате будет расшифровано в текст.")


@router.message(Command("help"))
async def start(message: types.Message):
    # Проверка, что сообщение отправлено в личный чат
    if message.chat.type == "private":
        await message.answer(f"Это бот помощник для расшифровки звуковых сообщений и аудиодорожек из видео в YouTube. Сообщения длиной более {tg_message_lenght} символов будут кратко пересказаны, полная расшифровку будет отправлена в дополнительном сообщении в текстовом файле.")
    else:
        # Если команда "/start" вызвана не в личном чате (например, в группе), бот может либо игнорировать ее,
        # либо отправить другое сообщение, либо вообще ничего не делать.
       await message.answer(f"Это бот помощник для расшифровки звуковых сообщений. Сообщения длиной более {tg_message_lenght} символов будут кратко пересказаны, полная расшифровку будет отправлена в дополнительном сообщении в текстовом файле.")
