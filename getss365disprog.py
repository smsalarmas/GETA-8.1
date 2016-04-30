from bd import BasedeDatos
from globalvars import *
from PyQt4 import QtCore
import time
from date import LaFecha


class GetSS365Disprog(QtCore.QThread):  
	def __init__(self):  
		QtCore.QThread.__init__(self)
		self.Timeout = 45
		self.detener = False
	def ConectarBD(self):
		self.BD1 = BasedeDatos()
		self.BD1.Conectar()
	def SearchSS365Disprog(self):
			#print "Entre"
			Result = self.BD1.Seleccionar("SELECT id, id_cliente, zona FROM t365_SS365Disprog WHERE status = 0""")
			print 'Arranco GetSS365Disprog'
			print Result
			if Result:
				for r in Result:
					global listass365disprog
					disp = str(r.id_cliente)+','+str(r.zona)
					listass365disprog.append(disp)
	def Error(self,excep):
		self.dia = LaFecha.damedia()
		self.fecha = LaFecha.damefecha()
		self.ErrorLog=open('history/'+str(self.dia)+'ErrorLog.txt','a')
		self.ErrorLog.write("ERROR"+' - '+str(excep)+' - '+str(self.fecha)+"\n")
		self.ErrorLog.close()	
	def Inicio(self):
		#try:
			while True:
				if self.Timeout == 45:
					self.SearchSS365Disprog()
					self.Timeout = 0
				#Mejorar el Uso del CPU
				self.Timeout = self.Timeout + 1
				if self.detener == True:
					break
				time.sleep(1)
		#except Exception as e:
		#	self.Error(e)
		#	self.Inicio()
	def run(self):
		try:
			self.ConectarBD()
		except:
			print 'No se pudo conectar a BD [GetSS365Disprog]'
		self.Inicio()



