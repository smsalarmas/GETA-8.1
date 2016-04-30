import os
#os.system("color 1f")
#os.system("title Consola 365Receiver                           ##NO CERRAR##")
from PyQt4.QtGui import *
from PyQt4 import QtCore
import sys
from maingui import MainWindow
from check import LicCheck
from openinfo import AvisodeApertura
from globalvars import Modo
import threading
from remote import Remote

def main():
	print ('Receptor de Senales de Alarma Version 1.65')
	Lic = LicCheck()
	if Lic == True:
		if Modo != None:
			t = threading.Thread(target=AvisodeApertura,args=[Lic])
			t.setDaemon(False)
			t.start()

			#AvisodeApertura(Lic)
			app = QApplication(sys.argv)
			import qt4reactor
			qt4reactor.install()
			from twisted.internet import reactor
			#app.setStyle(QStyleFactory.create("plastique"))
			w = MainWindow(reactor)
			#Retornamos en BD 'No hay BD' en caso de que no se consiga la BD
			#Si el receptor esta en MODO de BD. Para que no muestre nunca la 
			#Ventana.

			bd = w.IniciarReceptores()
			w.show()
			a = Remote(w)
			a.Iniciar()
			if bd == 'No hay BD':
				pass
			else:

				reactor.run()
				#sys.exit(app.exec_())

	else:
		AvisodeApertura(Lic)
		pass
 

main()







