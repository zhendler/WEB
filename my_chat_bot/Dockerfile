# Використовуємо базовий образ з Python
FROM python:3.11-slim

# Встановлюємо робочу директорію всередині контейнера
WORKDIR /app

# Копіюємо файли застосунку до контейнера
COPY . /app

# Встановлюємо залежності з файлу requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Вказуємо команду для запуску застосунку
CMD ["python", "main.py"]
