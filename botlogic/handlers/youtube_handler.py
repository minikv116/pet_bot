from aiogram import Router, F
from aiogram.types import Message
from botlogic.utils.downloader import download_audio_from_youtube
from botlogic.utils.audio_processing import process_audio_and_respond 

# Создаем роутер для обработки сообщений
router = Router()


# Обработчик сообщений с YouTube ссылками, работает только в личных сообщениях
#@router.message(lambda msg: ("youtube.com" in msg.text or "youtu.be" in msg.text or "rutube.ru" in msg.text) and msg.chat.type == "private")
@router.message(F.text.func(lambda text: "youtube.com" in text or "youtu.be" in text), F.chat.type == "private")
async def handle_youtube_link(message: Message):
    # Извлекаем ссылку на YouTube из сообщения
    youtube_link = message.text
    # Максимальное количество попыток для загрузки аудио с YouTube
    max_attempts = 3  

    # Переменная для хранения имени загруженного аудиофайла
    audio_file = None  
    for attempt in range(1, max_attempts + 1):
        # Уведомляем пользователя о попытке загрузки аудио
        await message.answer(f'Попытка {attempt} загрузить аудио из видео...')
        
        # Пытаемся скачать аудиофайл с YouTube с помощью функции download_audio_from_youtube
        audio_file = await download_audio_from_youtube(youtube_link)
        
        # Если загрузка успешна, прерываем цикл
        if audio_file:
            break

    # Если аудиофайл успешно загружен
    if audio_file:
        # Используем общую функцию для обработки аудиофайла и отправки текста пользователю
        await process_audio_and_respond(audio_file, message)
        # Сообщение пользователю о завершении обработки
        await message.answer("Видеофайл обработан.")  
    else:
        # Если после нескольких попыток не удалось скачать аудиофайл, отправляем ошибочное сообщение
        await message.answer("Не удалось загрузить аудиофайл с YouTube после нескольких попыток.")
