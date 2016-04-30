import re
import pyodbc
from PyQt4.QtGui import *
from date import *
from globalvars import *
from bd import *
from guardartrama import *

#Formatos de SS365
#Identico a ContactID del Surguard pero no guarda directo en ReceiveSignal 
#Guarda por el Store InsertarTramaSistema porque tengo el id_cliente directamente.

class ContactID_SS365(object):
	def __init__(self):
		self.nombre = "ContactID del SS365" 
		self.nombreformato = "CID"
		self.numprotocolo = '2'
		self.eregular = '(5|Q)(....|...|.....) (18|58) ([^ ]{0,}) ([^ ]{0,}) ([^ ]{0,}) ([\S]{0,})'
	def tratar(self,trama,numpuerto,prefijo,idcliente):
		#colaCIDMLR2.append(trama)
		try:
			self.patron = re.compile('(?P<Identificador>5)(?P<Receptor>\d\d)(?P<Linea>[0-9a-zA-Z]{1,3})(?P<Espacio> )(?P<ID>18)(?P<Espacio1> )(?P<Abonado>[^ ]{1,20})(?P<Espacio2> )(?P<Evento>[^ ]{1,20})(?P<Espacio3> )(?P<Particion>[^ ]{1,20})(?P<Espacio4> )(?P<ZonaUsuario>[^ ]{1,20})')
			self.dividida = self.patron.search(trama)
			#Para quitarle los 0 a la izq a la linea, solcuion temporal mientras se arregla la bd
			self.linea = int(self.dividida.group("Linea"))
			#Agregando el prefijo al Abonado en caso de que lo tenga
			self.Abonado = str(self.dividida.group('Abonado'))
			#if int(prefijo) >= 1000:
			#	self.Abonado = int(self.Abonado) + int(prefijo)
			self.datosparaGUI = (str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),self.dividida.group('Particion'),self.dividida.group('Linea'),self.nombreformato,LaFecha.damefecha())
			self.datosparaBD = (trama,str(idcliente),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),self.numprotocolo,LaFecha.damefechadatetime(),'',self.dividida.group('Linea'),str(numpuerto))
			ColaParaGuardarSenalSistema.append(self.datosparaBD)
			#Variables para Insertar
			fila = 0
			columna = 0
			globalvar["listadetablas"]["tabla"+str(numpuerto)].insertRow(0)
			for item in self.datosparaGUI:
				texto = QTableWidgetItem(item)
				globalvar["listadetablas"]["tabla"+str(numpuerto)].setItem(fila,columna,texto)
				columna = columna + 1
			#Contamos la cantidad de columnas en la tabla
			if globalvar["listadetablas"]["tabla"+str(numpuerto)].rowCount() > 300:
				globalvar["listadetablas"]["tabla"+str(numpuerto)].removeRow(301)
			print self.dividida.groups()
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(self.dividida.groups())
		except Exception as exc:
			self.tramafail = trama + "Error al Tratar Protocolo, Chequea ErrorLOG"
			GuardarTramaObjeto.GuardarTXTFail(self.tramafail)
			GuardarTramaObjeto.GuardarErrores(str(exc))

ContactID_SS365objeto = ContactID_SS365()

#Formatos de SurGuard

class ContactID_SurGuard(object):
	def __init__(self):
		self.nombre = "ContactID del SurGuard" 
		self.nombreformato = "CID"
		self.numprotocolo = '2'
		self.eregular = '(5|Q)(....|...|.....) (18|58)(.................|............)(\d\d|\d)'
	def tratar(self,trama,numpuerto,prefijo):
		#colaCIDMLR2.append(trama)
		try:
			self.patron = re.compile('(?P<Identificador>[5])(?P<Receptor>\d\d)(?P<Linea>[0-9a-zA-Z]{1,3})(?P<Espacio> )(?P<ID>18)(?P<Abonado>....)(?P<Evento>\D\d\d\d)(?P<Particion>\d\d)(?P<ZonaUsuario>\d{2,})')
			self.dividida = self.patron.search(trama)
			#Para quitarle los 0 a la izq a la linea, solcuion temporal mientras se arregla la bd
			self.linea = int(self.dividida.group("Linea"))
			#Agregando el prefijo al Abonado en caso de que lo tenga
			self.Abonado = str(self.dividida.group('Abonado'))
			if int(prefijo) >= 1000:
				self.Abonado = int(self.Abonado) + int(prefijo)
			self.datosparaGUI = (str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),self.dividida.group('Particion'),self.dividida.group('Linea'),self.nombreformato,LaFecha.damefecha())
			self.datosparaBD = (trama,str(self.linea),str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),self.numprotocolo,self.dividida.group('Particion'),numpuerto,'0')
			ColaParaGuardar.append(self.datosparaBD)
			#Variables para Insertar
			fila = 0
			columna = 0
			globalvar["listadetablas"]["tabla"+str(numpuerto)].insertRow(0)
			for item in self.datosparaGUI:
				texto = QTableWidgetItem(item)
				globalvar["listadetablas"]["tabla"+str(numpuerto)].setItem(fila,columna,texto)
				columna = columna + 1
			#Contamos la cantidad de columnas en la tabla
			if globalvar["listadetablas"]["tabla"+str(numpuerto)].rowCount() > 300:
				globalvar["listadetablas"]["tabla"+str(numpuerto)].removeRow(301)
			print self.dividida.groups()
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(self.dividida.groups())
		except Exception as exc:
			self.tramafail = trama + "Error al Tratar Protocolo, Chequea ErrorLOG"
			GuardarTramaObjeto.GuardarTXTFail(self.tramafail)
			GuardarTramaObjeto.GuardarErrores(str(exc))


ContactID_SurGuardobjeto = ContactID_SurGuard()

class Sia1_MLR2(object):
	def __init__(self):
		self.nombre = "Sia1 del SurGuard"
		self.nombreformato = "SIA"
		self.numprotocolo = '1'
		self.eregular = 'S(.\d\d|....|.....)\[#(...|....|.....|......)\|N..(\d\d\d|\d\d|\d)]'
	def tratar(self,trama,numpuerto,prefijo):
		#colaSIA1.append(trama)
		try:
			self.patron = re.compile('(?P<Identificador>S)(?P<Receptor>[0-9]{1,2})(?P<Linea>\d\d\d|\d\d|\d)(?P<Nada>\[\#)(?P<Abonado>[a-z0-9]{1,6})(?P<Nada2>\|N)(?P<Evento>\D\D)(?P<ZonaUsuario>[0-9]{1,6})')
			self.dividida = self.patron.search(trama)
			#Para quitarle los 0 a la izq a la linea, solcuion temporal mientras se arregla la bd
			self.linea = int(self.dividida.group("Linea"))

			#Agregando el prefijo al Abonado en caso de que lo tenga
			self.Abonado = str(self.dividida.group('Abonado'))
			if int(prefijo) >= 1000:
				self.Abonado = int(self.Abonado) + int(prefijo)

			self.datosparaGUI = (str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),'SP',self.dividida.group('Linea'),self.nombreformato,LaFecha.damefecha())
			self.datosparaBD = (trama,str(self.linea),str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),self.numprotocolo,'1',numpuerto,'0')
			#Insertar En Base de Datos
			ColaParaGuardar.append(self.datosparaBD)
			fila = 0
			columna = 0
			globalvar["listadetablas"]["tabla"+str(numpuerto)].insertRow(0)
			for item in self.datosparaGUI:
				texto = QTableWidgetItem(item)
				globalvar["listadetablas"]["tabla"+str(numpuerto)].setItem(fila,columna,texto)
				columna = columna + 1
			#Contamos la cantidad de columnas en la tabla
			if globalvar["listadetablas"]["tabla"+str(numpuerto)].rowCount() > 300:
				globalvar["listadetablas"]["tabla"+str(numpuerto)].removeRow(301)
			print self.dividida.groups()
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(self.dividida.groups())
		except Exception as exc:
			self.tramafail = trama + "Error al Tratar Protocolo, Chequea ErrorLOG"
			GuardarTramaObjeto.GuardarTXTFail(self.tramafail)
			GuardarTramaObjeto.GuardarErrores(str(exc))


Sia1_MLR2objeto = Sia1_MLR2()

class SiaLevel1_1_SurGuard(object): #Agregado Nuevo, Este parece ser LVL 1
	def __init__(self):
		self.nombre = "SiaOld del SurGuard"
		self.nombreformato = "SIA"
		self.numprotocolo = '1'
		self.eregular = '3...   .......\D\D....'
	def tratar(self,trama,numpuerto,prefijo):
		try:
			self.patron = re.compile('(?P<Identificador>[3])(?P<Receptor>\d\d)(?P<Linea>[0-9]{1,3})(?P<Separador> {4,9})(?P<Abonado>[0-9]{1,6})(?P<Evento>\D\D)(?P<Particion>\d|)(?P<Espacio>   |  | |)(?P<ZonaUsuario>\S\S\S|\S\S|\S)')
			self.dividida = self.patron.search(trama)
			#Para quitarle los 0 a la izq a la linea, solcuion temporal mientras se arregla la bd
			self.linea = int(self.dividida.group("Linea"))

			#Agregando el prefijo al Abonado en caso de que lo tenga
			self.Abonado = str(self.dividida.group('Abonado'))
			if int(prefijo) >= 1000:
				self.Abonado = int(self.Abonado) + int(prefijo)

			#Si llega sin la particion
			if self.dividida.group('Particion') == '':
				self.datosparaGUI = (str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),'SP',self.dividida.group('Linea'),self.nombreformato,LaFecha.damefecha())
				self.datosparaBD = (trama,str(self.linea),str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),self.numprotocolo,'1',numpuerto,'0')
			#Si llega con la particion
			else:
				self.datosparaGUI = (str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),self.dividida.group('Particion'),self.dividida.group('Linea'),self.nombreformato,LaFecha.damefecha())
				self.datosparaBD = (trama,str(self.linea),str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),self.numprotocolo,self.dividida.group('Particion'),numpuerto,'0')
			#Insertar En Base de Datos
			ColaParaGuardar.append(self.datosparaBD)
			fila = 0
			columna = 0
			globalvar["listadetablas"]["tabla"+str(numpuerto)].insertRow(0)
			for item in self.datosparaGUI:
				texto = QTableWidgetItem(item)
				globalvar["listadetablas"]["tabla"+str(numpuerto)].setItem(fila,columna,texto)
				columna = columna + 1
			#Contamos la cantidad de columnas en la tabla
			if globalvar["listadetablas"]["tabla"+str(numpuerto)].rowCount() > 300:
				globalvar["listadetablas"]["tabla"+str(numpuerto)].removeRow(301)
			print self.dividida.groups()
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(self.dividida.groups())
		except Exception as exc:
			self.tramafail = trama + "Error al Tratar Protocolo, Chequea ErrorLOG"
			GuardarTramaObjeto.GuardarTXTFail(self.tramafail)
			GuardarTramaObjeto.GuardarErrores(str(exc))


SiaLevel1_1_SurGuardobjeto = SiaLevel1_1_SurGuard()

class SiaLevel1_2_SurGuard(object): #Agregado Nuevo, Este parece ser LVL 1
	def __init__(self):
		self.nombre = "SiaOld del SurGuard"
		self.nombreformato = "SIA"
		self.numprotocolo = '1'
		self.eregular = '3...   .......r\d....'
	def tratar(self,trama,numpuerto,prefijo):
		try:
			self.patron = re.compile('(?P<Identificador>[3])(?P<Receptor>\d\d)(?P<Linea>[0-9]{1,3})(?P<Separador> {4,9})(?P<Abonado>[0-9]{1,6})(?P<Nada>r)(?P<Particion>\d)(?P<Evento>\S\S)(?P<ZonaUsuario>\S\S\S|\S\S|\S)')
			self.dividida = self.patron.search(trama)
			#Para quitarle los 0 a la izq a la linea, solcuion temporal mientras se arregla la bd
			self.linea = int(self.dividida.group("Linea"))			
			#Agregando el prefijo al Abonado en caso de que lo tenga
			self.Abonado = str(self.dividida.group('Abonado'))
			if int(prefijo) >= 1000:
				self.Abonado = int(self.Abonado) + int(prefijo)

			self.datosparaGUI = (str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),self.dividida.group('Particion'),self.dividida.group('Linea'),self.nombreformato,LaFecha.damefecha())
			self.datosparaBD = (trama,str(self.linea),str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),self.numprotocolo,self.dividida.group('Particion'),numpuerto,'0')
			#Insertar En Base de Datos
			ColaParaGuardar.append(self.datosparaBD)
			fila = 0
			columna = 0
			globalvar["listadetablas"]["tabla"+str(numpuerto)].insertRow(0)
			for item in self.datosparaGUI:
				texto = QTableWidgetItem(item)
				globalvar["listadetablas"]["tabla"+str(numpuerto)].setItem(fila,columna,texto)
				columna = columna + 1
			#Contamos la cantidad de columnas en la tabla
			if globalvar["listadetablas"]["tabla"+str(numpuerto)].rowCount() > 300:
				globalvar["listadetablas"]["tabla"+str(numpuerto)].removeRow(301)
			print self.dividida.groups()
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(self.dividida.groups())
		except Exception as exc:
			self.tramafail = trama + "Error al Tratar Protocolo, Chequea ErrorLOG"
			GuardarTramaObjeto.GuardarTXTFail(self.tramafail)
			GuardarTramaObjeto.GuardarErrores(str(exc))


SiaLevel1_2_SurGuardobjeto= SiaLevel1_2_SurGuard()

class Sia2_MLR2(object):
	def __init__(self):
		self.nombre = "Sia2 del SurGuard"
		self.nombreformato = "SIA"
		self.numprotocolo = '1'
		self.eregular = 'S(\d\d\d\d\d|\d\d\d\d|\d\d\d)\[#....|Nri\d\w\w(\d\d\d|\d\d)]'
	def tratar(self,trama,numpuerto,prefijo):
		#colaSIA2.append(trama)
		try:
			self.patron = re.compile('(?P<Identificador>[S])(?P<Receptor>\d\d)(?P<Linea>[0-9A-Z]{1,3})(?P<Separador>\[\#)(?P<Abonado>[0-9A-Za-z]{1,6})(?P<Separador2>\|)(?P<Separador3>Nr.)(?P<Particion>[0-9a-zA-Z]{1,3})(?P<Evento>\D\D)(?P<ZonaUsuario>[0-9a-zA-Z]{1,5})')
			self.dividida = self.patron.search(trama)
			#Para quitarle los 0 a la izq a la linea, solcuion temporal mientras se arregla la bd
			self.linea = int(self.dividida.group("Linea"))			
			#Agregando el prefijo al Abonado en caso de que lo tenga
			self.Abonado = str(self.dividida.group('Abonado'))
			if int(prefijo) >= 1000:
				self.Abonado = int(self.Abonado) + int(prefijo)

			self.datosparaGUI = (str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),self.dividida.group('Particion'),self.dividida.group('Linea'),self.nombreformato,LaFecha.damefecha())
			self.datosparaBD = (trama,str(self.linea),str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),self.numprotocolo,self.dividida.group('Particion'),numpuerto,'0')
			#Insertar En Base de Datos
			ColaParaGuardar.append(self.datosparaBD)
			fila = 0
			columna = 0
			globalvar["listadetablas"]["tabla"+str(numpuerto)].insertRow(0)
			for item in self.datosparaGUI:
				texto = QTableWidgetItem(item)
				globalvar["listadetablas"]["tabla"+str(numpuerto)].setItem(fila,columna,texto)
				columna = columna + 1
			#Contamos la cantidad de columnas en la tabla
			if globalvar["listadetablas"]["tabla"+str(numpuerto)].rowCount() > 300:
				globalvar["listadetablas"]["tabla"+str(numpuerto)].removeRow(301)
			print self.dividida.groups()
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(self.dividida.groups())
		except Exception as exc:
			self.tramafail = trama + "Error al Tratar Protocolo, Chequea ErrorLOG"
			GuardarTramaObjeto.GuardarTXTFail(self.tramafail)
			GuardarTramaObjeto.GuardarErrores(str(exc))


