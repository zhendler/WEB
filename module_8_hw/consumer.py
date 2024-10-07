import time
import pika
from mongoengine import connect
from models import Contact

# Налаштування підключення до MongoDB
connect(host='mongodb+srv://zhendlerbing:<db_password>@cluster01.mijkw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster01')

# Налаштування RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='email_queue', durable=True)

def send_email_stub(contact):
    # Функція-заглушка для імітації надсилання email
    print(f"Надсилання email до {contact.email}...")
    time.sleep(1)  # Імітація затримки
    print(f"Email до {contact.email} успішно надіслано.")

def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    contact = Contact.objects(id=contact_id).first()
    if contact:
        send_email_stub(contact)
        contact.update(sent=True)
        print(f"Поле 'sent' оновлено для контакту: {contact.fullname}")
    else:
        print(f"Контакт з ID {contact_id} не знайдено.")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='email_queue', on_message_callback=callback)
    print('Очікування повідомлень. Для виходу натисніть CTRL+C')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    connection.close()

if __name__ == "__main__":
    main()
