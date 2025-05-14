# Dockerfile
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем JSON с данными и код бота
COPY data.json bot.py ./

# Переменная окружения для токена (можно задавать при запуске)
ENV TELEGRAM_TOKEN=""

# Запуск бота
CMD ["python", "bot.py"]