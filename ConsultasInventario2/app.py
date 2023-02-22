from ConsultaCompras import ConsultaCompras
from pubsub import pub
import time

def on_notify():
  print("OK, I'm up-to-date")
time.sleep(3)
print("Iniciando servicio 2")
consulta= ConsultaCompras()
consulta.update=on_notify
consulta.iniciarProcesoRecepcion()

            