Sia2_MLR2objeto = Sia2_MLR2()

class Sia3_MLR2(object):
	def __init__(self):
		self.nombre = "Sia3 del SurGuard"
		self.nombreformato = "SIA"
		self.numprotocolo = '1'
		self.eregular = 'S(\d\d\d\d\d\d|\d\d\d\d\d|\d\d\d\d|\d\d\d)\[#(....|.....|......)\|\wri./(..\d\d\d|..\d\d)(]|/|)(.ri.|ri.|..\d\d\d|..\d\d||)(]|/|)(.ri.|ri.|..\d\d\d|..\d\d||)(]|/|)(.ri.|ri.|..\d\d\d|..\d\d||)(]|/|)(.ri.|ri.|..\d\d\d|..\d\d||)(]|/|)(.ri.|ri.|..\d\d\d|..\d\d||)(]|/|)(.ri.|ri.|..\d\d\d|..\d\d||)(]|/|)(.ri.|ri.|..\d\d\d|..\d\d||)(]|/|)(.ri.|ri.|..\d\d\d|..\d\d||)(]|/|)(.ri.|ri.|..\d\d\d|..\d\d||)(]|/|)(.ri.|ri.|..\d\d\d|..\d\d||)(]|/|)(.ri.|ri.|..\d\d\d|..\d\d||)(]|/|)(.ri.|ri.|..\d\d\d|..\d\d||)(]|/|)(.ri.|ri.|..\d\d\d|..\d\d||)(]|/|)(.ri.|ri.|..\d\d\d|..\d\d||)(]|/|)(.ri.|ri.|..\d\d\d|..\d\d||)(]|/|)(.ri.|ri.|..\d\d\d|..\d\d||)(]|/|)(.ri.|ri.|..\d\d\d|..\d\d||)(]|/|)(.ri.|ri.|..\d\d\d|..\d\d||)(]|/|)(.ri.|ri.|..\d\d\d|..\d\d||)(]|/|)(.ri.|ri.|..\d\d\d|..\d\d||)(]|/|)'
	def tratar(self,trama,numpuerto,prefijo):
		#colaSIA3.append(trama)
		try:
			if len(trama) >= 26:  #Deberia detectarla por varios / y no por el tamano
				#Como la Trama viene con muchos eventos, la pico en el primer Slash para Tener
				#El principio de la trama para todos los eventos
				tramadividida = trama.split("/",1)
				#Ahora pico todos los eventos por su Slash
				listadeeventos = tramadividida[1].split("/")
				#Definiendo la particion inicial de la trama para colocarla a los eventos
				#Al menos que mas adelante este una nueva particion
				patron = re.compile('(Nri(.|..))')
				particionactual = patron.search(tramadividida[0])
				particionactual = particionactual.group(0).replace('Nri','')
				listadetramas = []
				num = 0
				for i in listadeeventos:
					#Si entre los eventos hay un cambio de particion que venga ri y un numero
					if re.match("ri\d",i):
						#Guardamos el numero de particion quitandole el ri
						particionactual = i.replace('ri','')
						num = num + 1
					elif re.match("Or..",i):
						pass
					else:
						#Reemplazamos la particion de la trama por la particion Actual
						tramaparticionactual = re.sub('Nri\d','Nri'+particionactual, tramadividida[0])
						tr = tramaparticionactual + '/' + i.rstrip(']') + ']'
						listadetramas.append(tr)
						num = num + 1
						self.patron = re.compile('(?P<Identificador>[S])(?P<Receptor>\d\d)(?P<Linea>[0-9]{1,3})(?P<Separador>\[\#)(?P<Abonado>[0-9a-zA-Z]{1,6})(?P<Separador2>\|)(?P<Separador3>Nr.)(?P<Particion>[0-9a-zA-Z]{1,3})(?P<Separador4>/)(?P<Evento>\D\D)(?P<ZonaUsuario>[0-9a-zA-Z]{1,5})')
						self.dividida = self.patron.search(tr)
						#Para quitarle los 0 a la izq a la linea, solcuion temporal mientras se arregla la bd
						self.linea = int(self.dividida.group("Linea"))
						#Agregando el prefijo al Abonado en caso de que lo tenga
						self.Abonado = str(self.dividida.group('Abonado'))
						if int(prefijo) >= 1000:
							self.Abonado = int(self.Abonado) + int(prefijo)
						
						self.datosparaGUI = (str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),self.dividida.group('Particion'),self.dividida.group('Linea'),self.nombreformato,LaFecha.damefecha())
						self.datosparaBD = (trama,str(self.linea),str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),self.numprotocolo,self.dividida.group('Particion'),numpuerto,'0')


						#Insertar En Base de Datos
						ColaParaGuardar.append(self.datosparaBD)
						fila = 0
						columna = 0
						globalvar["listadetablas"]["tabla"+str(numpuerto)].insertRow(0)
						for item in self.datosparaGUI:
							texto = QTableWidgetItem(item)
							globalvar["listadetablas"]["tabla"+str(numpuerto)].setItem(fila,columna,texto)
							columna = columna + 1
						#Contamos la cantidad de columnas en la tabla
						if globalvar["listadetablas"]["tabla"+str(numpuerto)].rowCount() > 300:
							globalvar["listadetablas"]["tabla"+str(numpuerto)].removeRow(301)
						print self.dividida.groups()
						#Guardar en el Log
						GuardarTramaObjeto.GuardarTXTLog(self.dividida.groups())
				#print listadetramas
			#Si es una trama que trae un solo evento entonces
			else:
				self.patron = re.compile('(?P<Identificador>[S])(?P<Receptor>\d\d)(?P<Linea>[0-9]{1,3})(?P<Separador>\[\#)(?P<Abonado>[0-9A-Za-z]{1,6})(?P<Separador2>\|)(?P<Separador3>Nr.)(?P<Particion>[0-9A-Za-z]{1,3})(?P<Separador4>/)(?P<Evento>\D\D)(?P<ZonaUsuario>[0-9A-Za-z]{1,5})')
				self.dividida = self.patron.search(trama)
				#Para quitarle los 0 a la izq a la linea, solcuion temporal mientras se arregla la bd
				self.linea = int(self.dividida.group("Linea"))
				#Agregando el prefijo al Abonado en caso de que lo tenga
				self.Abonado = str(self.dividida.group('Abonado'))
				if int(prefijo) >= 1000:
					self.Abonado = int(self.Abonado) + int(prefijo)

				self.datosparaGUI = (str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),self.dividida.group('Particion'),self.dividida.group('Linea'),self.nombreformato,LaFecha.damefecha())
				self.datosparaBD = (trama,str(self.linea),str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),self.numprotocolo,self.dividida.group('Particion'),numpuerto,'0')
				#Insertar En Base de Datos
				ColaParaGuardar.append(self.datosparaBD)
				fila = 0
				columna = 0
				globalvar["listadetablas"]["tabla"+str(numpuerto)].insertRow(0)
				for item in self.datosparaGUI:
					texto = QTableWidgetItem(item)
					globalvar["listadetablas"]["tabla"+str(numpuerto)].setItem(fila,columna,texto)
					columna = columna + 1
				#Contamos la cantidad de columnas en la tabla
				if globalvar["listadetablas"]["tabla"+str(numpuerto)].rowCount() > 300:
					globalvar["listadetablas"]["tabla"+str(numpuerto)].removeRow(301)
				print self.dividida.groups()
				#Guardar en el Log
				GuardarTramaObjeto.GuardarTXTLog(self.dividida.groups())
		except Exception as exc:
			self.tramafail = trama + "Error al Tratar Protocolo, Chequea ErrorLOG"
			GuardarTramaObjeto.GuardarTXTFail(self.tramafail)
			GuardarTramaObjeto.GuardarErrores(str(exc))

Sia3_MLR2objeto = Sia3_MLR2()

class CuatromasDos_MLR2(object):
	def __init__(self):
		self.nombre = '4+2 SurGuard'
		self.nombreformato = "4+2"
		self.numprotocolo = '3'
		self.eregular = '1\d\d\d(|\d\d)      .... .  ..'
	def tratar(self,trama,numpuerto,prefijo):
		try:
			self.patron = re.compile('(?P<Identificador>[1])(?P<Receptor>\d\d)(?P<Linea>[0-9]{1,3})(?P<Separador>      )(?P<Abonado>....)(?P<Separador2> )(?P<NADA>.)(?P<Separador3>  )(?P<Evento>..)')
			self.dividida = self.patron.search(trama)
			#Para quitarle los 0 a la izq a la linea, solcuion temporal mientras se arregla la bd
			self.linea = int(self.dividida.group("Linea"))				
			#Agregando el prefijo al Abonado en caso de que lo tenga
			self.Abonado = str(self.dividida.group('Abonado'))
			if int(prefijo) >= 1000:
				self.Abonado = int(self.Abonado) + int(prefijo)

			self.datosparaGUI = (str(self.Abonado),self.dividida.group('Evento'),'No Aplica','No Aplica',self.dividida.group('Linea'),self.nombreformato,LaFecha.damefecha())
			self.datosparaBD = (trama,str(self.linea),str(self.Abonado),self.dividida.group('Evento'),'0',self.numprotocolo,'1',numpuerto,'0')
			#Insertar En Base de Datos
			ColaParaGuardar.append(self.datosparaBD)
			fila = 0
			columna = 0
			globalvar["listadetablas"]["tabla"+str(numpuerto)].insertRow(0)
			for item in self.datosparaGUI:
				texto = QTableWidgetItem(item)
				globalvar["listadetablas"]["tabla"+str(numpuerto)].setItem(fila,columna,texto)
				columna = columna + 1
			#Contamos la cantidad de columnas en la tabla
			if globalvar["listadetablas"]["tabla"+str(numpuerto)].rowCount() > 300:
				globalvar["listadetablas"]["tabla"+str(numpuerto)].removeRow(301)
			print self.dividida.groups()
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(self.dividida.groups())
		except Exception as exc:
			self.tramafail = trama + "Error al Tratar Protocolo, Chequea ErrorLOG"
			GuardarTramaObjeto.GuardarTXTFail(self.tramafail)
			GuardarTramaObjeto.GuardarErrores(str(exc))
		
CuatromasDos_MLR2objeto = CuatromasDos_MLR2()

#Formatos de AES

class ContactID_AES(object):
	def __init__(self):
		self.nombre = "ContactID del AES Intellinet"
		self.nombreformato = "CID"
		self.numprotocolo = '2'
		self.eregular = '1\d \d\d\d\d 18 \D... .. ....'
	def tratar(self,trama,numpuerto,prefijo):
		#colaCIDMLR2.append(trama)
		try:
			self.patron = re.compile('(?P<Identificador>1)(?P<Linea>[0-9])(?P<Espacio> )(?P<Abonado>....)(?P<Espacio2> )(?P<ID>18)(?P<Espacio3> )(?P<Evento>\D...)(?P<Espacio4> )(?P<Particion>\d\d)(?P<Espacio5> )(?P<Nada>.)(?P<ZonaUsuario>\d{2,})')
			self.dividida = self.patron.search(trama)
			
			#Agregando el prefijo al Abonado en caso de que lo tenga
			self.Abonado = str(self.dividida.group('Abonado'))
			if int(prefijo) >= 1000:
				self.Abonado = int(self.Abonado) + int(prefijo)

			self.datosparaGUI = (str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),self.dividida.group('Particion'),self.dividida.group('Linea'),self.nombreformato,LaFecha.damefecha())
			self.datosparaBD = (trama,self.dividida.group('Linea'),str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),self.numprotocolo,self.dividida.group('Particion'),numpuerto,'0')
			#Insertar En Base de Datos
			ColaParaGuardar.append(self.datosparaBD)
			fila = 0
			columna = 0
			globalvar["listadetablas"]["tabla"+str(numpuerto)].insertRow(0)
			for item in self.datosparaGUI:
				texto = QTableWidgetItem(item)
				globalvar["listadetablas"]["tabla"+str(numpuerto)].setItem(fila,columna,texto)
				columna = columna + 1
			#Contamos la cantidad de columnas en la tabla
			if globalvar["listadetablas"]["tabla"+str(numpuerto)].rowCount() > 300:
				globalvar["listadetablas"]["tabla"+str(numpuerto)].removeRow(301)
			print self.dividida.groups()
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(self.dividida.groups())
		except Exception as exc:
			self.tramafail = trama + "Error al Tratar Protocolo, Chequea ErrorLOG"
			GuardarTramaObjeto.GuardarTXTFail(self.tramafail)
			GuardarTramaObjeto.GuardarErrores(str(exc))

ContactID_AESobjeto= ContactID_AES()

#Formatos de DMP

