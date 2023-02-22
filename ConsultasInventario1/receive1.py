import pika
import sys
import os
import time

def main():

    #time.sleep(1)
    print('Service 1 Received init')

    parameters=  pika.ConnectionParameters('127.0.0.1', 5672,'/',pika.PlainCredentials( username='yonathan', password='YonathanBr1983*'))
    connection = pika.BlockingConnection(
      parameters
    )
    channel = connection.channel()

    channel.queue_declare(queue='hello-2')

    def callback(ch, method, properties, body):
        print(f"1- Received {body} ")
        channel.stop_consuming()
        time.sleep(0.1)
        main()
       

    channel.basic_consume(
        queue='hello-2', on_message_callback=callback, auto_ack=True)

    print(' Service 1  Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        time.sleep(3)
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
