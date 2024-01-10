import pika

def send_player_created_message(player_data):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='player_created')

    channel.basic_publish(exchange='',
                          routing_key='player_created',
                          body=str(player_data))

    connection.close()
