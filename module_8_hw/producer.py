import json
import os

from mongoengine import connect
from models import Contact
import pika
from faker import Faker
from dotenv import load_dotenv

# Налаштування підключення до MongoDB
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

# Налаштування RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='email_queue', durable=True)

def generate_contacts(n=10):
    fake = Faker()
    contacts = []
    for _ in range(n):
        contact = Contact(
            fullname=fake.name(),
            email=fake.email()
        )
        contacts.append(contact)
    Contact.objects.insert(contacts)
    return contacts

def send_messages(contacts):
    for contact in contacts:
        message = str(contact.id)
        channel.basic_publish(
            exchange='',
            routing_key='email_queue',
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # зробити повідомлення постійним
            )
        )
        print(f"Повідомлення відправлено для контакту: {contact.fullname} ({contact.email})")

def main():
    num_contacts = int(input("Введіть кількість фейкових контактів для створення: "))
    contacts = generate_contacts(num_contacts)
    send_messages(contacts)
    connection.close()

if __name__ == "__main__":
    main()
