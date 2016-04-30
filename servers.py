#!/usr/bin/env python
import SocketServer
import threading
from protocolos import *
from guardartrama import *
from twisted.internet.protocol import Factory, Protocol
import re
from bd import BasedeDatos
import socket



class ManejadorEBS(SocketServer.BaseRequestHandler):
	def identificar(self,trama,numpuerto,prefijo):
		self.terminal = ''
		self.heartbeat = '1011           @    '
		self.ack = '\x06'
		self.numpuerto = numpuerto
		if re.match(self.heartbeat,trama):
			print 'heartbeat recibido'
			#GuardarTramaObjeto.GuardarTXTOk(trama)
		elif re.match(FormatoPrivado_MLR2objeto.eregular,trama):
			print FormatoPrivado_MLR2objeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			FormatoPrivado_MLR2objeto.tratar(trama,self.numpuerto)
		elif re.match(ContactID_SurGuardobjeto.eregular,trama):
			print ContactID_SurGuardobjeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			ContactID_SurGuardobjeto.tratar(trama,self.numpuerto,prefijo)
		elif re.match(Sia3_MLR2objeto.eregular,trama):
			print Sia3_MLR2objeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			Sia3_MLR2objeto.tratar(trama,self.numpuerto,prefijo)
		elif re.match(Sia1_MLR2objeto.eregular,trama):
			print Sia1_MLR2objeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			Sia1_MLR2objeto.tratar(trama,self.numpuerto,prefijo)
		elif re.match(Sia2_MLR2objeto.eregular,trama):
			print Sia2_MLR2objeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			Sia2_MLR2objeto.tratar(trama,self.numpuerto,prefijo)
		elif re.match(SiaLevel1_1_SurGuardobjeto.eregular,trama):
			print SiaLevel1_1_SurGuardobjeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			SiaLevel1_1_SurGuardobjeto.tratar(trama,self.numpuerto,prefijo)
		elif re.match(SiaLevel1_2_SurGuardobjeto.eregular,trama):
			print SiaLevel1_2_SurGuardobjeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			SiaLevel1_2_SurGuardobjeto.tratar(trama,self.numpuerto,prefijo)
		elif re.match(CuatromasDos_MLR2objeto.eregular,trama):
			print CuatromasDos_MLR2objeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			CuatromasDos_MLR2objeto.tratar(trama,self.numpuerto,prefijo)
		else:
			GuardarTramaObjeto.GuardarTXTFail(trama)

	def handle(self):
		self.trama = 'vacia'
		numpuerto = self.server.num_puerto
		prefijo = self.server.prefijo
		print "Cliente Conectado", self.client_address
		while len(self.trama):
			self.trama = self.request.recv(1024)
			print self.trama + ' - OK'
			self.trama = self.trama.replace("","")
			self.request.send("\x06")
			self.identificar(self.trama, numpuerto, prefijo)

		print "Cliente Desconectado", self.client_address
		self.request.close()

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	pass

#############################################################################

