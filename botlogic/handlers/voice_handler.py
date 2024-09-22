import uuid
from aiogram import Router, F
from aiogram.types import Message
from botlogic.utils.audio_processing import process_audio_and_respond

# Создаем роутер для обработки сообщений
router = Router()


# Общая функция для обработки аудиофайлов и голосовых сообщений
async def process_audio_file(file_info, bot, message):
    unique_filename = f'audio_{uuid.uuid4()}.mp3'
    
    # Скачиваем аудиофайл с помощью уникального имени
    await bot.download_file(file_info.file_path, unique_filename)

    # Используем общую функцию для обработки и отправки ответа
    await process_audio_and_respond(unique_filename, message)


# Обработка голосовых сообщений
@router.message(F.voice)
async def handle_voice(message: Message):
    voice = message.voice
    file_id = voice.file_id
    file_info = await message.bot.get_file(file_id)

    # Передаем голосовое сообщение на обработку
    await process_audio_file(file_info, message.bot, message)
    # Подтверждение заврешения обработки файла только в личных сообщениях
    if message.chat.type == "private":
        await message.answer("Голосовое сообщение обработано.")


# Обработка аудиофайлов
@router.message(F.audio)
async def handle_audio(message: Message):
    audio = message.audio
    file_id = audio.file_id
    file_info = await message.bot.get_file(file_id)

    # Передаем аудиофайл на обработку
    await process_audio_file(file_info, message.bot, message)
    # Подтверждение заврешения обработки файла только в личных сообщениях
    if message.chat.type == "private":
        await message.answer("Аудиофайл обработан.")
