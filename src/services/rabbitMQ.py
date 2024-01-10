import pika
import os

def send_player_created_message(player_data):
    rabbitmq_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")
    
    params = pika.URLParameters(rabbitmq_url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue='player_created')

    channel.basic_publish(exchange='',
                          routing_key='player_created',
                          body=str(player_data))

    connection.close()
