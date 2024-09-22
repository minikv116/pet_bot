import os
from yt_dlp import YoutubeDL 

async def download_audio_from_youtube(youtube_link: str):
    """
    Загружает аудиофайл из YouTube по предоставленной ссылке и сохраняет его в формате MP3.

    :param youtube_link: Ссылка на YouTube для загрузки аудиофайла
    :return: Путь к загруженному аудиофайлу или None, если загрузка не удалась
    """

    # Опции для загрузчика YouTube
    ydl_opts = {
        'format': 'bestaudio/best',  # Загружаем лучший доступный аудиоформат
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',  # Используем FFmpeg для извлечения аудио
                'preferredcodec': 'mp3',  # Конвертируем аудио в формат MP3
                'preferredquality': '192'  # Устанавливаем качество 192 кбит/с
            }
        ],
        'outtmpl': 'audio.%(ext)s',  # Шаблон для имени выходного файла (например, audio.mp3)
    }

    # Создаем экземпляр загрузчика YoutubeDL с заданными параметрами
    with YoutubeDL(ydl_opts) as ydl:
        # Загружаем аудиофайл по предоставленной ссылке
        ydl.download([youtube_link])
        
        # Проверяем, был ли успешно загружен аудиофайл
        if os.path.exists('audio.mp3'):
            # Возвращаем путь к загруженному аудиофайлу
            return 'audio.mp3'  
        # Возвращаем None, если аудиофайл не был загружен
        return None  
