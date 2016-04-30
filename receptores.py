# -*- coding: utf-8 -*-
from protocolos import *

#PUERTO SERIAL

class Receptor_MLR2(object):
	def __init__(self,numpuerto,prefijo):
		self.terminal = ''
		self.heartbeatMLR2 = '1011           @    '
		self.heartbeatSYSTEMIII = '1.....           @    '
		self.ack = '\x06'
		self.trama = ''
		self.numpuerto = numpuerto
		#Prefijo es para agregar al numero una suma de ese numero al Abonado
		#Que llegue, como en el caso de MC24 con los PIMA
		#Si llega 0001, debe agregarse como 4001
		self.prefijo = prefijo
	def identificar(self,trama):
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
			ContactID_SurGuardobjeto.tratar(trama,self.numpuerto,self.prefijo)
		elif re.match(Sia3_MLR2objeto.eregular,trama):
			print Sia3_MLR2objeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			Sia3_MLR2objeto.tratar(trama,self.numpuerto,self.prefijo)
		elif re.match(Sia1_MLR2objeto.eregular,trama):
			print Sia1_MLR2objeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			Sia1_MLR2objeto.tratar(trama,self.numpuerto,self.prefijo)
		elif re.match(Sia2_MLR2objeto.eregular,trama):
			print Sia2_MLR2objeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			Sia2_MLR2objeto.tratar(trama,self.numpuerto,self.prefijo)
		elif re.match(SiaLevel1_1_SurGuardobjeto.eregular,trama):
			print SiaLevel1_1_SurGuardobjeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			SiaLevel1_1_SurGuardobjeto.tratar(trama,self.numpuerto,self.prefijo)
		elif re.match(SiaLevel1_2_SurGuardobjeto.eregular,trama):
			print SiaLevel1_2_SurGuardobjeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			SiaLevel1_2_SurGuardobjeto.tratar(trama,self.numpuerto,self.prefijo)
		elif re.match(CuatromasDos_MLR2objeto.eregular,trama):
			print CuatromasDos_MLR2objeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			CuatromasDos_MLR2objeto.tratar(trama,self.numpuerto,self.prefijo)
		else:
			GuardarTramaObjeto.GuardarTXTFail(trama)


	def proceso(self,puerto):
		#DetenerPuertos = False
		try:
			while True:
				self.caracter = puerto.read()
				#print self.caracter
				self.trama = self.trama + self.caracter
				if self.caracter == self.terminal:
					puerto.write(self.ack)
					print self.trama + ' - OK'
					self.trama = self.trama.replace('','')
					self.identificar(self.trama)
					self.trama = ''
		except Exception as exc:
			print 'Puerto ' + str(self.numpuerto) + ' Detenido'
			GuardarTramaObjeto.GuardarErrores(str(exc))

class Receptor_Sentinel(object):
	def __init__(self,numpuerto,prefijo):
		self.terminal = '\r'
		self.terminalemulandosurgard = ''
		self.heartbeat = '1011            @     '
		self.ack = '\x06'
		self.trama = ''
		self.numpuerto = numpuerto
		#Prefijo es para agregar al numero una suma de ese numero al Abonado
		#Que llegue, como en el caso de MC24 con los PIMA
		#Si llega 0001, debe agregarse como 4001
		self.prefijo = prefijo
	def identificar(self,trama):
		if re.match(self.heartbeat,trama):
			print 'heartbeat recibido'
			#GuardarTramaObjeto.GuardarTXTOk(trama)
		elif re.match(NewPaf_Sentinel1objeto.eregular,trama):
			print NewPaf_Sentinel1objeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			NewPaf_Sentinel1objeto.tratar(trama,self.numpuerto,self.prefijo)
		elif re.match(NewPaf_Sentinel2objeto.eregular,trama):
			print NewPaf_Sentinel2objeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			NewPaf_Sentinel2objeto.tratar(trama,self.numpuerto,self.prefijo)
		elif re.match(Sia_Sentinelobjeto.eregular,trama):
			print Sia_Sentinelobjeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			Sia_Sentinelobjeto.tratar(trama,self.numpuerto,self.prefijo)
		elif re.match(ContactID_Sentinelobjeto.eregular,trama):
			print ContactID_Sentinelobjeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			ContactID_Sentinelobjeto.tratar(trama,self.numpuerto,self.prefijo)
		else:
			GuardarTramaObjeto.GuardarTXTFail(trama)

	def proceso(self,puerto):
		try:
			while True:
				self.caracter = puerto.read()
				#print self.caracter
				self.trama = self.trama + self.caracter
				if self.caracter == self.terminal or self.caracter == self.terminalemulandosurgard:
					puerto.write(self.ack)
					self.trama = self.trama.replace('\n','')
					self.trama = self.trama.replace('\r','')
					self.trama = self.trama.replace('','')
					print self.trama + ' - OK'
					self.identificar(self.trama)
					self.trama = ''
		except Exception as exc:
			print 'Puerto ' + str(self.numpuerto) + ' Detenido'
			GuardarTramaObjeto.GuardarErrores(str(exc))
