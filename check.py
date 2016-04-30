#Importamos el modulo para archivos INI
from ConfigParser import ConfigParser
#Importamos Desencriptador XOR Pycrypto
from Crypto.Cipher import XOR
import base64
#Importamos el modulo xxmc
from getxxmc import xxmx

def LicCheck():
	config = ConfigParser()
	config.read("conf/config.ini")
	LicCif = config.get('CUENTA', 'Lic')
	contrasena = base64.b64decode('MjAxMDE3MzMtOTYwOTkyNg==')
	PASSWORD = XOR.new(str(contrasena))
	try:
		#Por si da algun error en la decodificacion
		LicDecif = PASSWORD.decrypt(base64.b64decode(str(LicCif)))
	except:
		LicDecif = None
	if str(xxmx) == str(LicDecif):
		return True
	else:
		if LicDecif == None:
			print "Contacte con el Administrador del Software. Error 2 [LICENCIA. ERROR DE LICENCIA]"
		else:
			print "Contacte con el Administrador del Software. Error 1 [LICENCIA. VIOLACION DE LICENCIA]"
		return False

def LicCheckRemote():
	config = ConfigParser()
	config.read("conf/config.ini")
	LicCif = config.get('CUENTA', 'Lic')
	contrasena = base64.b64decode('MjAxMDE3MzMtOTYwOTkyNg==')
	PASSWORD = XOR.new(str(contrasena))
	try:
		#Por si da algun error en la decodificacion
		LicDecif = PASSWORD.decrypt(base64.b64decode(str(LicCif)))
	except:
		LicDecif = None
	if str(xxmx) == str(LicDecif):
		return True
	else:
		return False

def BDCheck():
	config = ConfigParser()
	config.read("conf/config.ini")
	ModoCif = config.get('CUENTA', 'Modo')
	contrasena = base64.b64decode('MjAxMDE3MzMtOTYwOTkyNg==')
	PASSWORD = XOR.new(str(contrasena))
	try:
		#Por si da algun error en la decodificacion
		Modo = PASSWORD.decrypt(base64.b64decode(str(ModoCif)))
		if Modo == '1':
			return Modo
		elif Modo == '2':
			return Modo
	except:
		print "Contacte con el Administrador del Software. Error 3 [MODO]"
		Modo = None
		return Modo