class ManejadorEBSXML(Protocol):
	def connectionMade(self):
		# self.factory was set by the factory's default buildProtocol:
		print 'Conectado a EBS'
		self.transport.write('<?xml version="1.0" encoding="UTF-8"?><xml_al>')
		#self.factory.clients.append(self)
	def dataReceived(self,trama):
		if trama.count('<packet sq=') > 1:
			tramas = trama.split('</packet>')
			for trama in tramas:
				trama = trama+'</packet>'
				self.heartbeat = '<?xml version="1.0" encoding="UTF-8"?><xml_cs>'
				print trama + ' - OK'
				trama = trama.replace('\r','')
				trama = trama.replace('\n','')
				sq = re.search('packet sq="(.+?)"',trama)
				if sq:
					sq = sq.group(1)
					self.transport.write('<msg command="commit" sq="%s"/></xml_al>'%sq)
					self.numpuerto = self.factory.numpuerto
					self.prefijo = self.factory.prefijo
					if re.match(self.heartbeat,trama):
						print 'heartbeat recibido'
						self.transport.write('<?xml version="1.0" encoding="UTF-8"?><xml_al>')
					elif re.match(XML_EBSobjeto.eregular,trama):
						print XML_EBSobjeto.nombre
						#Guardar en el Log
						GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
						GuardarTramaObjeto.GuardarTXTOk(trama)
						XML_EBSobjeto.tratar(trama,self.numpuerto,self.prefijo)
		else:
			self.heartbeat = '<?xml version="1.0" encoding="UTF-8"?><xml_cs>'
			print trama + ' - OK'
			trama = trama.replace('\r','')
			trama = trama.replace('\n','')
			sq = re.search('packet sq="(.+?)"',trama)
			if sq:
				sq = sq.group(1)
				self.transport.write('<msg command="commit" sq="%s"/></xml_al>'%sq)
				self.numpuerto = self.factory.numpuerto
				self.prefijo = self.factory.prefijo
				if re.match(self.heartbeat,trama):
					print 'heartbeat recibido'
					self.transport.write('<?xml version="1.0" encoding="UTF-8"?><xml_al>')
				elif re.match(XML_EBSobjeto.eregular,trama):
					print XML_EBSobjeto.nombre
					#Guardar en el Log
					GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
					GuardarTramaObjeto.GuardarTXTOk(trama)
					XML_EBSobjeto.tratar(trama,self.numpuerto,self.prefijo)

	def connectionLost(self, reason):
		print "Lost a client!"
		#self.factory.clients.remove(self)

class FabricaEBSXML(Factory):
	# This will be used by the default buildProtocol to create new protocols:
	protocol = ManejadorEBSXML 

	def stopFactory(self):
		protocolo.transport.loseConnection()

	def __init__(self,numpuerto,prefijo):
		self.numpuerto = numpuerto
		self.prefijo = prefijo


########################################################################

class ManejadorSS365(SocketServer.BaseRequestHandler):
	def identificar(self,trama,numpuerto,prefijo,idcliente):
		self.terminal = ''
		self.heartbeat = '1011           @    '
		self.ack = '\x06'
		self.numpuerto = numpuerto
		if re.match(ContactID_SS365objeto.eregular,trama):
			print ContactID_SS365objeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			ContactID_SS365objeto.tratar(trama,self.numpuerto,prefijo,idcliente)
		else:
			GuardarTramaObjeto.GuardarTXTFail(trama)


	def handle(self):
		self.trama = 'vacia'
		numpuerto = self.server.num_puerto
		prefijo = self.server.prefijo
		listass365disprog = self.server.listass365disprog
		print "Cliente Conectado", self.client_address
		while len(self.trama):

			self.trama = self.request.recv(1024)
			print self.trama + ' - OK'
			self.trama = self.trama.replace("","")
			self.tramadiv = self.trama.split(',')
			self.trama = self.tramadiv[0]
			self.idcliente = self.tramadiv[1]
			self.patron = re.compile('(?P<Identificador>5)(?P<Receptor>\d\d)(?P<Linea>[0-9a-zA-Z]{1,3})(?P<Espacio> )(?P<ID>18)(?P<Espacio1> )(?P<Abonado>[^ ]{1,20})(?P<Espacio2> )(?P<Evento>[^ ]{1,20})(?P<Espacio3> )(?P<Particion>[^ ]{1,20})(?P<Espacio4> )(?P<ZonaUsuario>[^ ]{1,20})')
			self.dividida = self.patron.search(self.trama)
			zonausuario = self.dividida.group("ZonaUsuario")
			cuentadisp = str(self.idcliente)+','+str(zonausuario)
			Borrardelista = False
			if cuentadisp in listass365disprog:
				bd = BasedeDatos()
				bd.Conectar()
				cuentazona = cuentadisp.split(',')
				cuenta = cuentadisp[0]
				zona = cuentazona[1]
				bd.Borrar("DELETE FROM t365_SS365Disprog WHERE id_cliente = ? and zona = ?",[str(cuenta),str(zona)])
				self.request.send("Desprog")
				Borrardelista = True
			if Borrardelista == True:
				listass365disprog.remove(cuentadisp)
			else:
				self.request.send("\x06")
			self.identificar(self.trama, numpuerto, prefijo,self.idcliente)


		print "Cliente Desconectado", self.client_address
		self.request.close()