class Receptor_AES(object):
	def __init__(self,numpuerto,prefijo):
		self.terminal = '\r'
		self.heartbeat = '00 OKAY @ '
		self.ack = '\x06'
		self.trama = ''
		self.numpuerto = numpuerto
		#Prefijo es para agregar al numero una suma de ese numero al Abonado
		#Que llegue, como en el caso de MC24 con los PIMA
		#Si llega 0001, debe agregarse como 4001
		self.prefijo = prefijo
	def identificar(self,trama):
		if re.match(self.heartbeat,trama):
			print 'heartbeat recibido'
		if re.match(FormatoPrivado_AESObjeto.eregular,trama):
			print FormatoPrivado_AESObjeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			FormatoPrivado_AESObjeto.tratar(trama,self.numpuerto,self.prefijo)
		if re.match(ContactID_AESobjeto.eregular,trama):
			print ContactID_AESobjeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			ContactID_AESobjeto.tratar(trama,self.numpuerto,self.prefijo)
		else:
			GuardarTramaObjeto.GuardarTXTFail(trama)

	def proceso(self,puerto):
		try:
			while True:
				self.caracter = puerto.read()
				#Para omitir en la trama cuando llege (ln) no lo guardo en la trama
				ln = '\n'
				if self.caracter != ln:
					self.trama = self.trama + self.caracter
				if self.caracter == self.terminal:
					puerto.write(self.ack)
					self.trama = self.trama.replace(self.terminal,'')
					print self.trama + ' - OK'
					self.identificar(self.trama)
					self.trama = ''
		except Exception as exc:
			print 'Puerto ' + str(self.numpuerto) + ' Detenido'
			GuardarTramaObjeto.GuardarErrores(str(exc))

class Receptor_DMP(object):
	def __init__(self,numpuerto,prefijo):
		self.terminal = '\r'
		self.heartbeat = '1-    0 S99 '
		self.ack = '\x06'
		self.trama = ''
		self.numpuerto = numpuerto
		#Prefijo es para agregar al numero una suma de ese numero al Abonado
		#Que llegue, como en el caso de MC24 con los PIMA
		#Si llega 0001, debe agregarse como 4001
		self.prefijo = prefijo
	def identificar(self,trama):
		if re.match(self.heartbeat,trama):
			print 'heartbeat recibido'
			#GuardarTramaObjeto.GuardarTXTOk(trama)
		elif re.match(ContactID_DMPobjeto.eregular,trama):
			print ContactID_DMPobjeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			ContactID_DMPobjeto.tratar(trama,self.numpuerto,self.prefijo)
		elif re.match(DD_DMPobjeto.eregular,trama):
			print DD_DMPobjeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			DD_DMPobjeto.tratar(trama,self.numpuerto,self.prefijo)
		else:
			GuardarTramaObjeto.GuardarTXTFail(trama)

	def proceso(self,puerto):
		try:
			while True:
				self.caracter = puerto.read()
				self.trama = self.trama + self.caracter
				self.trama = self.trama.replace('\r','')
				if self.caracter == self.terminal:
					puerto.write(self.ack)
					print self.trama + ' - OK'
					self.identificar(self.trama)
					self.trama = ''
		except Exception as exc:
			print 'Puerto ' + str(self.numpuerto) + ' Detenido'
			GuardarTramaObjeto.GuardarErrores(str(exc))

