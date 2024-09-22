from datetime import datetime

log_file_path = 'summarization_log.txt'


# Логирование сокращенного текста
def log_summarization(text: str, summary: str):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp}\nИсходный текст: {text[:500]}...\nСуммаризация: {summary}\n{'-'*50}\n"
    
    with open(log_file_path, 'a', encoding='utf-8') as log_file:
        log_file.write(log_entry)
