import socket
import time
import traceback
from PyQt4 import QtCore

class NotifySMSA(QtCore.QThread):
	def __init__(self):  
		QtCore.QThread.__init__(self)
		#Variable para Avisar a SMSAlarmas
		self.Avisar = False
		self.Desconectar = False
	def SendNotify(self):

		while True:
			#print "Estatus Conexion = " + str(self.StatusConexionSMSA)
			#print "Desconectar =" + str(self.Desconectar)
			#print "Avisar =" + str(self.Avisar)
			if self.StatusConexionSMSA == True:
				if self.Desconectar == False:
					if self.Avisar == True:
						try:
							#print "Avisando"
							mensajesocket = "CargarDatosTrama"
							self.sock.send(mensajesocket)
							self.Avisar = False
						except:
							self.StatusConexionSMSA = False
					else:
						#print "No hay nada que avisar"
						pass
				elif self.Desconectar == True:
					self.DesconectarSMSA()
					print "Advertencia: Desconectado de SMSA"
					break
				time.sleep(0.5)
			elif self.StatusConexionSMSA == False:   
				try:
					time.sleep(3)
					print "Intentando Conectar Nuevamente a SMSA"
					del self.sock
					self.sock = socket.socket()
					self.StatusConexionSMSA = False
					self.ConectarSMSA()
					self.SendNotify()
				except Exception as exc:
					print(traceback.format_exc())
					print str(exc)+str("Excepcion")

	def ConectarSMSA(self):
		try:
			self.sock.connect(("localhost", 1122))
			self.StatusConexionSMSA = True
			print "Conectado a SMSA"
			self.SendNotify()

		except:
			self.StatusConexionSMSA = False
			print "No se pudo conectar con SMSA"
			self.SendNotify()

	def DesconectarSMSA(self):
		self.sock.close()
		self.StatusConexionSMSA = False
		print "Desconectado de SMSA"

	def run(self):
		self.sock = socket.socket()
		self.StatusConexionSMSA = False
		self.ConectarSMSA()


 
