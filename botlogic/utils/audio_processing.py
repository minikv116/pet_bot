import os
import uuid
from aiogram.types import FSInputFile
from botlogic.models.stt import speech_to_text
from botlogic.models.summarizer import sliding_window_summarization
from botlogic.utils.logger import log_summarization
from botlogic.config import tg_message_lenght

async def process_audio_and_respond(audio_file, message):
    """
    Преобразует аудиофайл в текст, выполняет суммаризацию при необходимости
    и отправляет результаты в виде сообщения или документа.
    
    :param audio_file: Путь к аудиофайлу
    :param message: Объект сообщения, в ответ на которое отправляется результат
    """
    # Преобразуем аудиофайл в текст с помощью функции распознавания речи
    recognized_text = await speech_to_text(audio_file)

    # Удаляем аудиофайл после обработки
    os.remove(audio_file)
    
    # Если длина текста превышает лимит, делаем суммаризацию
    if len(recognized_text) > tg_message_lenght:
        summary = sliding_window_summarization(recognized_text)
        log_summarization(recognized_text, summary)

        # Сохраняем полный текст в файл
        full_text_filename = f'full_text_{uuid.uuid4()}.txt'
        with open(full_text_filename, 'w', encoding='utf-8-sig') as f:
            f.write(recognized_text)
        
        # Отправляем полный текст как документ
        await message.answer_document(FSInputFile(full_text_filename))
        os.remove(full_text_filename)  # Удаляем файл после отправки

        # Отправляем краткую версию текста
        await message.answer(f'Краткий пересказ: {summary}')
    else:
        # Если текст короче лимита, отправляем его полностью
        await message.answer(f'Полный текст: {recognized_text}')
