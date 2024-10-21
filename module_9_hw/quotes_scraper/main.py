import json
from pymongo import MongoClient
from database import QuotesDatabase

# Параметри підключення
user = "zhen"
password = "passwordauth"
db_name = "quotes_database"

# Підключення до бази даних
quotes_db = QuotesDatabase(db_name, user, password)

def load_json_to_mongo(filename, collection):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
        if isinstance(data, list):  # Якщо файл містить список
            collection.insert_many(data)
        else:  # Якщо файл містить один об'єкт
            collection.insert_one(data)

if __name__ == "__main__":
    # Завантаження даних з файлів
    # load_json_to_mongo('quotes.json', quotes_db.quotes_collection)
    # load_json_to_mongo('authors.json', quotes_db.authors_collection)

    # print("Дані успішно завантажені в MongoDB.")

    # # Приклади використання функцій
    # print("Усі цитати:")
    # all_quotes = quotes_db.get_all_quotes()
    # for quote in all_quotes:
    #     print(quote)

    # print("\nУсі автори:")
    # all_authors = quotes_db.get_all_authors()
    # for author in all_authors:
    #     print(author)





    while True:
        print("name - Пошук цитат за автором")
        print("tag - Пошук цитат за тегом")
        print("Exit - Вихід")

        choice = input("Виберіть опцію: ")

        if choice == 'name':
            author = input("Введіть ім'я автора: ")
            quotes = quotes_db.get_quotes_by_author(author)
            for quote in quotes:
                print(f"{quote['text']} — {quote['author']}")

        elif choice == 'tag':
            tag = input("Введіть тег: ")
            quotes = quotes_db.get_quotes_by_tag(tag)
            for quote in quotes:
                print(f"{quote['text']} — {quote['author']}")

        elif choice == 'Exit':
            break

        else:
            print("Неправильний вибір, спробуйте ще раз.")
