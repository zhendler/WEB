from pymongo import MongoClient

class QuotesDatabase:
    def __init__(self, db_name, user, password):
        self.client = MongoClient(f"mongodb+srv://{user}:{password}@cluster01.mijkw.mongodb.net/{db_name}")
        self.db = self.client[db_name]
        self.quotes_collection = self.db["quotes"]
        self.authors_collection = self.db["authors"]

    def get_all_quotes(self):
        return list(self.quotes_collection.find())

    def get_all_authors(self):
        return list(self.authors_collection.find())

    def get_quotes_by_author(self, author_name):
        return list(self.quotes_collection.find({"author": author_name}))



