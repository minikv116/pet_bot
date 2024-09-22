import torch
from transformers import T5ForConditionalGeneration, GPT2Tokenizer
from botlogic.config import device

# Идентификатор модели для суммаризации текста на русском языке
summarizer_model_id = "RussianNLP/FRED-T5-Summarizer"

# Загрузка модели для генерации текстов (суммаризация)
model = T5ForConditionalGeneration.from_pretrained(summarizer_model_id).to(device)

# Загрузка токенизатора GPT-2 для русскоязычной модели с добавлением EOS-токена
tokenizer = GPT2Tokenizer.from_pretrained(summarizer_model_id, eos_token='</s>')


# Функция генерации суммаризации текста для части токенов
def generate_summary(part_tokens, min_new_tokens=50, max_new_tokens=150):
    """
    Генерирует краткое содержание для текста.
        
    :param min_new_tokens: минимальное количество токенов в генерируемом ответе
    :param max_new_tokens: максимальное количество токенов в генерируемом ответе
    :return: краткое содержание текста
    """    

    # Очищаем кэш GPU для экономии памяти
    torch.cuda.empty_cache()

    # Формируем текст для ввода в модель, добавляем специальную метку для задачи суммаризации
    input_text = '<LM> Сократи текст. \n ' + tokenizer.decode(part_tokens)
    
    # Преобразуем текст в идентификаторы токенов и переносим на устройство (например, GPU)
    input_ids = torch.tensor([tokenizer.encode(input_text)]).to('cuda')

    # Генерируем суммаризацию с помощью модели
    outputs = model.generate(
        input_ids,  # Входные идентификаторы токенов
        eos_token_id=tokenizer.eos_token_id,  # Идентификатор конца предложения
        num_beams=5,  # Количество лучей для поиска лучшего варианта
        min_new_tokens=min_new_tokens,  # Минимальное количество новых токенов в выводе
        max_new_tokens=max_new_tokens,  # Максимальное количество новых токенов в выводе
        do_sample=True,  # Использование выборки
        no_repeat_ngram_size=4,  # Запрет на повторение одинаковых 4-грамм
        top_p=0.9  # Использование метода "nucleus sampling" с порогом 0.9
    )

    # Преобразуем сгенерированные токены обратно в текст, убирая специальные символы
    return tokenizer.decode(outputs[0][1:-1])


# Функция суммаризации текста с использованием скользящего окна
def sliding_window_summarization(text, max_tokens_per_part=1500, overlap=500):
    """
    Основная функция для суммаризации. Оюбрабатывает текст скользящим окном с перекрытием

    :param max_tokens_per_part: максимальная длина окна 1500 токенов. Ограничение модели 1536 токенов
    :param max_tokens_per_part: перекрытие окна в токенах
    :return: краткое содержание всего текста
    """

    # Преобразуем текст в последовательность токенов
    tokens = tokenizer.encode(text)
    # Общее количество токенов
    total_tokens = len(tokens)  

    # Если длина текста меньше или равна количеству токенов в части, делаем простую суммаризацию
    if total_tokens <= max_tokens_per_part:
        return generate_summary(tokens, min_new_tokens=30,  max_new_tokens=80)
    

    # Рекурсивная функция для суммаризации частей текста
    def recursive_summarization(start):
        # Определяем конец текущей части текста
        end = min(start + max_tokens_per_part, total_tokens)
        # Выделяем токены для текущей части
        part_tokens = tokens[start:end]  

        # Генерируем суммаризацию для этой части
        summary_part = generate_summary(part_tokens)

        # Если мы дошли до конца текста, возвращаем эту часть
        if end >= total_tokens:
            return summary_part

        # Рекурсивно обрабатываем следующую часть текста с перекрытием
        next_part_summary = recursive_summarization(start + max_tokens_per_part - overlap)
        return summary_part + ' ' + next_part_summary

    # Начинаем суммаризацию с первой части текста рекурсивно
    summarized_text = recursive_summarization(0)

    # Окончательная суммаризация для объединенного текста
    tokens = tokenizer.encode(summarized_text)
    return generate_summary(tokens, min_new_tokens=30,  max_new_tokens=80)