class ManejadorMLR2(QtCore.QObject):
	def __init__(self,parent,tab,serverhost,num_puerto,prefijo):
		QtCore.QObject.__init__(self)
		self.numpuerto = num_puerto
		self.prefijo = prefijo
		self.serverhost = serverhost
		self.parent = parent
		self.tab = tab

	def identificar(self,trama,numpuerto,prefijo):
		self.terminal = ''
		self.heartbeatMLR2 = '1011           @    '
		self.heartbeatSYSTEMIII = '1.....           @    '
		self.ack = '\x06'
		self.numpuerto = numpuerto
		if re.match(self.heartbeatMLR2,trama):
			print 'heartbeat recibido'
			#GuardarTramaObjeto.GuardarTXTOk(trama)
		elif re.match(self.heartbeatSYSTEMIII,trama):
			print 'heartbeat recibido'
			#GuardarTramaObjeto.GuardarTXTOk(trama)
		elif re.match(FormatoPrivado_MLR2objeto.eregular,trama):
			print FormatoPrivado_MLR2objeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			FormatoPrivado_MLR2objeto.tratar(trama,self.numpuerto)
		elif re.match(FormatoPrivado_SystemIIIobjeto.eregular,trama):
			print FormatoPrivado_SystemIIIobjeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			FormatoPrivado_SystemIIIobjeto.tratar(trama,self.numpuerto)
		elif re.match(ContactID_SurGuardobjeto.eregular,trama):
			print ContactID_SurGuardobjeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(self.trama)
			ContactID_SurGuardobjeto.tratar(trama,self.numpuerto,prefijo)
		elif re.match(Sia3_MLR2objeto.eregular,trama):
			print Sia3_MLR2objeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			Sia3_MLR2objeto.tratar(trama,self.numpuerto,prefijo)
		elif re.match(Sia1_MLR2objeto.eregular,trama):
			print Sia1_MLR2objeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			Sia1_MLR2objeto.tratar(trama,self.numpuerto,prefijo)
		elif re.match(Sia2_MLR2objeto.eregular,trama):
			print Sia2_MLR2objeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			Sia2_MLR2objeto.tratar(trama,self.numpuerto,prefijo)
		elif re.match(SiaLevel1_1_SurGuardobjeto.eregular,trama):
			print SiaLevel1_1_SurGuardobjeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			SiaLevel1_1_SurGuardobjeto.tratar(trama,self.numpuerto,prefijo)
		elif re.match(SiaLevel1_2_SurGuardobjeto.eregular,trama):
			print SiaLevel1_2_SurGuardobjeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			SiaLevel1_2_SurGuardobjeto.tratar(trama,self.numpuerto,prefijo)
		elif re.match(CuatromasDos_MLR2objeto.eregular,trama):
			print CuatromasDos_MLR2objeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			CuatromasDos_MLR2objeto.tratar(trama,self.numpuerto,prefijo)
		else:
			GuardarTramaObjeto.GuardarTXTFail(trama)
	def Manejar(self):
		self.trama = 'vacia'
		self.conexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.conexion.connect((str(self.serverhost),int(self.numpuerto))) 
		self.parent.parent.IconoOK(self.tab)

		print "Cliente Conectado"
		while len(self.trama):
			self.trama = self.conexion.recv(1024)
			print self.trama + ' - OK'
			self.trama = self.trama.replace("","")
			self.conexion.send("\x06")
			self.identificar(self.trama,self.numpuerto,self.prefijo)
		print "Desconectado del Server SurGuard"
		self.conexion.close()
		del self.conexion
		time.sleep(10)
		print 'Intentando Reconexion al Server SurGuard en 10 Segundos'
		self.Manejar()


		