class ContactID_DMP(object):
	def __init__(self):
		self.nombre = "ContactID del DMP"
		self.nombreformato = "CID"
		self.numprotocolo = '2'
		self.eregular = '1(\d\d|\d|-) (.....|....|...|..) c(.....|....|...|..) 18 . ... .. ... .'
	def tratar(self,trama,numpuerto,prefijo):
		#colaCIDMLR2.append(trama)
		try:
			self.patron = re.compile('(?P<Identificador>1)(?P<NumTarjeta>\d|\-)(?P<Linea>\d|)(?P<Espacio> )(?P<Abonado>[0-9a-z]{1,5})(?P<Espacio2> )(?P<Nada>c)(?P<Espacio3> )(?P<AbonadoCID>[0-9a-z]{1,5})(?P<Espacio4> )(?P<Identificadorcid>18)(?P<Espacio5> )(?P<Calificador>.)(?P<Espacio6> )(?P<Evento>...)(?P<Espacio7> )(?P<Particion>..)(?P<Espacio8> )(?P<ZonaUsuario>...)(?P<Espacio9> )(?P<CheckSum>.)')
			self.dividida = self.patron.search(trama)
			
			#Agregando el prefijo al Abonado en caso de que lo tenga
			self.Abonado = str(self.dividida.group('Abonado'))
			if int(prefijo) >= 1000:
				self.Abonado = int(self.Abonado) + int(prefijo)

			#Arreglando la Linea
			self.Linea = str(self.dividida.group('Linea'))
			if self.Linea == '':
				self.Linea = '1'

			#Uniendo el Calificador con el Evento
			self.Evento = str(self.dividida.group('Calificador'))+str(self.dividida.group('Evento'))

			self.datosparaGUI = (str(self.Abonado),self.Evento,self.dividida.group('ZonaUsuario'),self.dividida.group('Particion'),self.Linea,self.nombreformato,LaFecha.damefecha())
			self.datosparaBD = (trama,self.Linea,str(self.Abonado),self.Evento,self.dividida.group('ZonaUsuario'),self.numprotocolo,self.dividida.group('Particion'),numpuerto,'0')
			#Insertar En Base de Datos
			ColaParaGuardar.append(self.datosparaBD)
			fila = 0
			columna = 0
			globalvar["listadetablas"]["tabla"+str(numpuerto)].insertRow(0)
			for item in self.datosparaGUI:
				texto = QTableWidgetItem(item)
				globalvar["listadetablas"]["tabla"+str(numpuerto)].setItem(fila,columna,texto)
				columna = columna + 1
			#Contamos la cantidad de columnas en la tabla
			if globalvar["listadetablas"]["tabla"+str(numpuerto)].rowCount() > 300:
				globalvar["listadetablas"]["tabla"+str(numpuerto)].removeRow(301)
			print self.dividida.groups()
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(self.dividida.groups())
		except Exception as exc:
			self.tramafail = trama + "Error al Tratar Protocolo, Chequea ErrorLOG"
			GuardarTramaObjeto.GuardarTXTFail(self.tramafail)
			GuardarTramaObjeto.GuardarErrores(str(exc))

ContactID_DMPobjeto = ContactID_DMP()

class DD_DMP(object):
	def __init__(self):
		self.nombre = "Digital Dialer del DMP" 
		self.nombreformato = "DD"
		self.numprotocolo = '11'
		self.eregular = '1(\d\d|\d|-) (.....|....|...|..) Z.......+'
	def tratar(self,trama,numpuerto,prefijo):
		#Necesario por problemas del lenguaje con el backslash
		trama = trama.replace('\\','/')
		try:
			self.patron = re.compile('(?P<Identificador>1)(?P<NumTarjeta>\d|\-)(?P<Linea>\d|)(?P<Espacio>    |   |  | )(?P<Abonado>[0-9a-z]{1,5})(?P<Espacio2> )(?P<GrupoEvento>Z.)(?P<LargoTrama>/.../)(?P<TipoSubMensaje>..)(?P<Evento>.\w\w|\d\d\d|\d\d)(?P<Seprador>/)(?P<Zona>z.[0-9]{1,5}|)(?P<NombreZona>"[0-9A-Z- ]{1,32}|)(?P<Seprador2>/|)(?P<Usuario>u.[0-9]{1,5}|)(?P<NombreUsuario>"[0-9A-Z- ]{1,32}|)(?P<Seprador3>/|)(?P<Area>a.[0-9]{1,5}|)(?P<NombreArea>"[0-9A-Z- ]{1,32}|)')
			self.dividida = self.patron.search(trama)
			#Arreglando la Linea
			self.Linea = str(self.dividida.group('Linea'))
			if self.Linea.isdigit():
				self.Linea = int(self.Linea)
			else:
				self.Linea = 1
			#Agregando el prefijo al Abonado en caso de que lo tenga
			self.Abonado = str(self.dividida.group('Abonado'))
			if int(prefijo) >= 1000:
				self.Abonado = int(self.Abonado) + int(prefijo)
			#Acomodo el Evento uniendo el Evento con el Grupo de Evento
			self.Evento = str(self.dividida.group('Evento'))
			if self.Evento.isdigit():
				self.Evento = str(self.Evento)+str(self.dividida.group('GrupoEvento'))
			else:
				self.Evento = str(self.Evento).replace('"','')+str(self.dividida.group('GrupoEvento'))
			#Acomodo la Zona quitandole la Z
			self.Zona = str(self.dividida.group('Zona')).strip()
			self.Zona = self.Zona[2:]
			#Acomodando el Usuario quitandole la U
			self.Usuario = str(self.dividida.group('Usuario')).strip()
			self.Usuario = self.Usuario[2:]
			#Acomodando el Area quitandole la A
			self.Area = str(self.dividida.group('Area')).strip()
			self.Area = self.Area[2:]
			#Si no hay particion se le coloca particion 0
			if self.Area == '':
				self.Area = '0'
			#Verificamos si es una senal de Zona o de Usuario
			self.ZonaUsuario = ''
			if self.Usuario == '':
				self.ZonaUsuario = self.Zona
			else:
				self.ZonaUsuario = self.Usuario
			#Si la Zona o el Usuario no existen es 0
			if self.ZonaUsuario == '':
				self.ZonaUsuario = '0'
			self.datosparaGUI = (str(self.Abonado),self.Evento,str(self.ZonaUsuario),str(self.Area),str(self.Linea),self.nombreformato,LaFecha.damefecha())
			self.datosparaBD = (trama,str(self.Linea),str(self.Abonado),self.Evento,str(self.ZonaUsuario),self.numprotocolo,str(self.Area),numpuerto,'0')
			#Insertar En Base de Datos
			ColaParaGuardar.append(self.datosparaBD)
			fila = 0
			columna = 0
			globalvar["listadetablas"]["tabla"+str(numpuerto)].insertRow(0)
			for item in self.datosparaGUI:
				texto = QTableWidgetItem(item)
				globalvar["listadetablas"]["tabla"+str(numpuerto)].setItem(fila,columna,texto)
				columna = columna + 1
			#Contamos la cantidad de columnas en la tabla
			if globalvar["listadetablas"]["tabla"+str(numpuerto)].rowCount() > 300:
				globalvar["listadetablas"]["tabla"+str(numpuerto)].removeRow(301)
			print self.dividida.groups()
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(self.dividida.groups())
		except Exception as exc:
			self.tramafail = trama + "Error al Tratar Protocolo, Chequea ErrorLOG"
			GuardarTramaObjeto.GuardarTXTFail(self.tramafail)
			GuardarTramaObjeto.GuardarErrores(str(exc))

DD_DMPobjeto = DD_DMP()


#Formatos del Sentinel

class ContactID_Sentinel(object):
	def __init__(self):
		self.nombre = "ContactID del Sentinel" 
		self.nombreformato = "CID"
		self.numprotocolo = '2'
		self.eregular = '5... 18....\w...  ...'
	def tratar(self,trama,numpuerto,prefijo):
		#colaCIDMLR2.append(trama)
		try:
			self.patron = re.compile('(?P<Identificador>5)(?P<Receptor>\d\d)(?P<Linea>[0-9a-zA-Z]{1,3})(?P<Espacio> )(?P<ID>18)(?P<Abonado>....)(?P<Evento>\D\d\d\d)(?P<Espacio2>  )(?P<ZonaUsuario>\d{2,})')
			self.dividida = self.patron.search(trama)
			#Para quitarle los 0 a la izq a la linea, solcuion temporal mientras se arregla la bd
			self.linea = int(self.dividida.group("Linea"))
			#Agregando el prefijo al Abonado en caso de que lo tenga
			self.Abonado = str(self.dividida.group('Abonado'))
			if int(prefijo) >= 1000:
				self.Abonado = int(self.Abonado) + int(prefijo)
			self.datosparaGUI = (str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),"No Aplica",self.dividida.group('Linea'),self.nombreformato,LaFecha.damefecha())
			self.datosparaBD = (trama,str(self.linea),str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),self.numprotocolo,"1",numpuerto,'0')
			ColaParaGuardar.append(self.datosparaBD)
			#Variables para Insertar
			fila = 0
			columna = 0
			globalvar["listadetablas"]["tabla"+str(numpuerto)].insertRow(0)
			for item in self.datosparaGUI:
				texto = QTableWidgetItem(item)
				globalvar["listadetablas"]["tabla"+str(numpuerto)].setItem(fila,columna,texto)
				columna = columna + 1
			#Contamos la cantidad de columnas en la tabla
			if globalvar["listadetablas"]["tabla"+str(numpuerto)].rowCount() > 300:
				globalvar["listadetablas"]["tabla"+str(numpuerto)].removeRow(301)
			print self.dividida.groups()
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(self.dividida.groups())
		except Exception as exc:
			self.tramafail = trama + "Error al Tratar Protocolo, Chequea ErrorLOG"
			GuardarTramaObjeto.GuardarTXTFail(self.tramafail)
			GuardarTramaObjeto.GuardarErrores(str(exc))
ContactID_Sentinelobjeto = ContactID_Sentinel()

class Sia_Sentinel(object):
	def __init__(self):
		self.nombre = 'Sia Sentinel Emulando SurGuard'
		self.nombreformato = "SIA"
		self.numprotocolo = '1'
		self.eregular = '\d\d\d\d      \d\d\d\d\S\S \d\d\d'
	def tratar(self,trama,numpuerto,prefijo):
		try:
			self.patron = re.compile('(?P<Identificador>\d)(?P<Receptor>\d\d)(?P<Linea>\d)(?P<Separador>      )(?P<Abonado>....)(?P<Evento>..)(?P<Separador2> )(?P<ZonaUsuario>...)')
			self.dividida = self.patron.search(trama)
			#Agregando el prefijo al Abonado en caso de que lo tenga
			self.Abonado = str(self.dividida.group('Abonado'))
			if int(prefijo) >= 1000:
				self.Abonado = int(self.Abonado) + int(prefijo)
			self.datosparaGUI = (str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),'No Aplica',self.dividida.group('Linea'),self.nombreformato,LaFecha.damefecha())
			self.datosparaBD = (trama,self.dividida.group('Linea'),str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),self.numprotocolo,'1',numpuerto,'0')
			#Insertar En Base de Datos
			ColaParaGuardar.append(self.datosparaBD)
			fila = 0
			columna = 0
			globalvar["listadetablas"]["tabla"+str(numpuerto)].insertRow(0)
			for item in self.datosparaGUI:
				texto = QTableWidgetItem(item)
				globalvar["listadetablas"]["tabla"+str(numpuerto)].setItem(fila,columna,texto)
				columna = columna + 1
			#Contamos la cantidad de columnas en la tabla
			if globalvar["listadetablas"]["tabla"+str(numpuerto)].rowCount() > 300:
				globalvar["listadetablas"]["tabla"+str(numpuerto)].removeRow(301)
			print self.dividida.groups()
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(self.dividida.groups())
		except Exception as exc:
			self.tramafail = trama + "Error al Tratar Protocolo, Chequea ErrorLOG"
			GuardarTramaObjeto.GuardarTXTFail(self.tramafail)
			GuardarTramaObjeto.GuardarErrores(str(exc))

Sia_Sentinelobjeto= Sia_Sentinel()

class NewPaf_Sentinel1(object):
	def __init__(self):
		self.nombre = 'NewPaf Sentinel Emulando SurGuard'
		self.nombreformato = "NewPaf"
		self.numprotocolo = '4'
		self.eregular = '\d\d\d\d      \d\d\d\d    ..'
	def tratar(self,trama,numpuerto,prefijo):
		try:
			self.patron = re.compile('(?P<Identificador>\d)(?P<Receptor>\d\d)(?P<Linea>\d)(?P<Separador>      )(?P<Abonado>....)(?P<Separador2>    )(?P<Evento>..)')
			self.dividida = self.patron.search(trama)
			#Agregando el prefijo al Abonado en caso de que lo tenga
			self.Abonado = str(self.dividida.group('Abonado'))
			if int(prefijo) >= 1000:
				self.Abonado = int(self.Abonado) + int(prefijo)
			self.datosparaGUI = (str(self.Abonado),self.dividida.group('Evento'),'No Aplica','No Aplica',self.dividida.group('Linea'),self.nombreformato,LaFecha.damefecha())
			self.datosparaBD = (trama,self.dividida.group('Linea'),str(self.Abonado),self.dividida.group('Evento'),'0',self.numprotocolo,'1',numpuerto,'0')
			#Insertar En Base de Datos
			ColaParaGuardar.append(self.datosparaBD)
			fila = 0
			columna = 0
			globalvar["listadetablas"]["tabla"+str(numpuerto)].insertRow(0)
			for item in self.datosparaGUI:
				texto = QTableWidgetItem(item)
				globalvar["listadetablas"]["tabla"+str(numpuerto)].setItem(fila,columna,texto)
				columna = columna + 1
			#Contamos la cantidad de columnas en la tabla
			if globalvar["listadetablas"]["tabla"+str(numpuerto)].rowCount() > 300:
				globalvar["listadetablas"]["tabla"+str(numpuerto)].removeRow(301)
			print self.dividida.groups()
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(self.dividida.groups())
		except Exception as exc:
			self.tramafail = trama + "Error al Tratar Protocolo, Chequea ErrorLOG"
			GuardarTramaObjeto.GuardarTXTFail(self.tramafail)
			GuardarTramaObjeto.GuardarErrores(str(exc))

NewPaf_Sentinel1objeto= NewPaf_Sentinel1()

class NewPaf_Sentinel2(object):
	def __init__(self):
		self.nombre = 'NewPaf Pima'
		self.nombreformato = "NewPaf"
		self.numprotocolo = '4'
		self.eregular = '\d\d\d\d\d----..'
	def tratar(self,trama,numpuerto,prefijo):
		try:
			self.patron = re.compile('(?P<Linea>\d)(?P<Abonado>....)(?P<Separadores>----)(?P<Evento>..)')
			self.dividida = self.patron.search(trama)
			#Agregando el prefijo al Abonado en caso de que lo tenga
			self.Abonado = str(self.dividida.group('Abonado'))
			if int(prefijo) >= 1000:
				self.Abonado = int(self.Abonado) + int(prefijo)
			self.datosparaGUI = (str(self.Abonado),self.dividida.group('Evento'),'No Aplica','No Aplica',self.dividida.group('Linea'),self.nombreformato,LaFecha.damefecha())
			self.datosparaBD = (trama,self.dividida.group('Linea'),str(self.Abonado),self.dividida.group('Evento'),'0',self.numprotocolo,'1',numpuerto,'0')
			#Insertar En Base de Datos
			ColaParaGuardar.append(self.datosparaBD)
			fila = 0
			columna = 0
			globalvar["listadetablas"]["tabla"+str(numpuerto)].insertRow(0)
			for item in self.datosparaGUI:
				texto = QTableWidgetItem(item)
				globalvar["listadetablas"]["tabla"+str(numpuerto)].setItem(fila,columna,texto)
				columna = columna + 1
			#Contamos la cantidad de columnas en la tabla
			if globalvar["listadetablas"]["tabla"+str(numpuerto)].rowCount() > 300:
				globalvar["listadetablas"]["tabla"+str(numpuerto)].removeRow(301)
			print self.dividida.groups()
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(self.dividida.groups())
		except Exception as exc:
			self.tramafail = trama + "Error al Tratar Protocolo, Chequea ErrorLOG"
			GuardarTramaObjeto.GuardarTXTFail(self.tramafail)
			GuardarTramaObjeto.GuardarErrores(str(exc))

