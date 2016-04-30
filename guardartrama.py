from date import LaFecha
from bd import BasedeDatos
from globalvars import *
from PyQt4 import QtCore
import time
from ConfigParser import ConfigParser


class GuardarTXT(object):
	def __init__(self):
		pass
	def GuardarTXTOk(self,trama):
		dia = LaFecha.damedia()
		fecha = LaFecha.damefecha()
		self.TramasOk=open('history/'+str(dia)+'Tramas.dat','a')
		self.TramasOk.write(trama+' - '+str(fecha)+"\n")
		self.TramasOk.close()
	def GuardarTXTFail(self,trama):
		dia = LaFecha.damedia()
		fecha = LaFecha.damefecha()
		self.TramasFail=open('history/'+str(dia)+'TramasFail.dat','a')
		self.TramasFail.write(trama+' - '+str(fecha)+"\n")
		self.TramasFail.close()
	def GuardarTXTLog(self,param):
		dia = LaFecha.damedia()
		fecha = LaFecha.damefecha()
		self.TramasLog=open('history/'+str(dia)+'Log.dat','a')
		self.TramasLog.write(str(param)+' - '+str(fecha)+"\n")
		self.TramasLog.close()
	def GuardarErrores(self,excep):
		self.dia = LaFecha.damedia()
		self.fecha = LaFecha.damefecha()
		self.ErrorLog=open('history/'+str(self.dia)+'ErrorLog.txt','a')
		self.ErrorLog.write("ERROR"+' - '+str(excep)+' - '+str(self.fecha)+"\n")
		self.ErrorLog.close()	

GuardarTramaObjeto = GuardarTXT()

class GuardarTramaBD(QtCore.QThread):  
	def __init__(self):  
		QtCore.QThread.__init__(self)
		self.LogoutOperadores = 0.0
	def ConectarBD(self):
		self.BD1 = BasedeDatos()
		self.BD1.Conectar()
	def VerificarOperadoresBD(self):
		self.OperadoresBD = True
		try:
			config = ConfigParser()
			config.read("conf/config.ini")
			Res = config.get('CUENTA', 'OperadoresBD')
			if Res == 'False':
				self.OperadoresBD = False
			else:
				self.OperadoresBD = True
		except:
			pass
	def InsertarBD(self):
		#print 'Insentando 1'
		if len(ColaParaGuardar) > 0:
			self.BD1.Insertar("INSERT INTO t365_ReceiveSignal(signal,num_line,customer,event,zone_user,protocol,partition,id_receptor,status)values(?,?,?,?,?,?,?,?,?); """, ColaParaGuardar.pop(0))
			#self.emit(QtCore.SIGNAL("signalNotifySMSA"))
			print 'Insentando 2'
		if len(ColaParaGuardarSenalSistema) > 0:
			self.BD1.Insertar("exec jssp_InsertarTramaSistema ?,?,?,?,?,?,?,?,?", ColaParaGuardarSenalSistema.pop(0))
		#	print 'Insentando 3'
		
		#Para manejar Logueo y Reparticion de Senales por Base de Datos con nuevos Stores y Triggers.
		if self.OperadoresBD:
		#	print 'Insentando 4'

			if self.LogoutOperadores > 5:
				self.BD1.Actualizar("exec sp365_LogoutOperador")
		#		print 'Insentando 5'

				#print 'Enviando Logout Operadores'
				self.LogoutOperadores = 0.0
			self.BD1.Actualizar("exec sp365_AsignarSenal")
			#print 'Asignando Senal'


	#Cree esta funcion para poder reiniciar en caso de error, no estoy seguro
	#Si RUN al iniciar un hilo pueda invocarla de nuevo	
	def Error(self,excep):
		self.dia = LaFecha.damedia()
		self.fecha = LaFecha.damefecha()
		self.ErrorLog=open('history/'+str(self.dia)+'ErrorLog.txt','a')
		self.ErrorLog.write("ERROR"+' - '+str(excep)+' - '+str(self.fecha)+"\n")
		self.ErrorLog.close()	
	def Inicio(self):
		try:
			self.VerificarOperadoresBD()
			while True:
				self.InsertarBD()
				#Mejorar el Uso del CPU
				time.sleep(0.5)
				if self.OperadoresBD:
					self.LogoutOperadores = self.LogoutOperadores + 0.5
		except Exception as e:
			print 'Error al guardar Trama' + str(e)
			self.Error(e)
			self.Inicio()
	def run(self):
		try:
			self.ConectarBD()
		except:
			print 'No se pudo conectar a BD [GTO]'
		self.Inicio()



