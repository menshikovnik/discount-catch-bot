# Используем базовый образ с Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем все файлы в контейнер
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt


# Указываем команду для запуска приложения
CMD ["python", "-m", "catch_bot.bot_start"]