NewPaf_Sentinel2objeto= NewPaf_Sentinel2()

#Formato SEABOARD M1A - M1AL

class SeaBoard_M1A(object):
	def __init__(self):
		self.nombre = "SeaBoard del M1A - M1AL"
		self.nombreformato = "M1A"
		self.numprotocolo = '8'
		self.eregular = '\d.....'
	def tratar(self,trama,numpuerto,prefijo):
		#colaCIDMLR2.append(trama)
		try:
			self.patron = re.compile('(?P<Abonado>....)(?P<Evento>..)')
			self.dividida = self.patron.search(trama)
			#Agregando el prefijo al Abonado en caso de que lo tenga
			self.Abonado = str(self.dividida.group('Abonado'))
			if int(prefijo) >= 1000:
				self.Abonado = int(self.Abonado) + int(prefijo)
			self.datosparaGUI = (str(self.Abonado),self.dividida.group('Evento'),'No Aplica','No Aplica','No Aplica',self.nombreformato,LaFecha.damefecha())
			self.datosparaBD = (trama,'1',str(self.Abonado),self.dividida.group('Evento'),"0",self.numprotocolo,"1",numpuerto,'0')
			#Insertar En Base de Datos
			ColaParaGuardar.append(self.datosparaBD)
			fila = 0
			columna = 0
			globalvar["listadetablas"]["tabla"+str(numpuerto)].insertRow(0)
			for item in self.datosparaGUI:
				texto = QTableWidgetItem(item)
				globalvar["listadetablas"]["tabla"+str(numpuerto)].setItem(fila,columna,texto)
				columna = columna + 1
			#Contamos la cantidad de columnas en la tabla
			if globalvar["listadetablas"]["tabla"+str(numpuerto)].rowCount() > 300:
				globalvar["listadetablas"]["tabla"+str(numpuerto)].removeRow(301)
			print self.dividida.groups()
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(self.dividida.groups())
		except Exception as exc:
			self.tramafail = trama + "Error al Tratar Protocolo, Chequea ErrorLOG"
			GuardarTramaObjeto.GuardarTXTFail(self.tramafail)
			GuardarTramaObjeto.GuardarErrores(str(exc))

SeaBoard_M1Aobjeto= SeaBoard_M1A()

class SeaBoard_M1AHEX(object):
	def __init__(self):
		self.nombre = "SeaBoard del M1A - M1AL HEX"
		self.nombreformato = "M1AHEX"
		self.numprotocolo = '9'
		self.eregular = '\d.....'
	def tratar(self,trama,numpuerto,prefijo):
		#colaCIDMLR2.append(trama)
		try:
			#Convertimos el Abonado de Hexadecimal a Decimal
			#Para eso tomo del digito 2 al 4 de la trama que son la parte HEX
			#del abonado porque el primer digito viene normal
			AbonadoenHex = str(trama[1:4])
			AbonadoenDec = int(AbonadoenHex,16)
			#Reemplazo en la trama el la parte HEX por la DEC que acabo de 
			#Convertir
			trama = trama.replace(AbonadoenHex,str(AbonadoenDec))
			self.patron = re.compile('(?P<Abonado>....)(?P<Evento>..)')
			self.dividida = self.patron.search(trama)
			#Agregando el prefijo al Abonado en caso de que lo tenga
			self.Abonado = str(self.dividida.group('Abonado'))
			if int(prefijo) >= 1000:
				self.Abonado = int(self.Abonado) + int(prefijo)
			self.datosparaGUI = (str(self.Abonado),self.dividida.group('Evento'),'No Aplica','No Aplica','No Aplica',self.nombreformato,LaFecha.damefecha())
			self.datosparaBD = (trama,'1',str(self.Abonado),self.dividida.group('Evento'),"0",self.numprotocolo,"1",numpuerto,'0')
			#Insertar En Base de Datos
			ColaParaGuardar.append(self.datosparaBD)
			fila = 0
			columna = 0
			globalvar["listadetablas"]["tabla"+str(numpuerto)].insertRow(0)
			for item in self.datosparaGUI:
				texto = QTableWidgetItem(item)
				globalvar["listadetablas"]["tabla"+str(numpuerto)].setItem(fila,columna,texto)
				columna = columna + 1
			#Contamos la cantidad de columnas en la tabla
			if globalvar["listadetablas"]["tabla"+str(numpuerto)].rowCount() > 300:
				globalvar["listadetablas"]["tabla"+str(numpuerto)].removeRow(301)
			print self.dividida.groups()
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(self.dividida.groups())
		except Exception as exc:
			self.tramafail = trama + "Error al Tratar Protocolo, Chequea ErrorLOG"
			GuardarTramaObjeto.GuardarTXTFail(self.tramafail)
			GuardarTramaObjeto.GuardarErrores(str(exc))

SeaBoard_M1AHEXobjeto= SeaBoard_M1AHEX()

#Formatos del VisorALARM

class ContactID1_VisorAlarm(object):
	def __init__(self):
		self.nombre = "ContactID del VisorALARM emulando ADEMCO685"
		self.nombreformato = "CID"
		self.numprotocolo = '2'
		self.eregular = '1\d \d\d\d\d 18 \D... .. ....'
	def tratar(self,trama,numpuerto,prefijo):
		#colaCIDMLR2.append(trama)
		try:
			self.patron = re.compile('(?P<Identificador>1)(?P<Linea>[0-9])(?P<Espacio> )(?P<Abonado>....)(?P<Espacio2> )(?P<ID>18)(?P<Espacio3> )(?P<Evento>\D...)(?P<Espacio4> )(?P<Particion>\d\d)(?P<Espacio5> )(?P<Nada>.)(?P<ZonaUsuario>\d{2,})')
			self.dividida = self.patron.search(trama)
			#Agregando el prefijo al Abonado en caso de que lo tenga
			self.Abonado = str(self.dividida.group('Abonado'))
			if int(prefijo) >= 1000:
				self.Abonado = int(self.Abonado) + int(prefijo)
			self.datosparaGUI = (str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),self.dividida.group('Particion'),self.dividida.group('Linea'),self.nombreformato,LaFecha.damefecha())
			self.datosparaBD = (trama,self.dividida.group('Linea'),str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),self.numprotocolo,self.dividida.group('Particion'),numpuerto,'0')
			#Insertar En Base de Datos
			ColaParaGuardar.append(self.datosparaBD)
			fila = 0
			columna = 0
			globalvar["listadetablas"]["tabla"+str(numpuerto)].insertRow(0)
			for item in self.datosparaGUI:
				texto = QTableWidgetItem(item)
				globalvar["listadetablas"]["tabla"+str(numpuerto)].setItem(fila,columna,texto)
				columna = columna + 1
			#Contamos la cantidad de columnas en la tabla
			if globalvar["listadetablas"]["tabla"+str(numpuerto)].rowCount() > 300:
				globalvar["listadetablas"]["tabla"+str(numpuerto)].removeRow(301)
			print self.dividida.groups()
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(self.dividida.groups())
		except Exception as exc:
			self.tramafail = trama + "Error al Tratar Protocolo, Chequea ErrorLOG"
			GuardarTramaObjeto.GuardarTXTFail(self.tramafail)
			GuardarTramaObjeto.GuardarErrores(str(exc))

ContactID1_VisorAlarmobjeto= ContactID1_VisorAlarm()

class ContactID2_VisorAlarm(object):
	def __init__(self):
		self.nombre = "ContactID del VisorALARM emulando SurGuard" 
		self.nombreformato = "CID"
		self.numprotocolo = '2'
		self.eregular = '(5|Q)(....|...|.....) (18|58)(.................|............)(\d\d|\d)'
	def tratar(self,trama,numpuerto,prefijo):
		#colaCIDMLR2.append(trama)
		try:
			self.patron = re.compile('(?P<Identificador>[5])(?P<Receptor>\d\d)(?P<Linea>[0-9a-zA-Z]{1,3})(?P<Espacio> )(?P<ID>18)(?P<Abonado>....)(?P<Evento>\D\d\d\d)(?P<Particion>\d\d)(?P<ZonaUsuario>\d{2,})')
			self.dividida = self.patron.search(trama)
			#Agregando el prefijo al Abonado en caso de que lo tenga
			self.Abonado = str(self.dividida.group('Abonado'))
			if int(prefijo) >= 1000:
				self.Abonado = int(self.Abonado) + int(prefijo)

			self.datosparaGUI = (str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),self.dividida.group('Particion'),self.dividida.group('Linea'),self.nombreformato,LaFecha.damefecha())
			self.datosparaBD = (trama,self.dividida.group('Linea'),str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),self.numprotocolo,self.dividida.group('Particion'),numpuerto,'0')
			ColaParaGuardar.append(self.datosparaBD)
			#Variables para Insertar
			fila = 0
			columna = 0
			globalvar["listadetablas"]["tabla"+str(numpuerto)].insertRow(0)
			for item in self.datosparaGUI:
				texto = QTableWidgetItem(item)
				globalvar["listadetablas"]["tabla"+str(numpuerto)].setItem(fila,columna,texto)
				columna = columna + 1
			#Contamos la cantidad de columnas en la tabla
			if globalvar["listadetablas"]["tabla"+str(numpuerto)].rowCount() > 300:
				globalvar["listadetablas"]["tabla"+str(numpuerto)].removeRow(301)
			print self.dividida.groups()
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(self.dividida.groups())
		except Exception as exc:
			self.tramafail = trama + "Error al Tratar Protocolo, Chequea ErrorLOG"
			GuardarTramaObjeto.GuardarTXTFail(self.tramafail)
			GuardarTramaObjeto.GuardarErrores(str(exc))

ContactID2_VisorAlarmobjeto = ContactID2_VisorAlarm()

class ContactID3_VisorAlarm(object):
	def __init__(self):
		self.nombre = "ContactID del VisorALARM emulando RADIONICS"
		self.nombreformato = "CID"
		self.numprotocolo = '2'
		self.eregular = 'a... ....18.........'
	def tratar(self,trama,numpuerto,prefijo):
		#colaCIDMLR2.append(trama)
		try:
			self.patron = re.compile('(?P<Identificador>[a])(?P<Receptor>\d\d)(?P<Linea>\d)(?P<Espacio> )(?P<Abonado>....)(?P<ID>18)(?P<Evento>\D\d\d\d)(?P<Particion>\d\d)(?P<ZonaUsuario>\d{2,})')
			self.dividida = self.patron.search(trama)
			#Agregando el prefijo al Abonado en caso de que lo tenga
			self.Abonado = str(self.dividida.group('Abonado'))
			if int(prefijo) >= 1000:
				self.Abonado = int(self.Abonado) + int(prefijo)
			self.datosparaGUI = (str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),self.dividida.group('Particion'),self.dividida.group('Linea'),self.nombreformato,LaFecha.damefecha())
			self.datosparaBD = (trama,self.dividida.group('Linea'),str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),self.numprotocolo,self.dividida.group('Particion'),numpuerto,'0')
			#Insertar En Base de Datos
			ColaParaGuardar.append(self.datosparaBD)
			fila = 0
			columna = 0
			globalvar["listadetablas"]["tabla"+str(numpuerto)].insertRow(0)
			for item in self.datosparaGUI:
				texto = QTableWidgetItem(item)
				globalvar["listadetablas"]["tabla"+str(numpuerto)].setItem(fila,columna,texto)
				columna = columna + 1
			#Contamos la cantidad de columnas en la tabla
			if globalvar["listadetablas"]["tabla"+str(numpuerto)].rowCount() > 300:
				globalvar["listadetablas"]["tabla"+str(numpuerto)].removeRow(301)
			print self.dividida.groups()
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(self.dividida.groups())
		except Exception as exc:
			self.tramafail = trama + "Error al Tratar Protocolo, Chequea ErrorLOG"
			GuardarTramaObjeto.GuardarTXTFail(self.tramafail)
			GuardarTramaObjeto.GuardarErrores(str(exc))

ContactID3_VisorAlarmobjeto= ContactID3_VisorAlarm()

#Formatos del MCDI

class CuatromasDos_MCDI(object):
	def __init__(self):
		self.nombre = '4+2 MCDI'
		self.nombreformato = "4+2"
		self.numprotocolo = '3'
		self.eregular = '\d\d:\d\d  \d\d/\d\d\[/\d\d\]  .. .... ..'
	def tratar(self,trama,numpuerto,prefijo):
		try:
			self.patron = re.compile('(?P<Fecha>\d\d:\d\d  \d\d/\d\d\[/\d\d\]  )(?P<Receptor>.)(?P<Linea>.)(?P<Separador> )(?P<Abonado>....)(?P<Nada> )(?P<Evento>..)')
			self.dividida = self.patron.search(trama)
			#Agregando el prefijo al Abonado en caso de que lo tenga
			self.Abonado = str(self.dividida.group('Abonado'))
			if int(prefijo) >= 1000:
				self.Abonado = int(self.Abonado) + int(prefijo)
			self.datosparaGUI = (str(self.Abonado),self.dividida.group('Evento'),'No Aplica','No Aplica',self.dividida.group('Linea'),self.nombreformato,LaFecha.damefecha())
			self.datosparaBD = (trama,self.dividida.group('Linea'),str(self.Abonado),self.dividida.group('Evento'),'0',self.numprotocolo,'1',numpuerto,'0')
			#Insertar En Base de Datos
			ColaParaGuardar.append(self.datosparaBD)
			fila = 0
			columna = 0
			globalvar["listadetablas"]["tabla"+str(numpuerto)].insertRow(0)
			for item in self.datosparaGUI:
				texto = QTableWidgetItem(item)
				globalvar["listadetablas"]["tabla"+str(numpuerto)].setItem(fila,columna,texto)
				columna = columna + 1
			#Contamos la cantidad de columnas en la tabla
			if globalvar["listadetablas"]["tabla"+str(numpuerto)].rowCount() > 300:
				globalvar["listadetablas"]["tabla"+str(numpuerto)].removeRow(301)
			print self.dividida.groups()
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(self.dividida.groups())
		except Exception as exc:
			self.tramafail = trama + "Error al Tratar Protocolo, Chequea ErrorLOG"
			GuardarTramaObjeto.GuardarTXTFail(self.tramafail)
			GuardarTramaObjeto.GuardarErrores(str(exc))
		
