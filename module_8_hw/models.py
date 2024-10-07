from mongoengine import Document, StringField, DateField, ReferenceField, ListField, BooleanField
import datetime

class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()

    meta = {'collection': 'authors'}

class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author, required=True)
    quote = StringField()

    meta = {'collection': 'quotes'}

class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True, unique=True)
    sent = BooleanField(default=False)
    # Додаткові поля за бажанням
    created_at = DateField(default=datetime.datetime.utcnow)

    meta = {'collection': 'contacts'}
