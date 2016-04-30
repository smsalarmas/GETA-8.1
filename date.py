#Importamos Modulo de Tiempo para la Hora de la Trama
import time
import datetime

class Fecha(object):
	def __init__(self):
		pass
	def damefecha(self):
		self.fechaactual = time.strftime('%d %b %y' + ' %H:%M:%S')
		return self.fechaactual
	def damedia(self):
		self.diaactual = time.strftime('%d %b %y')
		return self.diaactual
	def damefechadatetime(self):
		self.fecha = datetime.datetime.now()
		return self.fecha
LaFecha = Fecha()
