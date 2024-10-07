# test_connection.py
from mongoengine import connect
from dotenv import load_dotenv
import os

# Завантаження змінних середовища з .env
load_dotenv()

MONGODB_URI = os.getenv('MONGODB_URI')

if not MONGODB_URI:
    raise ValueError("Не вдалося знайти MONGODB_URI у файлі .env")

try:
    connect(host=MONGODB_URI)
    print("Підключення до MongoDB успішне!")
except Exception as e:
    print(f"Помилка підключення: {e}")
