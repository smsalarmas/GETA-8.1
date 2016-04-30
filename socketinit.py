from servers import ThreadedTCPServer, ManejadorEBS, ManejadorSS365, ManejadorMLR2
from servers import FabricaEBSXML
from PyQt4 import QtCore
from globalvars import *
#from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ServerEndpoint
#from twisted.internet import reactor
import threading, time

class Socket(QtCore.QThread):  
	def __init__(self,num_puerto,receptor,prefijo,server,tab,parent):
		QtCore.QThread.__init__(self) 
		self.num_puerto = num_puerto
		self.receptor = receptor
		self.prefijo = prefijo
		self.tab = tab
		self.parent = parent
		self.serverhost = server
		print 'Arrancando Receptor por Socket'
	def run(self):
		print 'Identificando tipo de Receptor por Socket'
		if int(self.receptor) == 1:
			try:
				self.cliente = ManejadorMLR2(self,self.tab,str(self.serverhost),str(self.num_puerto),str(self.prefijo))
				self.cliente.Manejar()
				print 'Receptor Socket Asignado - SurGuard por Socket'
			except:
				self.parent.IconoCANCEL(self.tab)
		elif int(self.receptor) == 16:
			try:
				self.server = ThreadedTCPServer(('',int(self.num_puerto)), ManejadorEBS)
				PuertosCorriendoSOCKET[self.num_puerto] = self.server
				self.server.num_puerto = self.num_puerto
				self.server.prefijo = self.prefijo
				self.parent.IconoOK(self.tab)
				print 'Receptor Socket Asignado - EBS por ContactID Emulando SurGuard'
				self.server.serve_forever()
			except:
				self.parent.IconoCANCEL(self.tab)
		elif int(self.receptor) == 18:
			try:
				self.server = ThreadedTCPServer(('',int(self.num_puerto)), ManejadorSS365)
				PuertosCorriendoSOCKET[self.num_puerto] = self.server
				self.server.num_puerto = self.num_puerto
				self.server.prefijo = self.prefijo
				global listass365disprog
				self.server.listass365disprog = listass365disprog
				self.emit(QtCore.SIGNAL("openGet365Disprog"))

				self.parent.IconoOK(self.tab)
				print 'Receptor Socket Asignado - SS365 por ContactID'
				self.server.serve_forever()
			except:
				self.parent.IconoCANCEL(self.tab)

class SocketTwisted(QtCore.QObject):
	def __init__(self,reactor,num_puerto,receptor,prefijo,server,tab,parent): 
		QtCore.QObject.__init__(self)
		self.num_puerto = num_puerto
		self.receptor = receptor
		self.prefijo = prefijo
		self.reactor = reactor
		self.tab = tab
		self.parent = parent
		print 'Arrancando Receptor por Socket TW'

	def iniciar(self):
		print 'Identificando tipo de Receptor por Socket'
		if int(self.receptor) == 17:
			try:
				endpoint = self.reactor.listenTCP(int(self.num_puerto),FabricaEBSXML(self.num_puerto,self.prefijo))
				PuertosCorriendoTWISTED[self.num_puerto] = endpoint
				#endpoint = TCP4ServerEndpoint(reactor, int(self.num_puerto))
				#endpoint.listen(FabricaEBSXML(self.num_puerto,self.prefijo))
				self.parent.IconoOK(self.tab)
				print 'Receptor Socket Asignado - EBS por XML Bidireccional'
				global ReactorIniciado
				if ReactorIniciado == False:
				#	self.reactor = reactor.run()
					ReactorIniciado = True
			except:
				self.parent.IconoCANCEL(self.tab)
				print 'No se pudo asignar el puerto '+str(self.num_puerto)





