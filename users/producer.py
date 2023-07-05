import logging
import pika
import time

while True:
    try:
        params = pika.ConnectionParameters("rabbitmq", heartbeat=0)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        logging.info("Producer.py successfully connected to RBMQ server")
        break
    except Exception as e:
        logging.warning(e)
        time.sleep(5)
        logging.warning("Try to reconnect in 5 secs")


def publish(key, body):
    logging.info(f"Publishing {key}")
    channel.basic_publish(exchange='', routing_key=key, body=body)
