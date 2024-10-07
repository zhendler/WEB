import os
import sys
import re
from mongoengine import connect, Q
from models import Author, Quote
import redis
from dotenv import load_dotenv
import os

load_dotenv()
# Підключення до MongoDB
MONGODB_URI = os.getenv('MONGODB_URI')
if not MONGODB_URI:
    raise ValueError("Не вдалося знайти MONGODB_URI у файлі .env")

try:
    connect(host=MONGODB_URI)
    print("Підключення до MongoDB успішне!")
except Exception as e:
    print(f"Помилка підключення: {e}")
    exit(1)


# Підключення до Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def search_by_name(name):
    cache_key = f"name:{name}"
    cached = redis_client.get(cache_key)
    if cached:
        print("Результат з кешу:")
        print(cached.decode('utf-8'))
        return

    regex = re.compile(f".*{re.escape(name)}.*", re.IGNORECASE)
    authors = Author.objects(fullname=regex)
    quotes = Quote.objects(author__in=authors)
    result = "\n".join([q.quote for q in quotes])
    print(result if result else "Цитати не знайдено.")

    # Кешування
    redis_client.set(cache_key, result, ex=300)  # кеш на 5 хвилин

def search_by_tag(tag):
    cache_key = f"tag:{tag}"
    cached = redis_client.get(cache_key)
    if cached:
        print("Результат з кешу:")
        print(cached.decode('utf-8'))
        return

    regex = re.compile(f".*{re.escape(tag)}.*", re.IGNORECASE)
    quotes = Quote.objects(tags=regex)
    result = "\n".join([q.quote for q in quotes])
    print(result if result else "Цитати не знайдено.")

    # Кешування
    redis_client.set(cache_key, result, ex=300)  # кеш на 5 хвилин

def search_by_tags(tags):
    cache_key = f"tags:{','.join(tags)}"
    cached = redis_client.get(cache_key)
    if cached:
        print("Результат з кешу:")
        print(cached.decode('utf-8'))
        return

    regex_list = [re.compile(f".*{re.escape(tag)}.*", re.IGNORECASE) for tag in tags]
    query = Q()
    for regex in regex_list:
        query |= Q(tags=regex)
    quotes = Quote.objects(query)
    result = "\n".join([q.quote for q in quotes])
    print(result if result else "Цитати не знайдено.")

    # Кешування
    redis_client.set(cache_key, result, ex=300)  # кеш на 5 хвилин

def main():
    print("Скрипт пошуку цитат. Введіть команду або 'exit' для виходу.")
    while True:
        try:
            user_input = input(">>> ").strip()
            if user_input.lower() == 'exit':
                print("Вихід...")
                break
            if ':' not in user_input:
                print("Невірний формат команди. Використовуйте 'command:value'.")
                continue
            command, value = user_input.split(':', 1)
            command = command.strip().lower()
            value = value.strip()

            if command == 'name':
                search_by_name(value)
            elif command == 'tag':
                search_by_tag(value)
            elif command == 'tags':
                tags = value.split(',')
                search_by_tags(tags)
            else:
                print("Невідома команда.")
        except KeyboardInterrupt:
            print("\nВихід...")
            break
        except Exception as e:
            print(f"Помилка: {e}")

if __name__ == "__main__":
    main()
