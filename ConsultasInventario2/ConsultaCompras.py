import os
import threading
import time
from ConexionRabbitMQ import ConexionRabbitMQ
from dotenv import load_dotenv
from pubsub import pub


class ConsultaCompras():

    def __init__(self):
        load_dotenv()
        self.conexionListenerRMQ = None
        self.conexionListener = None
        self.channelListener = None
        self.hiloListener = None
        self.YaFuiCreadoListener=False
        

        self.conexionReemplazarRMQ = ConexionRabbitMQ()
        self.conexionReemplazar = None
        self.channelReemplazar = None
        self.hiloReemplazar = None

        self.conexionReemplazoporCaidaRMQ = ConexionRabbitMQ()
        self.conexionReemplazoporCaida = None
        self.channelReemplazoporCaida = None
        self.hiloReemplazoporCaida = None
        self.hiloListenerSupender= None

        self.ID_SERVICIO = os.getenv('ID_SERVICIO')
        self.FUNCIONA_INMEDIATO = os.getenv('FUNCIONA_INMEDIATO')
        self.GENERO_ERROR = os.getenv('GENERO_ERROR')
        self.SERVICIO_DEPENDO = os.getenv('SERVICIO_DEPENDO')
        self.SERVICIO_QUE_DEPENDE_DE_MI = os.getenv(
            'SERVICIO_QUE_DEPENDE_DE_MI')
        
        #credenciales de conexion
        self.USUARIO_RABBIT = os.getenv('USUARIO_RABBIT')
        self.CONTRASENIA_RABBIT = os.getenv('CONTRASENIA_RABBIT')
        self.IP = os.getenv('IP')
        self.PUERTO = os.getenv('PORT')
       
        #colas
        self.COLA_PEDIR_REEMPLAZO = os.getenv('COLA_PEDIR_REEMPLAZO')
        self.COLA_CONSULTA = os.getenv('COLA_CONSULTA')
        self.COLA_CANCELAR_AYUDA = os.getenv('COLA_CANCELAR_AYUDA')

        #mensajes    
        self.MENSAJE_ESTA_BIEN = os.getenv('MENSAJE_ESTA_BIEN')
        self.MENSAJE_AUXILIO = os.getenv('MENSAJE_AUXILIO')
        self.MENSAJE_CANCELAR_AYUDA=os.getenv('MENSAJE_CANCELAR_AYUDA')
       
        self.conexionPeticion = None
        self.conexionMensaje = None
        self.channel = None
        self.update = None
        

    def do_something(self):
        # do whatever I need to do
        #print("I've changed\n")
        self.update()

    def renovarListener(self):
        self.crearListener()
        self.conexionListenerRMQ.solicitarReemplazoporCaida=self.solicitarReemplazoporCaida
        self.conexionListenerRMQ.renovarListener=self.renovarListener
        self.hiloListener.start()     

    def iniciarProcesoRecepcion(self):

        # ejecutamos los hilos
        if self.FUNCIONA_INMEDIATO == 'True':
            self.renovarListener()
        else:
          self.crearListenerParaRemplazar()
        
        # self.hiloNecesitoReemplazo.start()
        # primero creare mi ser
        # self.solicitarReemplazoporCaida()
        # self.do_something()

    # Aqui recibo mensajes que vienen de compras
    def crearListener(self):
        #print("cree listener")
        self.conexionListenerRMQ = ConexionRabbitMQ()
        self.conexionListener = self.conexionListenerRMQ.crearConexion(
            self.IP, self.PUERTO, self.USUARIO_RABBIT, self.CONTRASENIA_RABBIT)
        self.channelListener = self.conexionListenerRMQ.creacionCola(
            self.conexionListener, self.COLA_CONSULTA)
        self.hiloListener = threading.Thread(
            target=self.conexionListenerRMQ.crearListener, args=(self.COLA_CONSULTA,))
        self.conexionListenerRMQ.suspendeMiReemplazo=self.suspendeMiReemplazo
        self.YaFuiCreadoListener=True

    # Aqui me envian la alerta si necesitan mi ayuda
    def crearListenerParaRemplazar(self):
        self.hiloListener =None
        conexionReemplazarRMQ= ConexionRabbitMQ()  
        conexionReemplazar = conexionReemplazarRMQ.crearConexion(
            self.IP, self.PUERTO, self.USUARIO_RABBIT, self.CONTRASENIA_RABBIT)
        channelReemplazar = conexionReemplazarRMQ.creacionCola(
            conexionReemplazar, self.COLA_PEDIR_REEMPLAZO)
        hiloReemplazar = threading.Thread(
            target=conexionReemplazarRMQ.crearListener, args=(self.COLA_PEDIR_REEMPLAZO,))
        conexionReemplazarRMQ.retornoMensaje=self.procedeARemplazarme
        hiloReemplazar.start()
        self.hiloReemplazar=hiloReemplazar
    # Aqui envio el mensaje para que me re emplaze
    def solicitarReemplazoporCaida(self):

        #print("solicite mi reemplazo por caida")
        conexionReemplazoporCaidaRMQ= ConexionRabbitMQ()
        conexionReemplazoporCaida = conexionReemplazoporCaidaRMQ.crearConexion(
            self.IP, self.PUERTO, self.USUARIO_RABBIT, self.CONTRASENIA_RABBIT)
        channelReemplazoporCaida =conexionReemplazoporCaidaRMQ.creacionCola(
           conexionReemplazoporCaida, self.COLA_PEDIR_REEMPLAZO)
        hiloReemplazoporCaida = threading.Thread(target=conexionReemplazoporCaidaRMQ.enviarMensaje, args=(
             self.COLA_PEDIR_REEMPLAZO, self.MENSAJE_AUXILIO ,))
        hiloReemplazoporCaida.start()
        
        #print("envie mensaje")
       

    def procedeARemplazarme(self):
        print("Oye reemplazame")
        time.sleep(0.3)
        if(self.YaFuiCreadoListener==False):
            self.crearListener()
            self.conexionListenerRMQ.suspendeMiReemplazo=self.suspendeMiReemplazo
            self.hiloListener.start()
        else :
             self.conexionListenerRMQ.reiniciarServicio()
        self.ListenerSuspendeAyuda()
        
    
    def suspendeMiReemplazo(self):
        print("Suspende mi reemplazo")
        self.mensajeSuspendeAyuda()
        time.sleep(0.3)
        #self.renovarListener()
          #envio mensaje si  ya no necesitan mi ayuda
    def mensajeSuspendeAyuda(self):
        print("Ya estoy bien cancela tu ayuda")
        conexionSuspendeAyudaCaidaRMQ= ConexionRabbitMQ()
        conexionSuspendeAyuda = conexionSuspendeAyudaCaidaRMQ.crearConexion(
            self.IP, self.PUERTO, self.USUARIO_RABBIT, self.CONTRASENIA_RABBIT)
        channelReemplazoporCaida =conexionSuspendeAyudaCaidaRMQ.creacionCola(
           conexionSuspendeAyuda, self.COLA_CANCELAR_AYUDA)
        hiloSuspendeAyuda = threading.Thread(target=conexionSuspendeAyudaCaidaRMQ.enviarMensaje, args=(
             self.COLA_CANCELAR_AYUDA,self.MENSAJE_CANCELAR_AYUDA,))
        hiloSuspendeAyuda.start()
        #print("envie mensaje")

      # Aqui me envian la alerta si necesitan mi ayuda
    def ListenerSuspendeAyuda(self):
        conexionSuspendeAyudaRMQ= ConexionRabbitMQ()  
        conexionSuspenderAyuda = conexionSuspendeAyudaRMQ.crearConexion(
            self.IP, self.PUERTO, self.USUARIO_RABBIT, self.CONTRASENIA_RABBIT)
        channelSuspenderAyuda = conexionSuspendeAyudaRMQ.creacionCola(
            conexionSuspenderAyuda, self.COLA_CANCELAR_AYUDA)
        hiloListenerSupender = threading.Thread(
            target=conexionSuspendeAyudaRMQ.crearListener, args=(self.COLA_CANCELAR_AYUDA,))
        conexionSuspendeAyudaRMQ.retornoMensaje=self.cancelarReemplazoServidoPrincipal
        hiloListenerSupender.start()
        self.hiloListenerSupender=hiloListenerSupender
      
    def cancelarReemplazoServidoPrincipal(self):
        print("Cancelar reemplazo")
        self.conexionListenerRMQ.pararConsumo()
        #self.conexionListenerRMQ.cerrarConexion()
        #self.hiloListener=None
        self.crearListenerParaRemplazar() 

   