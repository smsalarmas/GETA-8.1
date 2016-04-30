from Crypto.Cipher import XOR
from base64 import b64encode, b64decode
import uuid
from socket import gethostname
from ConfigParser import ConfigParser
import datetime
import pyodbc
from urllib2 import urlopen
from check import LicCheckRemote
from apscheduler.schedulers.qt import QtScheduler
from apscheduler.triggers.interval import IntervalTrigger
import threading


class Remote(object):
	def __init__(self,app):
		self.app = app
		self.app.remoteprocess = self
	def Decision(self,st):
		#Este es el metodo a reescribir para cada app
		if st == False:
			print 'Vencido, Deteniendo'
			self.scheduler.shutdown(wait=False)
			self.app.trayIcon.showMessage("Licencia Vencida", "Contacte con el administrador del Software. Licencia Vencida" )
			self.app.exitEvent()

	def Iniciar(self):
		self.scheduler = QtScheduler()
		self.trigger = IntervalTrigger(hours=1)
		self.scheduler.add_job(self.Proceso, self.trigger)
		self.scheduler.start()
		t = threading.Thread(target=self.Proceso)
		t.start()


	def Proceso(self):
		self.ObtenerFecha()	
		self.ObtenerConexion()
		self.ValidarBDRemote()
		status =  self.ValidarFecha()
		self.Decision(status)

	def ObtenerConexion(self):
		config = ConfigParser()
		config.read("conf/config.ini")
		self.conexion = config.get('REMOTE', 'conexion')
		ps = b64decode('MjAxMDE3MzMtOTYwOTkyNg==')
		xorps = XOR.new(str(ps))
		self.conexion = xorps.decrypt(b64decode(str(self.conexion)))

	def ObtenerFecha(self):
		try:
			config = ConfigParser()
			config.read("conf/config.ini")
			date = config.get('REMOTE', 'date')
			ps = b64decode('MjAxMDE3MzMtOTYwOTkyNg==')
			xorps = XOR.new(str(ps))
			date = xorps.decrypt(b64decode(str(date)))	
			date = date.split(',')
			self.date = datetime.datetime(int(date[0]),int(date[1]),int(date[2]),int(date[3]),int(date[4]),int(date[5]))
			print self.date
		except:
			self.Decision(False)


	def ValidarFecha(self):
		if self.date >= datetime.datetime.now() and self.status == True:
			return True
		else:
			return False

	def ValidarBDRemote(self):
		#try:
			self.cnxn = pyodbc.connect(self.conexion)
			self.cursor = self.cnxn.cursor()
			self.cursor.execute("SELECT * FROM t365_Valid WHERE MAC = ?",str(':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1])))
			rows = self.cursor.fetchall()
			if rows:
				fecha = rows[0].datelic
				self.date = fecha
				self.status = rows[0].status
				print fecha
				fechaini = str(fecha.year)+','+str(fecha.month)+','+str(fecha.day)+','+str(fecha.hour)+','+str(fecha.minute)+','+str(fecha.second)
				print fechaini
				deco = XOR.new(b64decode('MjAxMDE3MzMtOTYwOTkyNg=='))
				fechaini =  b64encode(deco.encrypt(str(fechaini)))
				config = ConfigParser()
				config.read("conf/config.ini")
				config.set('REMOTE', 'date', fechaini)
				# Writing our configuration file to 'example.ini'
				with open("conf/config.ini", 'wb') as configfile:
				    config.write(configfile)
			else:
				self.InsertarBDRemote()
		#except:
		#	pass		

	def InsertarBDRemote(self):
		print 'No existe cliente insertando'
		self.IPPublica = '0'
		try:
			self.IPPublica = urlopen('http://ip.42.pl/raw').read().encode('utf8')
		except:
			pass
		nameempresa = 'Desconocido'
		try:
			config = ConfigParser()
			config.read("conf/config.ini")
			string = config.get('BASE DE DATOS', 'conexion')
			ps = b64decode('MjAxMDE3MzMtOTYwOTkyNg==')
			xorps = XOR.new(str(ps))
			string = xorps.decrypt(b64decode(str(string)))	
			self.cnxn1 = pyodbc.connect(string)
			self.cursor1 = self.cnxn1.cursor()
			self.cursor1.execute("SELECT nombre FROM t365_Empresas WHERE master = 1")
			rows = self.cursor1.fetchall()
			if rows:
				nameempresa = rows[0].nombre
			self.cursor.execute("INSERT INTO [t365_Valid] ([namempresa],[mac],[namepc],[ip]) VALUES (?,?,?,?)",nameempresa,str(':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1])),gethostname(),self.IPPublica)
			self.cnxn.commit()
		except:
			pass