class Receptor_SEABOARDM1A(object):
	def __init__(self,numpuerto,prefijo):
		self.terminal = ''  #El manual dice que termina con DC4 pero el que conocemos llega con CR de terminal
		self.terminal2 = '\r'
		self.heartbeat = 'NOEXISTEELHEARTBEAT'
		self.ack = '\x06'
		self.trama = ''
		self.numpuerto = numpuerto
		#Prefijo es para agregar al numero una suma de ese numero al Abonado
		#Que llegue, como en el caso de MC24 con los PIMA
		#Si llega 0001, debe agregarse como 4001
		self.prefijo = prefijo
	def identificar(self,trama):
		if re.match(self.heartbeat,trama):
			print 'heartbeat recibido'
			#GuardarTramaObjeto.GuardarTXTOk(trama)
		elif re.match(SeaBoard_M1Aobjeto.eregular,trama):
			print SeaBoard_M1Aobjeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			SeaBoard_M1Aobjeto.tratar(trama,self.numpuerto,self.prefijo)
		else:
			GuardarTramaObjeto.GuardarTXTFail(trama)

	def proceso(self,puerto):
		try:
			while True:
				self.caracter = puerto.read()
				self.trama = self.trama + self.caracter
				self.trama = self.trama.replace('','')
				self.trama = self.trama.replace('\r','')
				if self.caracter == self.terminal or self.caracter == self.terminal2:
					puerto.write(self.ack)
					print self.trama + ' - OK'
					self.identificar(self.trama)
					self.trama = ''
		except Exception as exc:
			print 'Puerto ' + str(self.numpuerto) + ' Detenido'
			GuardarTramaObjeto.GuardarErrores(str(exc))

class Receptor_SEABOARDM1AHEX(object):
	#Se crea un nuevo Receptor para el SeaBoard M1A Cuando recibe parte del abonado en
	#HEX porque no se pueden separar con EREG ya que son exactamente iguales.
	def __init__(self,numpuerto,prefijo):
		self.terminal = ''
		self.terminal2 = '\r'
		self.heartbeat = 'NOEXISTEELHEARTBEAT'
		self.ack = '\x06'
		self.trama = ''
		self.numpuerto = numpuerto
		#Prefijo es para agregar al numero una suma de ese numero al Abonado
		#Que llegue, como en el caso de MC24 con los PIMA
		#Si llega 0001, debe agregarse como 4001
		self.prefijo = prefijo
	def identificar(self,trama):
		if re.match(self.heartbeat,trama):
			print 'heartbeat recibido'
			#GuardarTramaObjeto.GuardarTXTOk(trama)
		elif re.match(SeaBoard_M1AHEXobjeto.eregular,trama):
			print SeaBoard_M1AHEXobjeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			SeaBoard_M1AHEXobjeto.tratar(trama,self.numpuerto,self.prefijo)
		else:
			GuardarTramaObjeto.GuardarTXTFail(trama)

	def proceso(self,puerto):
		try:
			while True:
				self.caracter = puerto.read()
				self.trama = self.trama + self.caracter
				self.trama = self.trama.replace('','')
				self.trama = self.trama.replace('\r','')
				if self.caracter == self.terminal or self.caracter == self.terminal2:
					puerto.write(self.ack)
					print self.trama + ' - OK'
					self.identificar(self.trama)
					self.trama = ''
		except Exception as exc:
			print 'Puerto ' + str(self.numpuerto) + ' Detenido'
			GuardarTramaObjeto.GuardarErrores(str(exc))