CuatromasDos_MCDIobjeto = CuatromasDos_MCDI()

class ContactID_MCDI(object):
	def __init__(self):
		self.nombre = "ContactID del MCDI" 
		self.nombreformato = "CID"
		self.numprotocolo = '2'
		self.eregular = '\d\d:\d\d  \d\d/\d\d\[/\d\d\]  .. .... 18 \D... .. ...'
	def tratar(self,trama,numpuerto,prefijo):
		#colaCIDMLR2.append(trama)
		try:
			self.patron = re.compile('(?P<Fecha>\d\d:\d\d  \d\d/\d\d\[/\d\d\]  )(?P<Receptor>.)(?P<Linea>.)(?P<Espacio> )(?P<Abonado>....)(?P<Espacio2> )(?P<ID>18)(?P<Espacio3> )(?P<Evento>\D...)(?P<Espacio4> )(?P<Particion>..)(?P<Espacio5> )(?P<Nada>.)(?P<ZonaUsuario>\d{2,})')
			self.dividida = self.patron.search(trama)
			#Agregando el prefijo al Abonado en caso de que lo tenga
			self.Abonado = str(self.dividida.group('Abonado'))
			if int(prefijo) >= 1000:
				self.Abonado = int(self.Abonado) + int(prefijo)
			self.datosparaGUI = (str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),self.dividida.group('Particion'),self.dividida.group('Linea'),self.nombreformato,LaFecha.damefecha())
			self.datosparaBD = (trama,self.dividida.group('Linea'),str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),self.numprotocolo,self.dividida.group('Particion'),numpuerto,'0')
			ColaParaGuardar.append(self.datosparaBD)
			#Variables para Insertar
			fila = 0
			columna = 0
			globalvar["listadetablas"]["tabla"+str(numpuerto)].insertRow(0)
			for item in self.datosparaGUI:
				texto = QTableWidgetItem(item)
				globalvar["listadetablas"]["tabla"+str(numpuerto)].setItem(fila,columna,texto)
				columna = columna + 1
			#Contamos la cantidad de columnas en la tabla
			if globalvar["listadetablas"]["tabla"+str(numpuerto)].rowCount() > 300:
				globalvar["listadetablas"]["tabla"+str(numpuerto)].removeRow(301)
			print self.dividida.groups()
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(self.dividida.groups())
		except Exception as exc:
			self.tramafail = trama + "Error al Tratar Protocolo, Chequea ErrorLOG"
			GuardarTramaObjeto.GuardarTXTFail(self.tramafail)
			GuardarTramaObjeto.GuardarErrores(str(exc))

ContactID_MCDIobjeto = ContactID_MCDI()

class ModemSia_MCDI(object):
	def __init__(self):
		self.nombre = "Modem Sia del MCDI"
		self.nombreformato = "SIA"
		self.numprotocolo = '1'
		self.eregular = '\d\d:\d\d  \d\d/\d\d\[/\d\d\]  .. \[#......\|......(]|/)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)'
	def tratar(self,trama,numpuerto,prefijo):
		#colaSIA3.append(trama)
		try:
			if len(trama) >= 40:  #Deberia detectarla por varios / y no por el tamano
				#Como la Trama viene con muchos eventos, la pico en el primer Slash para Tener
				#El principio de la trama para todos los eventos
				tramadividida = trama.split("|",1)
				#Ahora pico todos los eventos por su Slash
				listadeeventos = tramadividida[1].split("/")
				listadetramas = []
				for i in listadeeventos:
						if len(i) == 5 or i[5] == ']':
							#Agrego una letra i al principio para trabajar con un solo
							#Patron abajo, simulando que todos los eventos vienen asi
							#Como el primer evento de la cadena
							i = 'i' + i
						tr = tramadividida[0] + '|' + i.rstrip(']') + ']'
						listadetramas.append(tr)
						self.patron = re.compile('(?P<Fecha>\d\d:\d\d  \d\d/\d\d\[/\d\d\]  )(?P<Receptor>.)(?P<Linea>.)(?P<Espacio> )(?P<Nada>\[\#)(?P<Abonado>[a-z0-9A-Z]{1,6})(?P<Separador>\|)(?P<CodigoFuncion>.)(?P<Evento>..)(?P<ZonaUsuario>...)')
						self.dividida = self.patron.search(tr)
						#Agregando el prefijo al Abonado en caso de que lo tenga
						self.Abonado = str(self.dividida.group('Abonado'))
						if int(prefijo) >= 1000:
							self.Abonado = int(self.Abonado) + int(prefijo)

						self.datosparaGUI = (str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),'1',self.dividida.group('Linea'),self.nombreformato,LaFecha.damefecha())
						self.datosparaBD = (trama,self.dividida.group('Linea'),str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),self.numprotocolo,'1',numpuerto,'0')
						#Insertar En Base de Datos
						ColaParaGuardar.append(self.datosparaBD)
						fila = 0
						columna = 0
						globalvar["listadetablas"]["tabla"+str(numpuerto)].insertRow(0)
						for item in self.datosparaGUI:
							texto = QTableWidgetItem(item)
							globalvar["listadetablas"]["tabla"+str(numpuerto)].setItem(fila,columna,texto)
							columna = columna + 1
						#Contamos la cantidad de columnas en la tabla
						if globalvar["listadetablas"]["tabla"+str(numpuerto)].rowCount() > 300:
							globalvar["listadetablas"]["tabla"+str(numpuerto)].removeRow(301)
						print self.dividida.groups()
						#Guardar en el Log
						GuardarTramaObjeto.GuardarTXTLog(self.dividida.groups())
				#print listadetramas
			#Si es una trama que trae un solo evento entonces
			else:
				self.patron = re.compile('(?P<Fecha>\d\d:\d\d  \d\d/\d\d\[/\d\d\]  )(?P<Receptor>.)(?P<Linea>.)(?P<Espacio> )(?P<Nada>\[\#)(?P<Abonado>[a-z0-9A-Z]{1,6})(?P<Separador>\|)(?P<CodigoFuncion>.)(?P<Evento>..)(?P<ZonaUsuario>...)')
				self.dividida = self.patron.search(trama)
				#Le agregamos el prefijo si lo tiene
				self.Abonado = self.dividida.group('Abonado')
				self.Abonado = int(self.Abonado) + int(prefijo)
				#Agregando el prefijo al Abonado en caso de que lo tenga
				self.Abonado = str(self.dividida.group('Abonado'))
				if int(prefijo) >= 1000:
					self.Abonado = int(self.Abonado) + int(prefijo)
				self.datosparaGUI = (str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),'1',self.dividida.group('Linea'),self.nombreformato,LaFecha.damefecha())
				self.datosparaBD = (trama,self.dividida.group('Linea'),str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),self.numprotocolo,'1',numpuerto,'0')
				#Insertar En Base de Datos
				ColaParaGuardar.append(self.datosparaBD)
				fila = 0
				columna = 0
				globalvar["listadetablas"]["tabla"+str(numpuerto)].insertRow(0)
				for item in self.datosparaGUI:
					texto = QTableWidgetItem(item)
					globalvar["listadetablas"]["tabla"+str(numpuerto)].setItem(fila,columna,texto)
					columna = columna + 1
				#Contamos la cantidad de columnas en la tabla
				if globalvar["listadetablas"]["tabla"+str(numpuerto)].rowCount() > 300:
					globalvar["listadetablas"]["tabla"+str(numpuerto)].removeRow(301)
				print self.dividida.groups()
				#Guardar en el Log
				GuardarTramaObjeto.GuardarTXTLog(self.dividida.groups())
		except Exception as exc:
			self.tramafail = trama + "Error al Tratar Protocolo, Chequea ErrorLOG"
			GuardarTramaObjeto.GuardarTXTFail(self.tramafail)
			GuardarTramaObjeto.GuardarErrores(str(exc))

ModemSia_MCDIobjeto = ModemSia_MCDI()

class ModemSia_MCDIAdemco685(object):
	def __init__(self):
		self.nombre = "Modem Sia del MCDI emulando ADEMCO685"
		self.nombreformato = "SIA"
		self.numprotocolo = '1'
		self.eregular = '.. \[#......\|......(]|/)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)(]|/|)(\S....|)'
	def tratar(self,trama,numpuerto,prefijo):
		#colaSIA3.append(trama)
		try:
			if len(trama) >= 33:  #Deberia detectarla por varios / y no por el tamano
				#Como la Trama viene con muchos eventos, la pico en el primer Slash para Tener
				#El principio de la trama para todos los eventos
				tramadividida = trama.split("|",1)
				#Ahora pico todos los eventos por su Slash
				listadeeventos = tramadividida[1].split("/")
				listadetramas = []
				for i in listadeeventos:
						if len(i) == 5 or i[5] == ']':
							#Agrego una letra i al principio para trabajar con un solo
							#Patron abajo, simulando que todos los eventos vienen asi
							#Como el primer evento de la cadena
							i = 'i' + i
						tr = tramadividida[0] + '|' + i.rstrip(']') + ']'
						listadetramas.append(tr)
						self.patron = re.compile('(?P<Receptor>.)(?P<Linea>.)(?P<Espacio> )(?P<Nada>\[\#)(?P<Abonado>[a-z0-9A-Z]{1,6})(?P<Separador>\|)(?P<CodigoFuncion>.)(?P<Evento>..)(?P<ZonaUsuario>...)')
						self.dividida = self.patron.search(tr)
						#Agregando el prefijo al Abonado en caso de que lo tenga
						self.Abonado = str(self.dividida.group('Abonado'))
						if int(prefijo) >= 1000:
							self.Abonado = int(self.Abonado) + int(prefijo)
						self.datosparaGUI = (str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),'1',self.dividida.group('Linea'),self.nombreformato,LaFecha.damefecha())
						self.datosparaBD = (trama,self.dividida.group('Linea'),str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),self.numprotocolo,'1',numpuerto,'0')
						#Insertar En Base de Datos
						ColaParaGuardar.append(self.datosparaBD)
						fila = 0
						columna = 0
						globalvar["listadetablas"]["tabla"+str(numpuerto)].insertRow(0)
						for item in self.datosparaGUI:
							texto = QTableWidgetItem(item)
							globalvar["listadetablas"]["tabla"+str(numpuerto)].setItem(fila,columna,texto)
							columna = columna + 1
						#Contamos la cantidad de columnas en la tabla
						if globalvar["listadetablas"]["tabla"+str(numpuerto)].rowCount() > 300:
							globalvar["listadetablas"]["tabla"+str(numpuerto)].removeRow(301)
						print self.dividida.groups()
						#Guardar en el Log
						GuardarTramaObjeto.GuardarTXTLog(self.dividida.groups())
				#print listadetramas
			#Si es una trama que trae un solo evento entonces
			else:
				self.patron = re.compile('(?P<Receptor>.)(?P<Linea>.)(?P<Espacio> )(?P<Nada>\[\#)(?P<Abonado>[a-z0-9A-Z]{1,6})(?P<Separador>\|)(?P<CodigoFuncion>.)(?P<Evento>..)(?P<ZonaUsuario>...)')
				self.dividida = self.patron.search(trama)
				#Agregando el prefijo al Abonado en caso de que lo tenga
				self.Abonado = str(self.dividida.group('Abonado'))
				if int(prefijo) >= 1000:
					self.Abonado = int(self.Abonado) + int(prefijo)
				self.datosparaGUI = (str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),'1',self.dividida.group('Linea'),self.nombreformato,LaFecha.damefecha())
				self.datosparaBD = (trama,self.dividida.group('Linea'),str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),self.numprotocolo,'1',numpuerto,'0')
				#Insertar En Base de Datos
				ColaParaGuardar.append(self.datosparaBD)
				fila = 0
				columna = 0
				globalvar["listadetablas"]["tabla"+str(numpuerto)].insertRow(0)
				for item in self.datosparaGUI:
					texto = QTableWidgetItem(item)
					globalvar["listadetablas"]["tabla"+str(numpuerto)].setItem(fila,columna,texto)
					columna = columna + 1
				#Contamos la cantidad de columnas en la tabla
				if globalvar["listadetablas"]["tabla"+str(numpuerto)].rowCount() > 300:
					globalvar["listadetablas"]["tabla"+str(numpuerto)].removeRow(301)
				print self.dividida.groups()
				#Guardar en el Log
				GuardarTramaObjeto.GuardarTXTLog(self.dividida.groups())
		except Exception as exc:
			self.tramafail = trama + "Error al Tratar Protocolo, Chequea ErrorLOG"
			GuardarTramaObjeto.GuardarTXTFail(self.tramafail)
			GuardarTramaObjeto.GuardarErrores(str(exc))

ModemSia_MCDIAdemco685objeto = ModemSia_MCDIAdemco685()

#Formatos del Silent Knigth 

