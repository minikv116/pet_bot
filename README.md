# Обновляем список пакетов и устанавливаем обновления для системы
sudo apt update
sudo apt upgrade

# Устанавливаем Python 3.10, его виртуальное окружение и pip
sudo apt install -qq -y python3.10 python3.10-venv python3-pip

# Устанавливаем ffmpeg, который необходим для обработки аудио- и видеоданных
sudo apt install -qq -y ffmpeg

# Создаем виртуальное окружение для изоляции зависимостей проекта
python3 -m venv venv

# Активируем виртуальное окружение
source venv/bin/activate

# Устанавливаем зависимости проекта из файла requirements.txt
pip install -r requirements.txt