class Receptor_VisorALARM(object):
	def __init__(self,numpuerto,prefijo):
		self.terminal = ''
		self.heartbeat1 = '....           @    ' #Emulando Surguard o Radionics6500
		self.heartbeat2 = '......           @    ' #Emulando Surguard
		self.heartbeat3 = '00 OKAY @ ' #Emulando Ademco685
		self.ack = '\x06'
		self.trama = ''
		self.numpuerto = numpuerto
		#Prefijo es para agregar al numero una suma de ese numero al Abonado
		#Que llegue, como en el caso de MC24 con los PIMA
		#Si llega 0001, debe agregarse como 4001
		self.prefijo = prefijo
	def identificar(self,trama):
		if re.match(self.heartbeat1,trama):
			print 'heartbeat recibido'
			#GuardarTramaObjeto.GuardarTXTOk(trama)
		elif re.match(self.heartbeat2,trama):
			print 'heartbeat recibido'
			#GuardarTramaObjeto.GuardarTXTOk(trama)
		elif re.match(self.heartbeat3,trama):
			print 'heartbeat recibido'
			#GuardarTramaObjeto.GuardarTXTOk(trama)
		elif re.match(ContactID1_VisorAlarmobjeto.eregular,trama): #Cuando Emula Surgard
			print ContactID1_VisorAlarmobjeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(self.trama)
			ContactID1_VisorAlarmobjeto.tratar(trama,self.numpuerto,self.prefijo)
		elif re.match(ContactID2_VisorAlarmobjeto.eregular,trama): #Cuando Emula Ademco685 que es igual al CID del AES
			print ContactID2_VisorAlarmobjeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			ContactID2_VisorAlarmobjeto.tratar(trama,self.numpuerto,self.prefijo)
		elif re.match(ContactID3_VisorAlarmobjeto.eregular,trama): #Cuando Emula Ademco685 que es igual al CID del AES
			print ContactID3_VisorAlarmobjeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			ContactID3_VisorAlarmobjeto.tratar(trama,self.numpuerto,self.prefijo)
		else:
			GuardarTramaObjeto.GuardarTXTFail(trama)


	def proceso(self,puerto):
		#DetenerPuertos = False
		try:
			while True:
				self.caracter = puerto.read()
				#print self.caracter
				#Para omitir en la trama si llega (ln) no lo guardo en la trama
				#Es un hex20 o un hex0A que manda este receptor como inicio de la trama
				obviar = '\n'
				if self.caracter != obviar:
					self.trama = self.trama + self.caracter
				if self.caracter == self.terminal:
					puerto.write(self.ack)
					#Eliminamos el espacio que envia el Radionics al Comienzo
					if self.trama[0] == ' ':
						self.trama = self.trama.replace(' ','',1) 
					print self.trama + ' - OK'
					self.trama = self.trama.replace('','')
					self.identificar(self.trama)
					self.trama = ''
		except Exception as exc:
			print 'Puerto ' + str(self.numpuerto) + ' Detenido'
			GuardarTramaObjeto.GuardarErrores(str(exc))

class Receptor_MCDI(object):
	def __init__(self,numpuerto,prefijo):
		self.terminalMCDI = '\r'
		self.terminalSurGuard = ''
		self.heartbeatMCDI = '@'
		self.heartbeatSurGuard = '1011           @    '
		self.ack = '\x06'
		self.trama = ''
		self.numpuerto = numpuerto
		#Prefijo es para agregar al numero una suma de ese numero al Abonado
		#Que llegue, como en el caso de MC24 con los PIMA
		#Si llega 0001, debe agregarse como 4001
		self.prefijo = prefijo
	def identificar(self,trama):
		if re.match(self.heartbeatMCDI,trama):
			print 'heartbeat recibido'
			#GuardarTramaObjeto.GuardarTXTOk(trama)
		if re.match(self.heartbeatSurGuard,trama):
			print 'heartbeat recibido'
			#GuardarTramaObjeto.GuardarTXTOk(trama)
		elif re.match(ContactID_MCDIobjeto.eregular,trama):
			print ContactID_MCDIobjeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(self.trama)
			ContactID_MCDIobjeto.tratar(trama,self.numpuerto,self.prefijo)
		elif re.match(CuatromasDos_MCDIobjeto.eregular,trama):
			print CuatromasDos_MCDIobjeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			CuatromasDos_MCDIobjeto.tratar(trama,self.numpuerto,self.prefijo)
		elif re.match(ModemSia_MCDIobjeto.eregular,trama):
			print ModemSia_MCDIobjeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			ModemSia_MCDIobjeto.tratar(trama,self.numpuerto,self.prefijo)
		elif re.match(ModemSia_MCDIAdemco685objeto.eregular,trama):
			print ModemSia_MCDIAdemco685objeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			ModemSia_MCDIAdemco685objeto.tratar(trama,self.numpuerto,self.prefijo)
		#OJO#
		#Aqui comienzan las tramas del MCDI cuando emula SurGuard
		elif re.match(FormatoReceptor_MLR2objeto.eregular,trama):
			print FormatoReceptor_MLR2objeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			FormatoReceptor_MLR2objeto.tratar(trama,self.numpuerto,self.prefijo)
		elif re.match(ContactID_SurGuardobjeto.eregular,trama):
			print ContactID_SurGuardobjeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(self.trama)
			ContactID_SurGuardobjeto.tratar(trama,self.numpuerto,self.prefijo)
		elif re.match(Sia3_MLR2objeto.eregular,trama):
			print Sia3_MLR2objeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			Sia3_MLR2objeto.tratar(trama,self.numpuerto,self.prefijo)
		elif re.match(Sia1_MLR2objeto.eregular,trama):
			print Sia1_MLR2objeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			Sia1_MLR2objeto.tratar(trama,self.numpuerto,self.prefijo)
		elif re.match(Sia2_MLR2objeto.eregular,trama):
			print Sia2_MLR2objeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			Sia2_MLR2objeto.tratar(trama,self.numpuerto,self.prefijo)
		elif re.match(SiaLevel1_1_SurGuardobjeto.eregular,trama):
			print SiaLevel1_1_SurGuardobjeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			SiaLevel1_1_SurGuardobjeto.tratar(trama,self.numpuerto,self.prefijo)
		elif re.match(SiaLevel1_2_SurGuardobjeto.eregular,trama):
			print SiaLevel1_2_SurGuardobjeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			SiaLevel1_2_SurGuardobjeto.tratar(trama,self.numpuerto,self.prefijo)
		elif re.match(CuatromasDos_MLR2objeto.eregular,trama):
			print CuatromasDos_MLR2objeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			CuatromasDos_MLR2objeto.tratar(trama,self.numpuerto,self.prefijo)
		else:
			GuardarTramaObjeto.GuardarTXTFail(trama)


	def proceso(self,puerto):
		#DetenerPuertos = False
		try:
			while True:
				self.caracter = puerto.read()
				#print self.caracter
				self.trama = self.trama + self.caracter
				if self.caracter == self.terminalMCDI or self.caracter == self.terminalSurGuard:
					puerto.write(self.ack)
					self.trama = self.trama.replace('\r','')
					self.trama = self.trama.replace('\n','')
					self.trama = self.trama.replace('','')
					print self.trama + ' - OK'
					self.identificar(self.trama)
					self.trama = ''
		except Exception as exc:
			print 'Puerto ' + str(self.numpuerto) + ' Detenido'
			GuardarTramaObjeto.GuardarErrores(str(exc))
			