class ContactID_SilentKnight(object):
	def __init__(self):
		self.nombre = "ContactID del Silent Knight" 
		self.nombreformato = "CID"
		self.numprotocolo = '2'
		self.eregular = '&......"......".."....".........."18.........(,.|.|,|")(18.........|)(,.|.|,|"|)(18.........|)(,.|.|,|"|)(18.........|)(,.|.|,|"|)(18.........|)(,.|.|,|"|)(18.........|)(,.|.|,|"|)(18.........|)(,.|.|,|"|)(18.........|)(,.|.|,|"|)(18.........|)(,.|.|,|"|)(18.........|)(,.|.|,|"|)(18.........|)(,.|.|,|"|)(18.........|)(,.|.|,|"|)(18.........|)(,.|.|,|"|)(18.........|)(,.|.|,|"|)(18.........|)(,.|.|,|"|)(18.........|)(,.|.|,|"|)(18.........|)(,.|.|,|"|)(18.........|)(,.|.|,|"|)(18.........|)(,.|.|,|"|)(18.........|)(,.|.|,|"|)(18.........|)(,.|.|,|"|)(18.........|)(,.|.|,|"|)(18.........|)'
	def tratar(self,trama,numpuerto,prefijo):
		try:
			if len(trama) >= 50:  #Deberia detectarla por varios / y no por el tamano
				#Pico la trama en el 4 " para tener la parte de la trama que me importa y quitar la basura de la fecha y demas cosas que llegan
				#Con este receptor
				picartrama = trama.split('"',4)
				#Como la Trama viene con muchos eventos, la pico en el primer " para Tener
				#El principio de la trama para todos los eventos
				tramadividida = picartrama[4].split('"',1)
				#Ahora pico todos los eventos por su "
				listadeeventos = tramadividida[1].split('"')
				for i in listadeeventos:
					tr = picartrama[0] + '"' + picartrama[1] + '"' + picartrama[2] + '"' + picartrama[3] + '"' + tramadividida[0] + '"' + i 
					self.patron = re.compile('(?P<Nada>&......"......".."...."..)(?P<Receptor>\d\d)(?P<Linea>[0-9a-zA-Z]{1,3})(?P<Espacio>.)(?P<Abonado>....)(?P<Separador>")(?P<ID>18)(?P<Evento>\d\d\d\d)(?P<Particion>\d\d)(?P<ZonaUsuario>\d{2,})')
					self.dividida = self.patron.search(tr)
					#Agregando el prefijo al Abonado en caso de que lo tenga
					self.Abonado = str(self.dividida.group('Abonado'))
					if int(prefijo) >= 1000:
						self.Abonado = int(self.Abonado) + int(prefijo)
					self.datosparaGUI = (str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),self.dividida.group('Particion'),self.dividida.group('Linea'),self.nombreformato,LaFecha.damefecha())
					self.datosparaBD = (trama,self.dividida.group('Linea'),str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),self.numprotocolo,self.dividida.group('Particion'),numpuerto,'0')
					#Insertar En Base de Datos
					ColaParaGuardar.append(self.datosparaBD)
					fila = 0
					columna = 0
					globalvar["listadetablas"]["tabla"+str(numpuerto)].insertRow(0)
					for item in self.datosparaGUI:
						texto = QTableWidgetItem(item)
						globalvar["listadetablas"]["tabla"+str(numpuerto)].setItem(fila,columna,texto)
						columna = columna + 1
					#Contamos la cantidad de columnas en la tabla
					if globalvar["listadetablas"]["tabla"+str(numpuerto)].rowCount() > 300:
						globalvar["listadetablas"]["tabla"+str(numpuerto)].removeRow(301)
					print self.dividida.groups()
					#Guardar en el Log
					GuardarTramaObjeto.GuardarTXTLog(self.dividida.groups())
		#Si es una trama que trae un solo evento entonces
			else:
				self.patron = re.compile('(?P<Nada>&......"......".."...."..)(?P<Receptor>\d\d)(?P<Linea>[0-9a-zA-Z]{1,3})(?P<Espacio>.)(?P<Abonado>....)(?P<Separador>")(?P<ID>18)(?P<Evento>\d\d\d\d)(?P<Particion>\d\d)(?P<ZonaUsuario>\d{2,})')
				self.dividida = self.patron.search(trama)
				#Agregando el prefijo al Abonado en caso de que lo tenga
				self.Abonado = str(self.dividida.group('Abonado'))
				if int(prefijo) >= 1000:
					self.Abonado = int(self.Abonado) + int(prefijo)
				self.datosparaGUI = (str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),self.dividida.group('Particion'),self.dividida.group('Linea'),self.nombreformato,LaFecha.damefecha())
				self.datosparaBD = (trama,self.dividida.group('Linea'),str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),self.numprotocolo,self.dividida.group('Particion'),numpuerto,'0')
				#Insertar En Base de Datos
				ColaParaGuardar.append(self.datosparaBD)
				fila = 0
				columna = 0
				globalvar["listadetablas"]["tabla"+str(numpuerto)].insertRow(0)
				for item in self.datosparaGUI:
					texto = QTableWidgetItem(item)
					globalvar["listadetablas"]["tabla"+str(numpuerto)].setItem(fila,columna,texto)
					columna = columna + 1
				#Contamos la cantidad de columnas en la tabla
				if globalvar["listadetablas"]["tabla"+str(numpuerto)].rowCount() > 300:
					globalvar["listadetablas"]["tabla"+str(numpuerto)].removeRow(301)
				print self.dividida.groups()
				#Guardar en el Log
				GuardarTramaObjeto.GuardarTXTLog(self.dividida.groups())
		except Exception as exc:
			self.tramafail = trama + "Error al Tratar Protocolo, Chequea ErrorLOG"
			GuardarTramaObjeto.GuardarTXTFail(self.tramafail)
			GuardarTramaObjeto.GuardarErrores(str(exc))

ContactID_SilentKnightobjeto = ContactID_SilentKnight()

class Sia1_SilentKnight(object):
	def __init__(self):
		self.nombre = "SIA sin Particion del SilentKnight"
		self.nombreformato = "SIA"
		self.numprotocolo = '1'
		self.eregular = '&......"......".."...."......(......|.....|....)"(\w\w\d\d\d|\w\w\d\d|\w\w\d)(,.|.|")(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)(\w\w\d\d\d|\w\w\d\d|\w\w\d|)(,.|.|"|)'
	def tratar(self,trama,numpuerto,prefijo):
		#colaSIA3.append(trama)
		try:
			if len(trama) >= 42:  #Deberia detectarla por varios " y no por el tamano
				#Pico la trama en el 4 " para tener la parte de la trama que me importa y quitar la basura de la fecha y demas cosas que llegan
				#Con este receptor
				picartrama = trama.split('"',4)
				#Como la Trama viene con muchos eventos, la pico en el primer " para Tener
				#El principio de la trama para todos los eventos
				tramadividida = picartrama[4].split('"',1)
				#Ahora pico todos los eventos por su "
				listadeeventos = tramadividida[1].split('"')
				for i in listadeeventos:
					tr = picartrama[0] + '"' + picartrama[1] + '"' + picartrama[2] + '"' + picartrama[3] + '"' + tramadividida[0] + '"' + i 
					self.patron = re.compile('(?P<Nada>&......"......".."....".)(?P<Receptor>\d\d)(?P<Linea>[0-9a-zA-Z]{1,3})(?P<Espacio>.)(?P<Abonado>[0-9a-zA-Z ]{1,6})(?P<Separador>")(?P<Evento>..)(?P<ZonaUsuario>\d{1,})')
					self.dividida = self.patron.search(tr)
					#Agregando el prefijo al Abonado en caso de que lo tenga
					self.Abonado = str(self.dividida.group('Abonado'))
					if int(prefijo) >= 1000:
						self.Abonado = int(self.Abonado) + int(prefijo)
					self.datosparaGUI = (str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),'1',self.dividida.group('Linea'),self.nombreformato,LaFecha.damefecha())
					self.datosparaBD = (trama,self.dividida.group('Linea'),str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),self.numprotocolo,'1',numpuerto,'0')
					#Insertar En Base de Datos
					ColaParaGuardar.append(self.datosparaBD)
					fila = 0
					columna = 0
					globalvar["listadetablas"]["tabla"+str(numpuerto)].insertRow(0)
					for item in self.datosparaGUI:
						texto = QTableWidgetItem(item)
						globalvar["listadetablas"]["tabla"+str(numpuerto)].setItem(fila,columna,texto)
						columna = columna + 1
					#Contamos la cantidad de columnas en la tabla
					if globalvar["listadetablas"]["tabla"+str(numpuerto)].rowCount() > 300:
						globalvar["listadetablas"]["tabla"+str(numpuerto)].removeRow(301)
					print self.dividida.groups()
					#Guardar en el Log
					GuardarTramaObjeto.GuardarTXTLog(self.dividida.groups())
		#Si es una trama que trae un solo evento entonces
			else:
				self.patron = re.compile('(?P<Nada>&......"......".."....".)(?P<Receptor>\d\d)(?P<Linea>[0-9a-zA-Z]{1,3})(?P<Espacio>.)(?P<Abonado>[0-9a-zA-Z ]{1,6})(?P<Separador>")(?P<Evento>..)(?P<ZonaUsuario>\d{1,})')
				self.dividida = self.patron.search(trama)
				#Agregando el prefijo al Abonado en caso de que lo tenga
				self.Abonado = str(self.dividida.group('Abonado'))
				if int(prefijo) >= 1000:
					self.Abonado = int(self.Abonado) + int(prefijo)
				self.datosparaGUI = (str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),'1',self.dividida.group('Linea'),self.nombreformato,LaFecha.damefecha())
				self.datosparaBD = (trama,self.dividida.group('Linea'),str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),self.numprotocolo,'1',numpuerto,'0')
				#Insertar En Base de Datos
				ColaParaGuardar.append(self.datosparaBD)
				fila = 0
				columna = 0
				globalvar["listadetablas"]["tabla"+str(numpuerto)].insertRow(0)
				for item in self.datosparaGUI:
					texto = QTableWidgetItem(item)
					globalvar["listadetablas"]["tabla"+str(numpuerto)].setItem(fila,columna,texto)
					columna = columna + 1
				#Contamos la cantidad de columnas en la tabla
				if globalvar["listadetablas"]["tabla"+str(numpuerto)].rowCount() > 300:
					globalvar["listadetablas"]["tabla"+str(numpuerto)].removeRow(301)
				print self.dividida.groups()
				#Guardar en el Log
				GuardarTramaObjeto.GuardarTXTLog(self.dividida.groups())
		except Exception as exc:
			self.tramafail = trama + "Error al Tratar Protocolo, Chequea ErrorLOG"
			GuardarTramaObjeto.GuardarTXTFail(self.tramafail)
			GuardarTramaObjeto.GuardarErrores(str(exc))

Sia1_SilentKnightobjeto = Sia1_SilentKnight()

class Sia2_SilentKnight(object):
	def __init__(self):
		self.nombre = "SIA con Particion del SilentKnight"
		self.nombreformato = "SIA"
		self.numprotocolo = '1'
		self.eregular = '&(......"......".."...."......(......|.....|....)"ri.)(,.|.|")(\w\w\d\d\d|\w\w\d\d|ri.|)(,.|[(^\#-|^\ )]|"|)(\w\w\d\d\d|\w\w\d\d|ri.|)(,.|[(^\#-|^\ )]|"|)(\w\w\d\d\d|\w\w\d\d|ri.|)(,.|[(^\#-|^\ )]|"|)(\w\w\d\d\d|\w\w\d\d|ri.|)(,.|[(^\#-|^\ )]|"|)(\w\w\d\d\d|\w\w\d\d|ri.|)(,.|[(^\#-|^\ )]|"|)(\w\w\d\d\d|\w\w\d\d|ri.|)(,.|[(^\#-|^\ )]|"|)(\w\w\d\d\d|\w\w\d\d|ri.|)(,.|[(^\#-|^\ )]|"|)(\w\w\d\d\d|\w\w\d\d|ri.|)(,.|[(^\#-|^\ )]|"|)(\w\w\d\d\d|\w\w\d\d|ri.|)(,.|[(^\#-|^\ )]|"|)(\w\w\d\d\d|\w\w\d\d|ri.|)(,.|[(^\#-|^\ )]|"|)(\w\w\d\d\d|\w\w\d\d|ri.|)(,.|[(^\#-|^\ )]|"|)(\w\w\d\d\d|\w\w\d\d|ri.|)(,.|[(^\#-|^\ )]|"|)(\w\w\d\d\d|\w\w\d\d|ri.|)(,.|[(^\#-|^\ )]|"|)(\w\w\d\d\d|\w\w\d\d|ri.|)(,.|[(^\#-|^\ )]|"|)(\w\w\d\d\d|\w\w\d\d|ri.|)(,.|[(^\#-|^\ )]|"|)(\w\w\d\d\d|\w\w\d\d|ri.|)(,.|[(^\#-|^\ )]|"|)(\w\w\d\d\d|\w\w\d\d|ri.|)(,.|[(^\#-|^\ )]|"|)(\w\w\d\d\d|\w\w\d\d|ri.|)(,.|[(^\#-|^\ )]|"|)(\w\w\d\d\d|\w\w\d\d|ri.|)(,.|[(^\#-|^\ )]|"|)(\w\w\d\d\d|\w\w\d\d|ri.|)(,.|[(^\#-|^\ )]|"|)(\w\w\d\d\d|\w\w\d\d|ri.|)(,.|[(^\#-|^\ )]|"|)(\w\w\d\d\d|\w\w\d\d|ri.|)(,.|[(^\#-|^\ )]|"|)(\w\w\d\d\d|\w\w\d\d|ri.|)(,.|[(^\#-|^\ )]|"|)'
	def tratar(self,trama,numpuerto,prefijo):
		#colaSIA3.append(trama)
		try:
			if len(trama) >= 42:  #Deberia detectarla por varios " y no por el tamano
				#Pico la trama en el 4 " para tener la parte de la trama que me importa y quitar la basura de la fecha y demas cosas que llegan
				#Con este receptor
				picartrama = trama.split('"',4)
				#Como la Trama viene con muchos eventos, la pico en el primer " para Tener
				#El principio de la trama para todos los eventos
				tramadividida = picartrama[4].split('"',1)
				#Ahora pico todos los eventos por su "
				listadeeventos = tramadividida[1].split('"')
				#Definiendo la particion inicial de la trama para colocarla a los eventos
				#Al menos que mas adelante este una nueva particion
				particionactual = "1"
				for i in listadeeventos:
					#Si entre los eventos hay un cambio de particion que venga ri y un numero
					if re.match("ri\d",i):
						#Guardamos el numero de particion quitandole el ri
						particionactual = i
					else:
						#Reemplazamos la particion de la trama por la particion Actual
						tr = picartrama[0] + '"' + picartrama[1] + '"' + picartrama[2] + '"' + picartrama[3] + '"' + tramadividida[0] + '"'+ particionactual+ '"' + i 
						self.patron = re.compile('(?P<Nada>&......"......".."....".)(?P<Receptor>\d\d)(?P<Linea>[0-9a-zA-Z]{1,3})(?P<Espacio>.)(?P<Abonado>[a-z0-9A-Z ]{1,6})(?P<Separador>")(?P<Particion>ri.)(?P<Separador2>")(?P<Evento>..)(?P<ZonaUsuario>\d{2,})')
						self.dividida = self.patron.search(tr)
						#Agregando el prefijo al Abonado en caso de que lo tenga
						self.Abonado = str(self.dividida.group('Abonado'))
						if int(prefijo) >= 1000:
							self.Abonado = int(self.Abonado) + int(prefijo)
						#Este SIA de este Receptor, puede venir con espacios en Blanco en el Abonado
						#por ejemplo "  0001" entonces convirtiendolo a INT arriba si tiene prefiji
						#Se le quitan pero si no tiene prefijo, entonces se los quito a pie con el
						#else de abajo
						else:
							self.Abonado = self.Abonado.replace(" ","")
						self.datosparaGUI = (str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),str(particionactual.replace("ri","")),self.dividida.group('Linea'),self.nombreformato,LaFecha.damefecha())
						self.datosparaBD = (trama,self.dividida.group('Linea'),str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),self.numprotocolo,str(particionactual.replace("ri","")),numpuerto,'0')
						#Insertar En Base de Datos
						ColaParaGuardar.append(self.datosparaBD)
						fila = 0
						columna = 0
						globalvar["listadetablas"]["tabla"+str(numpuerto)].insertRow(0)
						for item in self.datosparaGUI:
							texto = QTableWidgetItem(item)
							globalvar["listadetablas"]["tabla"+str(numpuerto)].setItem(fila,columna,texto)
							columna = columna + 1
						#Contamos la cantidad de columnas en la tabla
						if globalvar["listadetablas"]["tabla"+str(numpuerto)].rowCount() > 300:
							globalvar["listadetablas"]["tabla"+str(numpuerto)].removeRow(301)
						print self.dividida.groups()
						#Guardar en el Log
						GuardarTramaObjeto.GuardarTXTLog(self.dividida.groups())
		#Si es una trama que trae un solo evento entonces
			else:
				self.patron = re.compile('(?P<Nada>&......"......".."....".)(?P<Receptor>\d\d)(?P<Linea>[0-9a-zA-Z]{1,3})(?P<Espacio>.)(?P<Abonado>[a-z0-9A-Z ]{1,6})(?P<Separador>")(?P<Particion>ri.)(?P<Separador2>")(?P<Evento>..)(?P<ZonaUsuario>\d{2,})')
				self.dividida = self.patron.search(trama)
				#Agregando el prefijo al Abonado en caso de que lo tenga
				self.Abonado = str(self.dividida.group('Abonado'))
				if int(prefijo) >= 1000:
					self.Abonado = int(self.Abonado) + int(prefijo)
				#Este SIA de este Receptor, puede venir con espacios en Blanco en el Abonado
				#por ejemplo "  0001" entonces convirtiendolo a INT arriba si tiene prefiji
				#Se le quitan pero si no tiene prefijo, entonces se los quito a pie con el
				#else de abajo
				else:
					self.Abonado = self.Abonado.replace(" ","")
				self.datosparaGUI = (str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),particionactual,self.dividida.group('Linea'),self.nombreformato,LaFecha.damefecha())
				self.datosparaBD = (trama,self.dividida.group('Linea'),str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),self.numprotocolo,particionactual,numpuerto,'0')
				#Insertar En Base de Datos
				ColaParaGuardar.append(self.datosparaBD)
				fila = 0
				columna = 0
				globalvar["listadetablas"]["tabla"+str(numpuerto)].insertRow(0)
				for item in self.datosparaGUI:
					texto = QTableWidgetItem(item)
					globalvar["listadetablas"]["tabla"+str(numpuerto)].setItem(fila,columna,texto)
					columna = columna + 1
				#Contamos la cantidad de columnas en la tabla
				if globalvar["listadetablas"]["tabla"+str(numpuerto)].rowCount() > 300:
					globalvar["listadetablas"]["tabla"+str(numpuerto)].removeRow(301)
				print self.dividida.groups()
				#Guardar en el Log
				GuardarTramaObjeto.GuardarTXTLog(self.dividida.groups())
		except Exception as exc:
			self.tramafail = trama + "Error al Tratar Protocolo, Chequea ErrorLOG"
			GuardarTramaObjeto.GuardarTXTFail(self.tramafail)
			GuardarTramaObjeto.GuardarErrores(str(exc))

