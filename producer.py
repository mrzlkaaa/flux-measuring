import pika

with pika.BlockingConnection(pika.ConnectionParameters("localhost")) as conn:
    channel = conn.channel()
    channel.queue_declare(queue='hello')
    channel.basic_publish(exchange='',
                        routing_key='hello',
                        body='Hello World!')
    print(" [x] Sent 'Hello World!'")