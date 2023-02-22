import pika
import sys
import os
import time
from dotenv import load_dotenv
load_dotenv()


class ConexionRabbitMQ:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.ID_SERVICIO = os.getenv('ID_SERVICIO')
        self.retornoMensaje=None
        self.suspendeMiReemplazo=None
        self.solicitarReemplazoporCaida = None
        self.renovarListener=None
        self.Cola=None
        self.FUNCIONA_INMEDIATO = os.getenv('FUNCIONA_INMEDIATO')
        self.ID_SERVICIO = os.getenv('ID_SERVICIO')
        self.FUNCIONA_INMEDIATO = os.getenv('FUNCIONA_INMEDIATO')
        self.GENERO_ERROR = os.getenv('GENERO_ERROR')
        self.SERVICIO_DEPENDO = os.getenv('SERVICIO_DEPENDO')
        self.SERVICIO_QUE_DEPENDE_DE_MI = os.getenv(
            'SERVICIO_QUE_DEPENDE_DE_MI')
        self.COLA_CONSULTA = os.getenv('COLA_CONSULTA')
        self.USUARIO_RABBIT = os.getenv('USUARIO_RABBIT')
        self.CONTRASENIA_RABBIT = os.getenv('CONTRASENIA_RABBIT')
        self.COLA_PEDIR_REEMPLAZO = os.getenv('COLA_PEDIR_REEMPLAZO')
        self.MENSAJE_AUXILIO = os.getenv('MENSAJE_AUXILIO')
        self.MENSAJE_ESTA_BIEN = os.getenv('MENSAJE_ESTA_BIEN')
        self.IP = os.getenv('IP')
        self.PUERTO = os.getenv('PORT')
        self.suspendeMiReemplazo=None

        # body of the constructor

    def crearConexion(self, IP, puerto, usuario, contrasenia):
        #print(f"Creacion de conexion del servicio {os.getenv('ID_SERVICIO')}")
        # parameters=  pika.ConnectionParameters(IP, 5672,'/',pika.PlainCredentials( username=usuario, password=contrasenia))
        parameters = pika.ConnectionParameters(
            '127.0.0.1', 5672, '/', pika.PlainCredentials(username='yonathan', password='YonathanBr1983*'))
        self.connection = pika.BlockingConnection(parameters)
        return self.connection

    def creacionCola(self, connection, cola):
        #print(f"Creacion de cola del servicio {os.getenv('ID_SERVICIO')}")
        self.Cola= cola
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=cola)
        return self.channel

    def callback(self, ch, method, properties, body):
        print(f"Camilo Recibe=> {self.ID_SERVICIO}- mensage={body} ")
        ch.basic_ack(delivery_tag = method.delivery_tag)
        time.sleep(0.1)
        if  self.retornoMensaje!=None:
             self.retornoMensaje()
           
        if self.FUNCIONA_INMEDIATO == 'True':
            idMensaje= int(body)
            numero=int(idMensaje)%3
        
            if( numero==0  and int(idMensaje)>9) :
                #print('entre reemplazo')
                #self.channel.stop_consuming()
                #self.connection.close()
                #self.pararConsumo()
                self.solicitarReemplazoporCaida()
                time.sleep(3)
                self.suspendeMiReemplazo()
                time.sleep(0.03)
                self.reiniciarServicio()

    def reiniciarServicio(self):
        self.crearConexion(self.IP, self.PUERTO, self.USUARIO_RABBIT, self.CONTRASENIA_RABBIT)
        self.creacionCola(self.connection, self.Cola)
        self.crearListener(self.Cola)
    
    def pararConsumo(self):
        self.channel.stop_consuming()

    def crearListener(self, cola):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue=cola, on_message_callback=self.callback, auto_ack=False)
        self.channel.start_consuming()

    def enviarMensaje(self, cola, mensaje):
        self.channel.basic_publish(
            exchange='', routing_key=cola, body=f'{mensaje}')
        print(f' Camilo envia   {mensaje}')
        self.cerrarConexion()

    def cerrarConexion(self):
        self.channel.stop_consuming()
        self.connection.close()
