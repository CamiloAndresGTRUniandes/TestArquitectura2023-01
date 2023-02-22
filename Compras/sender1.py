#!/usr/bin/env python
import pika
import sys
import os

#, username="yonathan", password="YonathanBr1983*"
print("Hello")
i=1

while i<104:
  try:
    parameters=  pika.ConnectionParameters('127.0.0.1', 5672,'/',pika.PlainCredentials(username='yonathan', password='YonathanBr1983*'))
    connection = pika.BlockingConnection(
      parameters
    )
    channel = connection.channel()

    channel.queue_declare(queue='hello-2')

    channel.basic_publish(exchange='', routing_key='hello-2', body=f'{i}')
    print(f' [x] Sent Hello World!  {i}'  )
    connection.close()
    i=i+1
  except NameError:
    print(NameError)


print("Fin")