Sia2_SilentKnightobjeto = Sia2_SilentKnight()

class XML_EBS(object):
	def __init__(self):
		self.nombre = "XML del EBS"
		self.nombreformato = "XML"
		self.nombreformatoCIDEmbeded = "CID Interno"
		self.nombreformatoSIAEmbeded = "SIA Interno"

		self.numprotocolo = '5'
		self.numprotocoloCID = '2'  #Opcional por si se utiliza una LX para transmitir senales de una alarma.
		self.numprotocoloSIA = '1'	 #Opcional por si se utiliza una LX para transmitir senales de una alarma.
		self.eregular = '<packet.{0,}</packet>'
	def tratarDTMF(self,trama,numpuerto,prefijo): #Para que cuando una trama XML traiga un evento en DTMF de una alarma, decodificar el HEX y tratarlo 
		error=open('DTMF.dat','a')
		error.write(str(trama)+"\n")
		error.close()
		self.patron = re.compile('(?P<Inicio><packet.{5,100}>)(?P<IncioMsg><msg )(?P<Dispositivo>dt="..")(?P<Separacion1> )(?P<Serial>sn=".{0,20}")(?P<Separacion2> )(?P<FechaDisp>dts="\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d"|)(?P<Separacion3> |)(?P<FechaOSM>csts="\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d"|)(?P<Separacion4> )(?P<SRC>src="[^"]{1,20}")(?P<Separacion5> )(?P<Evento>evt="[^"]{1,25}")(?P<Separacion6> |)(?P<DataEvento>evtData="[^"]{0,500}"|)(?P<Separacion7> |)(?P<CSQ>CSQ="[^"]{0,6}"|)(?P<Separacion8> |)(?P<EstatusConexion>ConnectionStatus="[^"]{0,50}"|)(?P<Separacion9> |)(?P<Bateria>BattVol="[^"]{0,15}"|)(?P<Separacion10> |)(?P<EstatusPower>PowerStatus="[^"]{0,80}"|)(?P<Separacion11> |)(?P<ActividadMovimiento>MovementActivity="[^"]{0,6}"|)(?P<Separacion12> |)(?P<GPS>gps="[^"]{0,100}"|)')
		self.dividida = self.patron.search(trama)
		#Arreglando los Elementos de la trama
		self.Dispositivo = str(self.dividida.group('Dispositivo')).replace('dt="','').replace('"','')
		self.Serial = str(self.dividida.group('Serial')).replace('sn="','').replace('"','')
		self.FechaDisp = str(self.dividida.group('FechaDisp')).replace('dts="','').replace('"','')
		self.FechaOSM = str(self.dividida.group('FechaOSM')).replace('csts="','').replace('"','')
		self.Source = str(self.dividida.group('SRC')).replace('src="','').replace('"','')
		self.Evento = str(self.dividida.group('Evento')).replace('evt="','').replace('"','')
		self.DataEvento = str(self.dividida.group('DataEvento')).replace('evtData="','').replace('"','')
		if str(self.DataEvento[:2]) == '0x':
			pass
		self.Signal = str(self.dividida.group('CSQ')).replace('CSQ="','').replace('"','')
		self.EstatusConexion = str(self.dividida.group('EstatusConexion')).replace('ConnectionStatus="','').replace('"','')
		self.EstatusPower = str(self.dividida.group('EstatusPower')).replace('PowerStatus="','').replace('"','')
		self.ActividadMovimiento = str(self.dividida.group('ActividadMovimiento')).replace('MovementActivity="','').replace('"','')
		self.GPS = str(self.dividida.group('GPS')).replace('gps="','').replace('"','')


		self.DataEvento = self.DataEvento[2:].decode('hex')[2:17]
		#Si es en ContactID
		if re.match('....18\d\d\d\d.....',self.DataEvento):
			self.patron = re.compile('(?P<Abonado>....)(?P<ID>18)(?P<Evento>....)(?P<Particion>..)(?P<ZonaUsuario>.{2,})')
			self.dividida = self.patron.search(self.DataEvento)
			self.Abonado = str(self.dividida.group('Abonado'))
			self.Evento = str(self.dividida.group('Evento'))
			if self.Evento[0] == '1':
				self.Evento = 'E'+self.Evento[1:]
			elif self.Evento[0] == '3':
				self.Evento = 'R'+self.Evento[1:]
			self.Particion = str(self.dividida.group('Particion'))
			self.ZonaUsuario = str(self.dividida.group('ZonaUsuario'))
			#Agregando el prefijo al Abonado en caso de que lo tenga
			if int(prefijo) >= 1000:
				self.Abonado = int(self.Abonado) + int(prefijo)
			self.datosparaGUI = (str(self.Abonado),self.Evento,self.ZonaUsuario,self.Particion,str(1),self.nombreformatoCIDEmbeded,LaFecha.damefecha())
			self.datosparaBD = (str(trama),str(1),str(self.Abonado),self.Evento,self.ZonaUsuario,self.numprotocoloCID,self.Particion,numpuerto,'0')
			#Insertar En Base de Datos
			ColaParaGuardar.append(self.datosparaBD)
			fila = 0
			columna = 0
			globalvar["listadetablas"]["tabla"+str(numpuerto)].insertRow(0)
			for item in self.datosparaGUI:
				texto = QTableWidgetItem(item)
				globalvar["listadetablas"]["tabla"+str(numpuerto)].setItem(fila,columna,texto)
				columna = columna + 1
			#Contamos la cantidad de columnas en la tabla
			if globalvar["listadetablas"]["tabla"+str(numpuerto)].rowCount() > 300:
				globalvar["listadetablas"]["tabla"+str(numpuerto)].removeRow(301)
			print self.dividida.groups()
			#Guardar en el Log
			#print 'GUARDANDO LOG'
			GuardarTramaObjeto.GuardarTXTLog(self.dividida.groups())
	
	def tratarONOFFLX(self,trama,numpuerto,prefijo):
		try:
			if 'evt="OFF' in trama:
				zone = re.search('(?<=evt="OFF)\d{0,50}', trama)
				self.Evento = "OFF"
				self.DataEvento = str(zone.group(0))
			elif 'evt="ON' in trama:
				zone = re.search('(?<=evt="ON)\d{0,50}', trama)
				self.Evento = "ON"
				self.DataEvento = str(zone.group(0))
			self.patron = re.compile('(?P<Inicio><packet.{5,100}>)(?P<IncioMsg><msg )(?P<Dispositivo>dt="..")(?P<Separacion1> )(?P<Serial>sn=".{0,20}")(?P<Separacion2> )(?P<FechaDisp>dts="\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d"|)(?P<Separacion3> |)(?P<FechaOSM>csts="\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d"|)(?P<Separacion4> )(?P<SRC>src="[^"]{1,20}")(?P<Separacion5> )(?P<Evento>evt="[^"]{1,25}")(?P<Separacion6> |)(?P<DataEvento>evtData="[^"]{0,500}"|)(?P<Separacion7> |)(?P<CSQ>CSQ="[^"]{0,6}"|)(?P<Separacion8> |)(?P<EstatusConexion>ConnectionStatus="[^"]{0,50}"|)(?P<Separacion9> |)(?P<Bateria>BattVol="[^"]{0,15}"|)(?P<Separacion10> |)(?P<EstatusPower>PowerStatus="[^"]{0,80}"|)(?P<Separacion11> |)(?P<ActividadMovimiento>MovementActivity="[^"]{0,6}"|)(?P<Separacion12> |)(?P<GPS>gps="[^"]{0,100}"|)')
			self.dividida = self.patron.search(trama)
			#Arreglando los Elementos de la trama
			self.Dispositivo = str(self.dividida.group('Dispositivo')).replace('dt="','').replace('"','')
			self.Serial = str(self.dividida.group('Serial')).replace('sn="','').replace('"','')
			self.FechaDisp = str(self.dividida.group('FechaDisp')).replace('dts="','').replace('"','')
			self.FechaOSM = str(self.dividida.group('FechaOSM')).replace('csts="','').replace('"','')
			self.Source = str(self.dividida.group('SRC')).replace('src="','').replace('"','')
			#self.Evento = str(self.dividida.group('Evento')).replace('evt="','').replace('"','')
			#self.DataEvento = str(self.dividida.group('DataEvento')).replace('evtData="','').replace('"','')
			#if str(self.DataEvento[:2]) == '0x':
			#	pass
			self.Signal = str(self.dividida.group('CSQ')).replace('CSQ="','').replace('"','')
			self.EstatusConexion = str(self.dividida.group('EstatusConexion')).replace('ConnectionStatus="','').replace('"','')
			self.EstatusPower = str(self.dividida.group('EstatusPower')).replace('PowerStatus="','').replace('"','')
			self.ActividadMovimiento = str(self.dividida.group('ActividadMovimiento')).replace('MovementActivity="','').replace('"','')
			self.GPS = str(self.dividida.group('GPS')).replace('gps="','').replace('"','')
			#Agregando el prefijo al Abonado en caso de que lo tenga
			if int(prefijo) >= 1000:
				self.Serial = int(self.Serial) + int(prefijo)
			self.datosparaGUI = (str(self.Serial),self.Evento,self.DataEvento,'No Aplica',str(1),self.nombreformato,LaFecha.damefecha())
			self.datosparaBD = (str(trama),str(1),str(self.Serial),self.Evento,self.DataEvento,self.numprotocolo,'0',numpuerto,'0')
			#Insertar En Base de Datos
			ColaParaGuardar.append(self.datosparaBD)
			fila = 0
			columna = 0
			globalvar["listadetablas"]["tabla"+str(numpuerto)].insertRow(0)
			for item in self.datosparaGUI:
				texto = QTableWidgetItem(item)
				globalvar["listadetablas"]["tabla"+str(numpuerto)].setItem(fila,columna,texto)
				columna = columna + 1
			#Contamos la cantidad de columnas en la tabla
			if globalvar["listadetablas"]["tabla"+str(numpuerto)].rowCount() > 300:
				globalvar["listadetablas"]["tabla"+str(numpuerto)].removeRow(301)
			print self.dividida.groups()
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(self.dividida.groups())
		except Exception as exc:
			self.tramafail = trama + "Error al Tratar Protocolo, Chequea ErrorLOG"
			GuardarTramaObjeto.GuardarTXTFail(self.tramafail)
			GuardarTramaObjeto.GuardarErrores(str(exc))
	def tratar(self,trama,numpuerto,prefijo):
		try:
			if trama.count('<msg ') > 1: #Si la trama viene con varios mensajes.
				tramadividida = trama.split(">",1)
				#Le quitamos el packet final a la trama y se lo colocamos al final a cada una que generemos
				tramadividida[1] = tramadividida[1].replace('</packet>','')
				#Ahora pico todos los eventos por su <>
				listadeeventos = tramadividida[1].split(">")


				for i in listadeeventos:
					if i: #Que quede en la historia, Jean Carlos Garcia penso esto!!!!! 14/03/2016 16:40pm
						i = i+'>'
						tr = tramadividida[0] + '>' + i + '</packet>'
						print tr
						if 'evt="DATA DTMF"' in tr:
							self.tratarDTMF(tr,numpuerto,prefijo)
						elif 'evt="OFF' in trama or 'evt="ON' in trama:
							self.tratarONOFFLX(trama,numpuerto,prefijo)
						elif 'evt="TEST' in tr:
							pass
						else:
							self.patron = re.compile('(?P<Inicio><packet.{5,100}>)(?P<IncioMsg><msg )(?P<Dispositivo>dt="..")(?P<Separacion1> )(?P<Serial>sn=".{0,20}")(?P<Separacion2> )(?P<FechaDisp>dts="\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d"|)(?P<Separacion3> |)(?P<FechaOSM>csts="\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d"|)(?P<Separacion4> )(?P<SRC>src="[^"]{1,20}")(?P<Separacion5> )(?P<Evento>evt="[^"]{1,25}")(?P<Separacion6> |)(?P<DataEvento>evtData="[^"]{0,500}"|)(?P<Separacion7> |)(?P<CSQ>CSQ="[^"]{0,6}"|)(?P<Separacion8> |)(?P<EstatusConexion>ConnectionStatus="[^"]{0,50}"|)(?P<Separacion9> |)(?P<Bateria>BattVol="[^"]{0,15}"|)(?P<Separacion10> |)(?P<EstatusPower>PowerStatus="[^"]{0,80}"|)(?P<Separacion11> |)(?P<ActividadMovimiento>MovementActivity="[^"]{0,6}"|)(?P<Separacion12> |)(?P<GPS>gps="[^"]{0,100}"|)')
							self.dividida = self.patron.search(tr)
							#Arreglando los Elementos de la trama
							self.Dispositivo = str(self.dividida.group('Dispositivo')).replace('dt="','').replace('"','')
							self.Serial = str(self.dividida.group('Serial')).replace('sn="','').replace('"','')
							self.FechaDisp = str(self.dividida.group('FechaDisp')).replace('dts="','').replace('"','')
							self.FechaOSM = str(self.dividida.group('FechaOSM')).replace('csts="','').replace('"','')
							self.Source = str(self.dividida.group('SRC')).replace('src="','').replace('"','')
							self.Evento = str(self.dividida.group('Evento')).replace('evt="','').replace('"','')
							self.DataEvento = str(self.dividida.group('DataEvento')).replace('evtData="','').replace('"','')
							if str(self.DataEvento[:2]) == '0x':
								pass
							self.Signal = str(self.dividida.group('CSQ')).replace('CSQ="','').replace('"','')
							self.EstatusConexion = str(self.dividida.group('EstatusConexion')).replace('ConnectionStatus="','').replace('"','')
							self.EstatusPower = str(self.dividida.group('EstatusPower')).replace('PowerStatus="','').replace('"','')
							self.ActividadMovimiento = str(self.dividida.group('ActividadMovimiento')).replace('MovementActivity="','').replace('"','')
							self.GPS = str(self.dividida.group('GPS')).replace('gps="','').replace('"','')
							#Agregando el prefijo al Abonado en caso de que lo tenga
							if int(prefijo) >= 1000:
								self.Serial = int(self.Serial) + int(prefijo)
							self.datosparaGUI = (str(self.Serial),self.Evento,self.DataEvento,'No Aplica',str(1),self.nombreformato,LaFecha.damefecha())
							self.datosparaBD = (str(tr),str(1),str(self.Serial),self.Evento,self.DataEvento,self.numprotocolo,'0',numpuerto,'0')
							#Insertar En Base de Datos
							ColaParaGuardar.append(self.datosparaBD)
							fila = 0
							columna = 0
							globalvar["listadetablas"]["tabla"+str(numpuerto)].insertRow(0)
							for item in self.datosparaGUI:
								texto = QTableWidgetItem(item)
								globalvar["listadetablas"]["tabla"+str(numpuerto)].setItem(fila,columna,texto)
								columna = columna + 1
							#Contamos la cantidad de columnas en la tabla
							if globalvar["listadetablas"]["tabla"+str(numpuerto)].rowCount() > 300:
								globalvar["listadetablas"]["tabla"+str(numpuerto)].removeRow(301)
							print self.dividida.groups()
							#Guardar en el Log
							#print 'GUARDANDO LOG'
							GuardarTramaObjeto.GuardarTXTLog(self.dividida.groups())
				#Si es una trama que trae un solo evento entonces
			else:
				if 'evt="DATA DTMF"' in trama:
					self.tratarDTMF(trama,numpuerto,prefijo)
				elif 'evt="OFF' in trama or 'evt="ON' in trama:
					self.tratarONOFFLX(trama,numpuerto,prefijo)
				elif 'evt="TEST' in trama:
					pass
				else:
					self.patron = re.compile('(?P<Inicio><packet.{5,100}>)(?P<IncioMsg><msg )(?P<Dispositivo>dt="..")(?P<Separacion1> )(?P<Serial>sn=".{0,20}")(?P<Separacion2> )(?P<FechaDisp>dts="\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d"|)(?P<Separacion3> |)(?P<FechaOSM>csts="\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d"|)(?P<Separacion4> )(?P<SRC>src="[^"]{1,20}")(?P<Separacion5> )(?P<Evento>evt="[^"]{1,25}")(?P<Separacion6> |)(?P<DataEvento>evtData="[^"]{0,500}"|)(?P<Separacion7> |)(?P<CSQ>CSQ="[^"]{0,6}"|)(?P<Separacion8> |)(?P<EstatusConexion>ConnectionStatus="[^"]{0,50}"|)(?P<Separacion9> |)(?P<Bateria>BattVol="[^"]{0,15}"|)(?P<Separacion10> |)(?P<EstatusPower>PowerStatus="[^"]{0,80}"|)(?P<Separacion11> |)(?P<ActividadMovimiento>MovementActivity="[^"]{0,6}"|)(?P<Separacion12> |)(?P<GPS>gps="[^"]{0,100}"|)')
					self.dividida = self.patron.search(trama)
					#Arreglando los Elementos de la trama
					self.Dispositivo = str(self.dividida.group('Dispositivo')).replace('dt="','').replace('"','')
					self.Serial = str(self.dividida.group('Serial')).replace('sn="','').replace('"','')
					self.FechaDisp = str(self.dividida.group('FechaDisp')).replace('dts="','').replace('"','')
					self.FechaOSM = str(self.dividida.group('FechaOSM')).replace('csts="','').replace('"','')
					self.Source = str(self.dividida.group('SRC')).replace('src="','').replace('"','')
					self.Evento = str(self.dividida.group('Evento')).replace('evt="','').replace('"','')
					self.DataEvento = str(self.dividida.group('DataEvento')).replace('evtData="','').replace('"','')
					if str(self.DataEvento[:2]) == '0x':
						pass
					self.Signal = str(self.dividida.group('CSQ')).replace('CSQ="','').replace('"','')
					self.EstatusConexion = str(self.dividida.group('EstatusConexion')).replace('ConnectionStatus="','').replace('"','')
					self.EstatusPower = str(self.dividida.group('EstatusPower')).replace('PowerStatus="','').replace('"','')
					self.ActividadMovimiento = str(self.dividida.group('ActividadMovimiento')).replace('MovementActivity="','').replace('"','')
					self.GPS = str(self.dividida.group('GPS')).replace('gps="','').replace('"','')
					#Agregando el prefijo al Abonado en caso de que lo tenga
					if int(prefijo) >= 1000:
						self.Serial = int(self.Serial) + int(prefijo)
					self.datosparaGUI = (str(self.Serial),self.Evento,self.DataEvento,'No Aplica',str(1),self.nombreformato,LaFecha.damefecha())
					self.datosparaBD = (str(trama),str(1),str(self.Serial),self.Evento,self.DataEvento,self.numprotocolo,'0',numpuerto,'0')
					#Insertar En Base de Datos
					ColaParaGuardar.append(self.datosparaBD)
					fila = 0
					columna = 0
					globalvar["listadetablas"]["tabla"+str(numpuerto)].insertRow(0)
					for item in self.datosparaGUI:
						texto = QTableWidgetItem(item)
						globalvar["listadetablas"]["tabla"+str(numpuerto)].setItem(fila,columna,texto)
						columna = columna + 1
					#Contamos la cantidad de columnas en la tabla
					if globalvar["listadetablas"]["tabla"+str(numpuerto)].rowCount() > 300:
						globalvar["listadetablas"]["tabla"+str(numpuerto)].removeRow(301)
					print self.dividida.groups()
					#Guardar en el Log
					GuardarTramaObjeto.GuardarTXTLog(self.dividida.groups())
		except Exception as exc:
			self.tramafail = trama + "Error al Tratar Protocolo, Chequea ErrorLOG"
			GuardarTramaObjeto.GuardarTXTFail(self.tramafail)
			GuardarTramaObjeto.GuardarErrores(str(exc))

