# load_data.py
import json
from mongoengine import connect, DoesNotExist, ValidationError
from models import Author, Quote
from dotenv import load_dotenv
import os


load_dotenv()

# Отримання URI підключення до MongoDB з файлу .env
MONGODB_URI = os.getenv('MONGODB_URI')

if not MONGODB_URI:
    raise ValueError("Не вдалося знайти MONGODB_URI у файлі .env")

print("Спроба підключення до MongoDB...")
try:
    connect(host=MONGODB_URI)
    print("Підключення до MongoDB успішне!")
except Exception as e:
    print(f"Помилка підключення: {e}")
    exit(1)

def get_or_create_author(fullname, defaults):
    """
    Отримати автора за fullname або створити нового, якщо його немає.
    """
    try:
        author = Author.objects.get(fullname=fullname)
        created = False
        print(f"Автор '{fullname}' знайдений в базі даних.")
    except DoesNotExist:
        try:
            # Додавання 'fullname' при створенні нового автора
            author = Author(fullname=fullname, **defaults)
            author.save()
            created = True
            print(f"Автор '{fullname}' створений у базі даних.")
        except ValidationError as ve:
            print(f"ValidationError при створенні автора '{fullname}': {ve}")
            return None, False
    return author, created

def load_authors(file_path):
    """
    Завантажити авторів з JSON файлу до бази даних.
    """
    print(f"Завантаження авторів з файлу: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            authors = json.load(f)
    except FileNotFoundError:
        print(f"Файл '{file_path}' не знайдено.")
        return
    except json.JSONDecodeError as e:
        print(f"Помилка у форматі JSON файлу '{file_path}': {e}")
        return

    for author_data in authors:
        fullname = author_data.get('fullname')
        if not fullname:
            print("Відсутнє поле 'fullname' для одного з авторів.")
            continue
        print(f"Обробка автора: {fullname}")
        author, created = get_or_create_author(
            fullname=fullname,
            defaults={
                'born_date': author_data.get('born_date'),
                'born_location': author_data.get('born_location'),
                'description': author_data.get('description')
            }
        )
        if author:
            if not created:
                try:
                    author.update(
                        born_date=author_data.get('born_date'),
                        born_location=author_data.get('born_location'),
                        description=author_data.get('description')
                    )
                    print(f"Автор '{fullname}' оновлений.")
                except ValidationError as ve:
                    print(f"ValidationError при оновленні автора '{fullname}': {ve}")
            else:
                print(f"Автор '{fullname}' успішно створений.")


def load_quotes(filename):
    print(f"Завантаження цитат з файлу: {filename}")

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            quotes_data = json.load(file)

            for quote_data in quotes_data:
                author_name = quote_data.get('author')
                quote_text = quote_data.get('quote')

                # Знайдемо автора в базі даних за fullname
                author = Author.objects(fullname=author_name).first()

                if author:
                    # Створення нової цитати
                    quote = Quote(author=author, quote=quote_text)
                    quote.save()
                    print(f"Цитата з автором '{author_name}' успішно додана.")
                else:
                    print(f"Автор '{author_name}' не знайдений. Цитата не додана.")

    except FileNotFoundError:
        print(f"Файл '{filename}' не знайдено.")
    except Exception as e:
        print(f"Помилка при завантаженні цитат: {e}")


if __name__ == "__main__":
    load_authors('authors.json')
    load_quotes('quotes.json')