class Receptor_SilentKnight(object):
	def __init__(self,numpuerto,prefijo):
		self.terminal = '\r'
		self.heartbeat = 'DESCONOCIDO'
		self.ack = '\x06'
		self.trama = ''
		self.numpuerto = numpuerto
		#Prefijo es para agregar al numero una suma de ese numero al Abonado
		#Que llegue, como en el caso de MC24 con los PIMA
		#Si llega 0001, debe agregarse como 4001
		self.prefijo = prefijo
	def identificar(self,trama):
		if re.match(self.heartbeat,trama):
			print 'heartbeat recibido'
			#GuardarTramaObjeto.GuardarTXTOk(trama)
		elif re.match(ContactID_SilentKnightobjeto.eregular,trama):
			print ContactID_SilentKnightobjeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(self.trama)
			ContactID_SilentKnightobjeto.tratar(trama,self.numpuerto,self.prefijo)
		elif re.match(Sia2_SilentKnightobjeto.eregular,trama):
			print Sia2_SilentKnightobjeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			Sia2_SilentKnightobjeto.tratar(trama,self.numpuerto,self.prefijo)
		elif re.match(Sia1_SilentKnightobjeto.eregular,trama):
			print Sia1_SilentKnightobjeto.nombre
			#Guardar en el Log
			GuardarTramaObjeto.GuardarTXTLog(trama + ' - OK')
			GuardarTramaObjeto.GuardarTXTOk(trama)
			Sia1_SilentKnightobjeto.tratar(trama,self.numpuerto,self.prefijo)

		else:
			GuardarTramaObjeto.GuardarTXTFail(trama)

	def proceso(self,puerto):
		#DetenerPuertos = False
		try:
			while True:
				self.caracter = puerto.read()
				#print self.caracter
				self.trama = self.trama + self.caracter
				if self.caracter == self.terminal:
					puerto.write(self.ack)
					self.trama = self.trama.replace('\r','')
					self.trama = self.trama.replace('\n','')
					#Especial para el SilentKnight por toda la basura que llega
					if self.trama.find("#") != -1 or self.trama.find('\x05') == -1:
						self.trama = ''
						pass
					else:
						print self.trama + ' - OK'
						self.identificar(self.trama)
						self.trama = ''
		except Exception as exc:
			print 'Puerto ' + str(self.numpuerto) + ' Detenido'
			GuardarTramaObjeto.GuardarErrores(str(exc))