XML_EBSobjeto = XML_EBS()

#Formatos de Receptores

class FormatoPrivado_MLR2(object):
	def __init__(self):
		self.nombre = "Evento Privado del MLR2"
		self.nombreformato = "MLR2"
		self.numprotocolo = '100'
		self.eregular = '....      0000 .  ..'
	def tratar(self,trama,numpuerto):
		#colaSIA1.append(trama)
		try:
			self.patron = re.compile('(?P<Identificador>.)(?P<Receptor>..)(?P<Linea>.)(?P<Separador>      )(?P<Abonado>....)(?P<Separador2> )(?P<T>.)(?P<Separador3>  )(?P<Evento>..)')
			self.dividida = self.patron.search(trama)
			self.datosparaGUI = (str(self.dividida.group('Abonado')),self.dividida.group('Evento'),'No Aplica','SP',self.dividida.group('Linea'),self.nombreformato,LaFecha.damefecha())
			self.datosparaBD = (trama,'0',self.dividida.group('Evento'),'REC'+self.dividida.group('Receptor')+' - LINE'+self.dividida.group('Linea'),self.numprotocolo,LaFecha.damefechadatetime(),'',self.dividida.group('Linea'),numpuerto)
			#Insertar En Base de Datos
			ColaParaGuardarSenalSistema.append(self.datosparaBD)
			fila = 0
			columna = 0
			globalvar["listadetablas"]["tabla"+str(numpuerto)].insertRow(0)
			for item in self.datosparaGUI:
				texto = QTableWidgetItem(item)
				globalvar["listadetablas"]["tabla"+str(numpuerto)].setItem(fila,columna,texto)
				columna = columna + 1
			#Contamos la cantidad de columnas en la tabla
			if globalvar["listadetablas"]["tabla"+str(numpuerto)].rowCount() > 300:
				globalvar["listadetablas"]["tabla"+str(numpuerto)].removeRow(301)
			print self.dividida.groups()
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(self.dividida.groups())
		except Exception as exc:
			self.tramafail = trama + "Error al Tratar Protocolo, Chequea ErrorLOG"
			GuardarTramaObjeto.GuardarTXTFail(self.tramafail)
			GuardarTramaObjeto.GuardarErrores(str(exc))

FormatoPrivado_MLR2objeto = FormatoPrivado_MLR2()

class FormatoPrivado_SystemIII(object):
	def __init__(self):
		self.nombre = "Evento Privado SystemIII"
		self.nombreformato = "SIII"
		self.numprotocolo = '101'
		self.eregular = '......\[#0000\|N......\]'

	def tratar(self,trama,numpuerto):
		#colaSIA1.append(trama)
		try:
			self.patron = re.compile('(?P<Identificador>.)(?P<Receptor>..)(?P<Linea>...)(?P<Separador>\[\#)(?P<Abonado>....)(?P<Separador2>\|)(?P<Evento>.......)')
			self.dividida = self.patron.search(trama)
			#Para quitarle los 0 a la izq a la linea, solcuion temporal mientras se arregla la bd
			self.linea = int(self.dividida.group("Linea"))
			self.dividida = self.patron.search(trama)
			self.datosparaGUI = (self.dividida.group('Abonado'),self.dividida.group('Evento'),'No Aplica','SP',self.dividida.group('Linea'),self.nombreformato,LaFecha.damefecha())
			self.datosparaBD = (trama,'0',self.dividida.group('Evento'),'REC'+self.dividida.group('Receptor')+' - LINE'+self.dividida.group('Linea'),self.numprotocolo,LaFecha.damefechadatetime(),'',self.dividida.group('Linea'),numpuerto)
			#Insertar En Base de Datos
			ColaParaGuardarSenalSistema.append(self.datosparaBD)
			fila = 0
			columna = 0
			globalvar["listadetablas"]["tabla"+str(numpuerto)].insertRow(0)
			for item in self.datosparaGUI:
				texto = QTableWidgetItem(item)
				globalvar["listadetablas"]["tabla"+str(numpuerto)].setItem(fila,columna,texto)
				columna = columna + 1
			#Contamos la cantidad de columnas en la tabla
			if globalvar["listadetablas"]["tabla"+str(numpuerto)].rowCount() > 300:
				globalvar["listadetablas"]["tabla"+str(numpuerto)].removeRow(301)
			print self.dividida.groups()
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(self.dividida.groups())
		except Exception as exc:
			self.tramafail = trama + "Error al Tratar Protocolo, Chequea ErrorLOG"
			GuardarTramaObjeto.GuardarTXTFail(self.tramafail)
			GuardarTramaObjeto.GuardarErrores(str(exc))

FormatoPrivado_SystemIIIobjeto = FormatoPrivado_SystemIII()

class FormatoPrivado_AES(object):
	def __init__(self):
		self.nombre = "Evento Privado AES INTELLINET"
		self.nombreformato = "AES"
		self.numprotocolo = '102'
		self.eregular = '1\d 0000 18 \D... .. ....'

	def tratar(self,trama,numpuerto,prefijo):
		#colaCIDMLR2.append(trama)
		try:
			self.patron = re.compile('(?P<Identificador>1)(?P<Linea>[0-9])(?P<Espacio> )(?P<Abonado>....)(?P<Espacio2> )(?P<ID>18)(?P<Espacio3> )(?P<Evento>\D...)(?P<Espacio4> )(?P<Particion>\d\d)(?P<Espacio5> )(?P<Nada>.)(?P<ZonaUsuario>\d{2,})')
			self.dividida = self.patron.search(trama)

			self.datosparaGUI = (str(self.Abonado),self.dividida.group('Evento'),self.dividida.group('ZonaUsuario'),self.dividida.group('Particion'),self.dividida.group('Linea'),self.nombreformato,LaFecha.damefecha())
			self.datosparaBD = (trama,'0',self.dividida.group('Evento'),'REC'+self.dividida.group('Identificador')+' - LINE'+self.dividida.group('Linea'),self.numprotocolo,LaFecha.damefechadatetime(),'',self.dividida.group('Linea'),numpuerto)
			#Insertar En Base de Datos
			ColaParaGuardarSenalSistema.append(self.datosparaBD)
			fila = 0
			columna = 0
			globalvar["listadetablas"]["tabla"+str(numpuerto)].insertRow(0)
			for item in self.datosparaGUI:
				texto = QTableWidgetItem(item)
				globalvar["listadetablas"]["tabla"+str(numpuerto)].setItem(fila,columna,texto)
				columna = columna + 1
			#Contamos la cantidad de columnas en la tabla
			if globalvar["listadetablas"]["tabla"+str(numpuerto)].rowCount() > 300:
				globalvar["listadetablas"]["tabla"+str(numpuerto)].removeRow(301)
			print self.dividida.groups()
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(self.dividida.groups())
		except Exception as exc:
			self.tramafail = trama + "Error al Tratar Protocolo, Chequea ErrorLOG"
			GuardarTramaObjeto.GuardarTXTFail(self.tramafail)
			GuardarTramaObjeto.GuardarErrores(str(exc))

FormatoPrivado_AESObjeto = FormatoPrivado_AES()