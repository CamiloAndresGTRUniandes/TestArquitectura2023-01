from ConsultaCompras import ConsultaCompras
import time

def on_notify():
  print("OK, I'm up-to-date")



#, username="yonathan", password="YonathanBr1983*"
print("Hello")
time.sleep(8)
print("Iniciando servicio 1")
consulta= ConsultaCompras()
consulta.update=on_notify
consulta.iniciarProcesoRecepcion()

            