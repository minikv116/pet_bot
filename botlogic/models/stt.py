from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from botlogic.config import device, torch_dtype

# Идентификатор модели для распознавания речи
stt_model_id = "openai/whisper-large-v3"

# Загрузка модели для последовательного распознавания речи (Whisper)
stt_model = AutoModelForSpeechSeq2Seq.from_pretrained(stt_model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True).to(device)

# Загрузка процессора для обработки аудиоданных (фичи и токенизация)
processor = AutoProcessor.from_pretrained(stt_model_id)

# Создание пайплайна для автоматического распознавания речи (ASR)
stt_pipe = pipeline(
    "automatic-speech-recognition",  # Тип задачи: распознавание речи
    model=stt_model,                 # Модель для последовательного распознавания речи
    tokenizer=processor.tokenizer,   # Токенизатор, который преобразует текстовые данные
    feature_extractor=processor.feature_extractor,  # Фича-экстрактор для обработки аудиосигнала
    device=device                    # Устройство для выполнения модели (CPU или GPU)
)


# Асинхронная функция для преобразования аудиофайла в текст
async def speech_to_text(audio_file: str) -> str:
    return stt_pipe(audio_file, return_timestamps=True)['text']