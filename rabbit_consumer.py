import smtplib
import ssl
import os
import django
import pika
import json
from email.message import EmailMessage

RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST", "localhost")
params = pika.ConnectionParameters("rabbitmq")

connection = pika.BlockingConnection(params)
channel = connection.channel()

# Declaring channels
channel.queue_declare(queue="message_alert")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo.settings")
django.setup()


def send_notification_to_emails(data):

    data = json.loads(data)

    # Define email sender and receiver
    email_sender = os.environ.get("EMAIL_HOST_USER")
    email_password = os.environ.get("EMAIL_HOST_PASSWORD")
    email_receiver = data['email_receiver']

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = data['subject']
    em.set_content(data['body'])

    # Add SSL (layer of security)
    context = ssl.create_default_context()

    # Log in and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())


def alerts_callback(ch, method, properties, body):
    send_notification_to_emails(body)


channel.basic_consume(queue="message_alert", on_message_callback=alerts_callback, auto_ack=True)
channel.start_consuming()
channel.close()
