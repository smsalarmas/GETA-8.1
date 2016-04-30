#!/usr/bin/env python
import SocketServer
import threading
import re

class ManejadorOperadores(SocketServer.BaseRequestHandler):

	def handle(self):
		self.data = 'vacia'
		print "Conectado", self.client_address
		while len(self.data):
			self.data = self.request.recv(1024)
			print self.data

		print "Cliente Desconectado", self.client_address
		self.request.close()

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	pass
