import json
from pymongo import MongoClient

# Підключаємося до MongoDB
client = MongoClient("mongodb+srv://zhen:passwordauth@cluster01.mijkw.mongodb.net/quotes_db?retryWrites=true&w=majority&appName=Cluster01")

# Обираємо базу даних і колекції
db = client["quotes_database"]
quotes_collection = db["quotes"]
authors_collection = db["authors"]

# Функція для завантаження даних з JSON файлу у MongoDB
def load_json_to_mongo(filename, collection):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
        if isinstance(data, list):  # Якщо файл містить список
            collection.insert_many(data)
        else:  # Якщо файл містить один об'єкт
            collection.insert_one(data)

# Завантажуємо цитати
load_json_to_mongo('quotes.json', quotes_collection)

# Завантажуємо авторів
load_json_to_mongo('authors.json', authors_collection)

print("Дані успішно завантажені в MongoDB!")
