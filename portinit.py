import serial
from PyQt4 import QtCore
from receptores import Receptor_MLR2, Receptor_Sentinel, Receptor_AES, Receptor_DMP, Receptor_SEABOARDM1A,Receptor_SEABOARDM1AHEX, Receptor_VisorALARM, Receptor_MCDI, Receptor_SilentKnight
from globalvars import *

class Puertos(QtCore.QThread):
	def __init__(self,num_puerto,baudrate,bitesize,parity,stopbits,receptor,prefijo,tab,parent):
		QtCore.QThread.__init__(self)
		self.num_puerto = int(num_puerto)
		self.baudrate = int(baudrate)
		self.bitesize = eval(bitesize)
		self.parity = eval(parity)
		self.stopbits = eval(stopbits)
		self.receptor = int(receptor)
		self.prefijo = str(prefijo)
		self.tab = tab
		self.parent = parent
		self.parent.IconoOK(int(self.tab))
	def asignar(self):
		try:
			self.puerto = serial.Serial(self.num_puerto-1,self.baudrate,self.bitesize,self.parity,self.stopbits)
			PuertosCorriendoCOM[self.num_puerto] = self.puerto
			print "Puerto Asignado"
			print self.puerto
			self.parent.IconoOK(int(self.tab))
		except:
			self.parent.IconoCANCEL(int(self.tab))
			print 'No se pudo asignar el puerto ' + str(self.num_puerto)

	def run(self):
		self.asignar()
		try:
			if self.receptor == 1:
				MLR2 = Receptor_MLR2(self.num_puerto,self.prefijo)
				listadereceptores['MLR2'+str(self.num_puerto)] = MLR2
				print "Receptor Seleccionado Sur-Guard"
				listadereceptores['MLR2'+str(self.num_puerto)].proceso(self.puerto)
			elif self.receptor == 2:
				SENTINEL = Receptor_Sentinel(self.num_puerto,self.prefijo)
				listadereceptores['SENTINEL'+str(self.num_puerto)] = SENTINEL
				print "Receptor Seleccionado SENTINEL"
				listadereceptores['SENTINEL'+str(self.num_puerto)].proceso(self.puerto)
			elif self.receptor == 11:
				DMP = Receptor_DMP(self.num_puerto,self.prefijo)
				listadereceptores['DMP'+str(self.num_puerto)] = DMP
				print "Receptor Seleccionado DMP"
				listadereceptores['DMP'+str(self.num_puerto)].proceso(self.puerto)
			elif self.receptor == 3:
				AES = Receptor_AES(self.num_puerto,self.prefijo)
				listadereceptores['AES'+str(self.num_puerto)] = AES
				print "Receptor Seleccionado AES Intellinet"
				listadereceptores['AES'+str(self.num_puerto)].proceso(self.puerto)
			elif self.receptor == 9:
				VisorALARM = Receptor_VisorALARM(self.num_puerto,self.prefijo)
				listadereceptores['VisorALARM'+str(self.num_puerto)] = VisorALARM
				print "Receptor Seleccionado VisorALARM"
				listadereceptores['VisorALARM'+str(self.num_puerto)].proceso(self.puerto)
			elif self.receptor == 13:
				M1A = Receptor_SEABOARDM1A(self.num_puerto,self.prefijo)
				listadereceptores['SEABOARDM1A'+str(self.num_puerto)] = M1A
				print "Receptor Seleccionado SEABOARD M1A"
				listadereceptores['SEABOARDM1A'+str(self.num_puerto)].proceso(self.puerto)
			elif self.receptor == 14:
				M1AHEX = Receptor_SEABOARDM1AHEX(self.num_puerto,self.prefijo)
				listadereceptores['SEABOARDM1AHEX'+str(self.num_puerto)] = M1AHEX
				print "Receptor Seleccionado SEABOARD M1A"
				listadereceptores['SEABOARDM1AHEX'+str(self.num_puerto)].proceso(self.puerto)
			elif self.receptor == 15:
				MCDI = Receptor_MCDI(self.num_puerto,self.prefijo)
				listadereceptores['MCDI'+str(self.num_puerto)] = MCDI
				print "Receptor Seleccionado MCDI"
				listadereceptores['MCDI'+str(self.num_puerto)].proceso(self.puerto)
			elif self.receptor == 4:
				SilentKnight = Receptor_SilentKnight(self.num_puerto,self.prefijo)
				listadereceptores['SilentKnight'+str(self.num_puerto)] = SilentKnight
				print "Receptor Seleccionado SilentKnight"
				listadereceptores['SilentKnight'+str(self.num_puerto)].proceso(self.puerto)

		except:
			print 'No se pudo comenzar la escucha, verifica que el puerto ' + str(self.num_puerto) + ' esta disponible'