import logging
import sys
import asyncio
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from botlogic.handlers import voice_handler, youtube_handler, commands
from botlogic.settings import bot


# Включение логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )

# Инициализация диспетчера
dp = Dispatcher(storage=MemoryStorage())

# Регистрация обработчиков
dp.include_router(commands.router) 
dp.include_router(voice_handler.router)
dp.include_router(youtube_handler.router)


# Главная функция запуска бота
async def start():
    #await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    asyncio.run(start())
