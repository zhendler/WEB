# consumer.py
import os
import sys
import json
from mongoengine import connect, DoesNotExist
from models import Contact
import pika
from dotenv import load_dotenv

# Завантаження змінних середовища з .env
load_dotenv()

# Отримання URI підключення до MongoDB з файлу .env
MONGODB_URI = os.getenv('MONGODB_URI')

if not MONGODB_URI:
    raise ValueError("Не вдалося знайти MONGODB_URI у файлі .env")

# Підключення до MongoDB
try:
    connect(host=MONGODB_URI)
    print("Підключення до MongoDB успішне!")
except Exception as e:
    print(f"Помилка підключення до MongoDB: {e}")
    sys.exit(1)

# Підключення до RabbitMQ
try:
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='email_queue', durable=True)
    print("Підключення до RabbitMQ успішне!")
except Exception as e:
    print(f"Помилка підключення до RabbitMQ: {e}")
    sys.exit(1)


def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    print(f"Отримано повідомлення для контакту ID: {contact_id}")

    try:
        contact = Contact.objects.get(id=contact_id)
        # Тут ви можете реалізувати логіку обробки контакту, наприклад, надсилання електронного листа
        print(f"Обробка контакту: {contact.fullname} ({contact.email})")

        # Підтвердження обробки повідомлення
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except DoesNotExist:
        print(f"Контакт з ID {contact_id} не знайдений.")
        # Відхилення повідомлення без повторної черги
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    except Exception as e:
        print(f"Помилка при обробці контакту з ID {contact_id}: {e}")
        # Відхилення повідомлення з повторною чергою
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


def main():
    print("Споживач RabbitMQ запущений і очікує повідомлень...")
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='email_queue', on_message_callback=callback)
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Вихід...")
        channel.stop_consuming()
    except Exception as e:
        print(f"Помилка: {e}")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
