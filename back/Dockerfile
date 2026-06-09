FROM python:3.10-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода
COPY . .

# Создание папки для медиа и статики
RUN mkdir -p media static

# Открываем порт
EXPOSE 8000

# Запуск
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]