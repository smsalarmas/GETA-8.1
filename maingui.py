from PyQt4.QtGui import *
from PyQt4 import QtCore
from portinit import Puertos
from socketinit import Socket, SocketTwisted
from searchports import serial_ports
import time
from bd import BasedeDatos
from globalvars import *
from guardartrama import GuardarTramaBD
from notifysmsa import NotifySMSA
import threading
from getss365disprog import GetSS365Disprog


class MainWindow(QMainWindow):
	def __init__(self,reactor):
		super(MainWindow,self).__init__()
		#Titulo y Tamano de la Ventana Principal
		self.setWindowTitle('365Receiver 1.65')
		self.setMinimumSize(623,468)
		self.setMaximumSize(623,468)
		#Icono de la ventna
		self.setWindowIcon(QIcon("icons/faviconredondo.png"))
		self.remoteprocess = None
		self.reactor = reactor
		#Layouts
		layoutv = QVBoxLayout()
		layouth = QHBoxLayout()

		#Label informacion y Label para el Logo
		#Label de Informacion
		Label = QLabel()
		Label.setText("")
		#Label para el Logo
		#Pintar Logo
		self.labellogo = QLabel()
		self.logo = QPixmap('icons/logo.png')
		self.labellogo.setPixmap(self.logo)

		#Crear Tabs
		self.Tab = QTabWidget()
		self.Tab.setMovable(True)

		#Asignar Layouts y Widgets
		layoutv.addLayout(layouth)
		layouth.addWidget(self.labellogo)
		layouth.addWidget(Label)
		layoutv.addWidget(self.Tab)

		#Crear CentralWidget a mano, anadir al layout, y decirle que es el centralwidget
		central_widget = QWidget()
		central_widget.setLayout(layoutv)
		self.setCentralWidget(central_widget)

		#QActioneptor')
		self.accionSalir = QAction('Salir', self)
		self.accionSalir.setStatusTip('Salir de la Aplicacion')
		self.accionSalir.setShortcut('Ctrl+X')
		self.accionSalir.setIcon(QIcon('icons/salir.png'))
		self.accionNuevoSerial = QAction('Nuevo Serial', self)
		self.accionNuevoSerial.setStatusTip('Nuevo Receptor Puerto Serial')
		self.accionNuevoSerial.setShortcut('Ctrl+C')
		self.accionNuevoSerial.setIcon(QIcon('icons/nuevo.png'))
		self.accionNuevoSocket = QAction('Nuevo Socket', self)
		self.accionNuevoSocket.setStatusTip('Nuevo Receptor Socket')
		self.accionNuevoSocket.setShortcut('Ctrl+S')
		self.accionNuevoSocket.setIcon(QIcon('icons/nuevosocket.png'))
		self.accionEditar = QAction('Editar', self)
		self.accionEditar.setStatusTip('Editar Receptores')
		self.accionEditar.setShortcut('Ctrl+E')
		self.accionEditar.setIcon(QIcon('icons/editar.png'))
		self.accionIniciar = QAction('Iniciar', self)
		self.accionIniciar.setStatusTip('Iniciar Receptores')
		self.accionIniciar.setShortcut('Ctrl+I')
		self.accionIniciar.setIcon(QIcon('icons/iniciar.png'))
		self.accionDetener = QAction('Detener', self)
		self.accionDetener.setStatusTip('Detener Receptores')
		self.accionDetener.setShortcut('Ctrl+D')
		self.accionDetener.setIcon(QIcon('icons/detener.png'))
		self.accionLimpiar = QAction('Limpiar', self)
		self.accionLimpiar.setStatusTip('Limpiar Listas')
		self.accionLimpiar.setShortcut('Ctrl+L')
		self.accionLimpiar.setIcon(QIcon('icons/limpiar.png'))

		#Botones


		#Crear y Asignar QActions a la ToolBar
		#Creandola
		self.toolbar = QToolBar(self)
		#self.toolbar.setStyleSheet("background: rgb(175,175,175)")
		#Indicandole donde saldra por defecto
		self.addToolBar(QtCore.Qt.LeftToolBarArea,self.toolbar)
		#Agregando los QActions
		self.toolbar.addAction(self.accionIniciar)
		self.toolbar.addAction(self.accionDetener)
		self.toolbar.addSeparator()
		self.toolbar.addAction(self.accionNuevoSerial)
		self.toolbar.addAction(self.accionNuevoSocket)
		self.toolbar.addAction(self.accionEditar)
		self.toolbar.addSeparator()
		self.toolbar.addAction(self.accionLimpiar)
		self.toolbar.addAction(self.accionSalir)

		#Barra de Estado
		self.statusbar = self.setStatusBar(QStatusBar())

		#Menu
		#menu = self.menuBar()
		#menu_archivo = menu.addMenu('&Archivo')
		#menu_archivo.addAction(self.accionSalir)

		#Conexiones
		#Conexion Limpiar Tablas
		self.connect(self.accionLimpiar, QtCore.SIGNAL("triggered()"), self.LimpiarTablas)
		self.connect(self.accionIniciar, QtCore.SIGNAL("triggered()"), self.IniciarReceptores)
		self.connect(self.accionDetener, QtCore.SIGNAL("triggered()"), self.DetenerReceptores)
		self.connect(self.accionSalir, QtCore.SIGNAL("triggered()"), self.exitEvent)

		self.connect(self.accionNuevoSerial, QtCore.SIGNAL("triggered()"), self.ReceptorNuevoSerial)
		self.connect(self.accionNuevoSocket, QtCore.SIGNAL("triggered()"), self.ReceptorNuevoSocket)
		self.connect(self.accionEditar, QtCore.SIGNAL("triggered()"), self.EditarReceptores)
		#Se crea el Objeto GuardarTrama pero no se inicia si no hay BD en la funcion Iniciar Recepores
		self.GuardarTramaBDObjeto = GuardarTramaBD()
		self.connect(self.GuardarTramaBDObjeto, QtCore.SIGNAL("signalNotifySMSA"), self.NotifySMSA)






		##################FUNCIONES PARA EL SYSTEM TRAY ICON#######################
		self.exitOnClose = False
		exit = QAction(QIcon("icons/faviconredondo.png"), "Cerrar Receptor", self)
		self.connect(exit, QtCore.SIGNAL("triggered()"), self.exitEvent)
		self.trayIcon = QSystemTrayIcon(QIcon("icons/faviconredondo.png"), self)
		menu = QMenu(self)
		menu.addAction(exit)
		self.trayIcon.setContextMenu(menu)
		self.connect(self.trayIcon, \
			QtCore.SIGNAL("activated(QSystemTrayIcon::ActivationReason)"), \
			self.trayIconActivated)
		self.trayIcon.show()
		self.trayIcon.showMessage("365Receiver Iniciando", "Espere un momento... \nBoton derecho para Menu" )
		self.trayIcon.setToolTip("365Receiver")


		self.HayBD = True
	def trayIconActivated(self, reason):
		if reason == QSystemTrayIcon.Context:
			self.trayIcon.contextMenu().show()
		elif reason == QSystemTrayIcon.Trigger:
			self.show()
			self.raise_()

	def closeEvent(self, event):
		if self.exitOnClose:
			self.trayIcon.hide()
			self.DetenerReceptores()
			del self.trayIcon
			#event.accept()
			try:
				self.reactor.stop()
			except:
				pass
			self.remoteprocess.scheduler.shutdown(wait=False)
			event.accept()
		else:
			self.hide()
			event.setAccepted(True)
			event.ignore()

	def exitEvent(self):
		self.exitOnClose = True

		self.close()

		################################################################################

	def IconoOK(self,index):
		self.Tab.setTabIcon(int(index),QIcon("icons/ok.png"))

	def IconoCANCEL(self,index):
		self.Tab.setTabIcon(int(index),QIcon("icons/cancel.png"))

	def NotifySMSA(self):
		#Variable para que el hilo de notifysmsa le envie el comando a SmsAlarmas
		#Para que busque en Base de datos
		#print "Notificando a SMSA"
		self.ConexionSMSA.Avisar = True

	def EjecutarGet365Disprog(self):

		self.disprog365 = GetSS365Disprog()
		self.disprog365.start()

	def BotonesCuandoInicia(self):
		self.accionNuevoSerial.setEnabled(False)
		self.accionIniciar.setEnabled(False)
		self.accionSalir.setEnabled(False)
		self.accionEditar.setEnabled(False)
		self.accionNuevoSocket.setEnabled(False)
		self.accionDetener.setEnabled(True)



	def BotonesCuandoPara(self):
		self.accionNuevoSerial.setEnabled(True)
		self.accionIniciar.setEnabled(True)
		self.accionSalir.setEnabled(True)
		self.accionEditar.setEnabled(True)
		self.accionNuevoSocket.setEnabled(True)
		self.accionDetener.setEnabled(False)


	def LimpiarTablas(self):
		for t in globalvar["listadetablas"]:
			globalvar["listadetablas"][t].clearContents()

	def IniciarReceptores(self):
		self.Modo = Modo
		if self.Modo == '1':
			self.HayBD = True
		elif self.Modo == '2':
			self.HayBD = False
		if self.Modo == "1":
			try:
				archivoconfiguracion = []
				print 'Buscando Receptores en la Base de Datos'
				#Variable self.HayBD para identificar si hay Base de Datos
				#Y arrancar en modo BD o Stand Alone.
				self.BD = BasedeDatos()
				self.BD.Conectar()
				print 'Conectado a la Base de Datos'
				#Arrancar el Hilo para Guardar Tramas en Base de Datos
				print 'Iniciando Proceso de Almacenamiento de Tramas Recibidas'
				self.GuardarTramaBDObjeto.start()
				#Me conecto a SMSAlarmas por el Socket para avisarle cuando me llego una trama busque en BD
				#Primero creo el Objeto
				#self.ConexionSMSA = NotifySMSA()
				#self.ConexionSMSA.Desconectar = False

				#Ahora me conecto
				#self.ConexionSMSA.start()

				#El objeto BD se crea en el archivo BD para manejar conexiones a Base de Datos
				self.BD.Seleccionar("select PortID, config, type, Port, idReceptor, orden, Status, prefijo, Server from t365_ConfigPortII where Status = 1")
				for row in self.BD.resultado:
					config = row.config.split(",")
					#Si es TIPO 1 que es Puerto Serial
					if row.type == 1:
						lista = [str(row.PortID),str(config[0]),str(nombresPySerial['Tamano'][config[2]]),str(nombresPySerial['Paridad'][config[1]]),str(nombresPySerial['Stop'][config[3]]),str(row.idReceptor),str(row.type),str(row.prefijo),'']
						archivoconfiguracion.append(lista)
					#Si es TIPO 2 que es SOCKET
					if row.type == 2:
						lista = [str(row.PortID),'','','','',str(row.idReceptor),str(row.type),str(row.prefijo),str(row.Server)]
						archivoconfiguracion.append(lista)
			except:
				print 'Contacte con el Administrador del Software, Error 4 [BD]'
				#Para detener la ventana
				return 'No hay BD'
		#print archivoconfiguracion		
		elif self.Modo == "2":
			print 'Receptor en modo Stand-Alone'
			archivoconfiguracion = open('conf/config.txt','r')
			#Creamos BD para que no explote cuando se le pasan los argumentos 
			# de la BD a las ventanas, mejor que hacer un if en cada llamada
			# a una ventana nueva
			self.BD = False
		for line in archivoconfiguracion:
			time.sleep(0.5)
			if type(line) == str:
				linea = line.split(",")
			else:
				linea = line
			#Si es un receptor por puerto Serial
			if int(linea[6]) == 1:
				#Crear Tabs y Tablas
				tab = QWidget()
				#Agrego a la lista para tener el orden de como se crearon los tab para acceder por el index
				tabla = QTableWidget()
				tabla.setShowGrid(False)
				tabla.verticalHeader().setVisible(False)
				tabla.setAlternatingRowColors(True)
				tabla.verticalHeader().setDefaultSectionSize(26)
				tabla.setSelectionMode(QAbstractItemView.NoSelection)
				layout = QVBoxLayout()
				globalvar["listadelayout"]["layout"+nombresreceptoresserial[linea[5].rstrip('\n')] + 'COM' + linea[0]] = layout
				globalvar["listadetablas"]["tabla"+str(linea[0])] = tabla
				globalvar["listadetabs"]["tab"+nombresreceptoresserial[linea[5].rstrip('\n')] + 'COM' + linea[0]] = tab
				#Asignando Tamano de la Tabla
				globalvar["listadetablas"]["tabla"+linea[0]].setRowCount(50)
				globalvar["listadetablas"]["tabla"+linea[0]].setColumnCount(7)
				globalvar["listadetablas"]["tabla"+linea[0]].setHorizontalHeaderLabels(("Abonado","Evento","Zona/Usuario","Particion","Linea","Formato","Fecha"))
				#Cambiando el Tamano a las primeras 4 Columnas
				globalvar["listadetablas"]["tabla"+linea[0]].setColumnWidth(0,60)
				globalvar["listadetablas"]["tabla"+linea[0]].setColumnWidth(1,60)
				globalvar["listadetablas"]["tabla"+linea[0]].setColumnWidth(2,80)
				globalvar["listadetablas"]["tabla"+linea[0]].setColumnWidth(3,60)
				globalvar["listadetablas"]["tabla"+linea[0]].setColumnWidth(4,60)
				globalvar["listadetablas"]["tabla"+linea[0]].setColumnWidth(5,60)
				globalvar["listadetablas"]["tabla"+linea[0]].setColumnWidth(6,143)
				#Le asignamos un nuevo TAB al QTabWidget Creado en la Clase Main Window con el Nombre del Receptor mas elCOM
				self.Tab.addTab(globalvar["listadetabs"]["tab"+nombresreceptoresserial[linea[5].rstrip('\n')] + 'COM' + linea[0]], nombresreceptoresserial[linea[5].rstrip('\n')] + ' ' + linea[0])
				listatabscreados.append(tab)
				ubicacion = listatabscreados.index(tab)
				globalvar["listadelayout"]["layout"+nombresreceptoresserial[linea[5].rstrip('\n')] + 'COM' + linea[0]].addWidget(globalvar["listadetablas"]["tabla"+linea[0]])
				globalvar["listadetabs"]["tab"+nombresreceptoresserial[linea[5].rstrip('\n')] + 'COM' + linea[0]].setLayout(globalvar["listadelayout"]["layout"+nombresreceptoresserial[linea[5].rstrip('\n')] + 'COM' + linea[0]])
				#Creamos los Receptores
				self.objeto = Puertos(linea[0],linea[1],linea[2],linea[3],linea[4],linea[5],linea[7].rstrip('\n'),ubicacion,self)
				globalvar["listadepuertosCOM"]["puerto"+str(linea[0])] = self.objeto
				#Descomentar sigueinte linea si queremos que arranquen de una los receptores
				globalvar["listadepuertosCOM"]["puerto"+str(linea[0])].start()
				self.BotonesCuandoInicia()
			#Si es un receptor por Socket
			elif int(linea[6]) == 2:
				#Crear Tabs y Tablas
				tab = QWidget()
				#Agrego a la lista para tener el orden de como se crearon los tab para acceder por el index
				tabla = QTableWidget()
				tabla.setShowGrid(False)
				tabla.verticalHeader().setVisible(False)
				tabla.setAlternatingRowColors(True)
				tabla.verticalHeader().setDefaultSectionSize(26)
				tabla.setSelectionMode(QAbstractItemView.NoSelection)
				layout = QVBoxLayout()
				globalvar["listadelayout"]["layout"+nombresreceptoressocket[linea[5].rstrip('\n')] + 'PORT' + linea[0]] = layout
				globalvar["listadetablas"]["tabla"+str(linea[0])] = tabla
				globalvar["listadetabs"]["tab"+nombresreceptoressocket[linea[5].rstrip('\n')] + 'PORT' + linea[0]] = tab
				#Asignando Tamano de la Tabla
				globalvar["listadetablas"]["tabla"+linea[0]].setRowCount(50)
				globalvar["listadetablas"]["tabla"+linea[0]].setColumnCount(7)
				globalvar["listadetablas"]["tabla"+linea[0]].setHorizontalHeaderLabels(("Abonado","Evento","Zona/Usuario","Particion","Linea","Formato","Fecha"))
				#Cambiando el Tamano a las primeras 4 Columnas
				globalvar["listadetablas"]["tabla"+linea[0]].setColumnWidth(0,60)
				globalvar["listadetablas"]["tabla"+linea[0]].setColumnWidth(1,60)
				globalvar["listadetablas"]["tabla"+linea[0]].setColumnWidth(2,80)
				globalvar["listadetablas"]["tabla"+linea[0]].setColumnWidth(3,60)
				globalvar["listadetablas"]["tabla"+linea[0]].setColumnWidth(4,60)
				globalvar["listadetablas"]["tabla"+linea[0]].setColumnWidth(5,60)
				globalvar["listadetablas"]["tabla"+linea[0]].setColumnWidth(6,143)
				#Le asignamos un nuevo TAB al QTabWidget Creado en la Clase Main Window con el Nombre del Receptor mas el Puerto
				self.Tab.addTab(globalvar["listadetabs"]["tab"+nombresreceptoressocket[linea[5].rstrip('\n')] + 'PORT' + linea[0]], nombresreceptoressocket[linea[5].rstrip('\n')] + ' ' + linea[0])
				listatabscreados.append(tab)
				ubicacion = listatabscreados.index(tab)
				globalvar["listadelayout"]["layout"+nombresreceptoressocket[linea[5].rstrip('\n')] + 'PORT' + linea[0]].addWidget(globalvar["listadetablas"]["tabla"+linea[0]])
				globalvar["listadetabs"]["tab"+nombresreceptoressocket[linea[5].rstrip('\n')] + 'PORT' + linea[0]].setLayout(globalvar["listadelayout"]["layout"+nombresreceptoressocket[linea[5].rstrip('\n')] + 'PORT' + linea[0]])
				#Creamos los Receptores
				if int(linea[5]) != 17: #Si no es el EBS con XML que utiliza twisted y tiene que correr en el hilo principal se va a los QThreads
					self.objeto = Socket(linea[0],linea[5],linea[6],linea[8].rstrip('\n'),ubicacion,self)
					globalvar["listadepuertosSOCKET"]["puerto"+str(linea[0])] = self.objeto
					globalvar["listadepuertosSOCKET"]["puerto"+str(linea[0])].start()
					if int(linea[5]) == 18: #Arranco 365Disprog
						self.connect(self.objeto, QtCore.SIGNAL("openGet365Disprog"),self.EjecutarGet365Disprog)
				else:
				#	print 'Estoy por aqui'
					self.objeto = SocketTwisted(self.reactor,linea[0],linea[5],linea[6],linea[8].rstrip('\n'),ubicacion,self)
					globalvar["listadepuertosSOCKET"]["puerto"+str(linea[0])] = self.objeto
					self.objeto.iniciar()
				self.BotonesCuandoInicia()
		


	def DetenerReceptores(self):
		global listatabscreados
		listatabscreados = []
		for t in PuertosCorriendoTWISTED:
			PuertosCorriendoTWISTED[t].stopListening()
		#DetenerPuertos == True
		try:
			self.disprog365.detener = True
		except:
			pass

		for r in PuertosCorriendoCOM:
			PuertosCorriendoCOM[r].close()
		for s in PuertosCorriendoSOCKET:
			#Aqui hay que leer bien porque funciona pero no aparece asi en la
			#documentacion
			PuertosCorriendoSOCKET[s].shutdown()
			PuertosCorriendoSOCKET[s].socket.close()
		self.BotonesCuandoPara()
		#Creo Variables para almacenar nombres de Tabs, Tablas y Layout Existentes
		#Porque no puedo borrarlos dentro del FOR donde le hago hide()
		#Da un error porque estoy haciendo un bucle sobre un elemento que estoy
		#Cambiando por eso lo hago por fuera
		tablasaborrar = []
		tabsaborrar = []
		layoutaborrar = []
		#Eliminamos las Tablas
		for l in globalvar['listadetablas']:
			globalvar['listadetablas'][l].setParent = None
			globalvar['listadetablas'][l].hide()
			tablasaborrar.append(l)
		#Eliminamos las Tablas Almacenadas en las Variables Globales
		for lb in tablasaborrar:
			del globalvar['listadetablas'][lb]
		#Eliminamos Los Layout
		for la in globalvar['listadelayout']:
			globalvar['listadelayout'][la].setParent = None
			#globalvar['listadelayout'][la].hide()
			layoutaborrar.append(la)
		#Eliminamos los Layout Almacenadas en las Variables Globales
		for lab in layoutaborrar:
			del globalvar['listadelayout'][lab]
		#Eliminamos Los Tabs
		#Contamos los Tabs con count()
		numtabs = self.Tab.count()
		for t in range(numtabs):
			self.Tab.removeTab(0)
		#Ahora guardamos en una lista todos los Objetos dentro de la Variable Global
		#Lista de Tabs
		for tb in globalvar['listadetabs']:
			tabsaborrar.append(tb)
		#Eliminamos los Tabs Almacenadas en las Variables Globales
		for tb in tabsaborrar:
			del globalvar['listadetabs'][tb]
		#Verificamos si estamos trabajando con SMSA para Desconectarnos
		if self.HayBD == True:
			#Nos desconectamos de SMSAlarmas
			#self.ConexionSMSA.Desconectar = True
			pass

		
	def ReceptorNuevoSerial(self):
		self.Qnuevo = QnuevoreceptorSerial(self,self.BD,self.HayBD)
		self.Qnuevo.show()

	def ReceptorNuevoSocket(self):
		self.Qnuevo = QnuevoreceptorSocket(self,self.BD,self.HayBD)
		self.Qnuevo.show()

	def EditarReceptores(self):
		self.QEditar = Qeditarreceptores(self,self.BD,self.HayBD)
		self.QEditar.show()


class QerrorPuerto(QDialog):
	def __init__(self, parent):
		QDialog.__init__(self, parent)
		self.setWindowTitle('ADVERTENCIA')
		contenedor = QVBoxLayout()
		self.setLayout(contenedor)

		labelerror = QLabel()
		labelerror.setText('Puerto NO disponible')
 
		btnSalir = QPushButton("Entendido",None)
		contenedor.addWidget(labelerror)
		contenedor.addWidget(btnSalir)

		self.connect(btnSalir, QtCore.SIGNAL("clicked()"), self.Entendido)
 
	def Entendido(self):
		self.close()


class QnuevoreceptorSerial(QDialog):
	def __init__(self, parent, BD, HayBD):
		#super(Qnuevoreceptor,self).__init__()
		QDialog.__init__(self, parent)
		#Recibo la Conexion a la BD
		self.BD = BD
		#Recibo si hay o no BD
		self.HayBD = HayBD

		#Descomentar Abajo si queremos los puertos disponibles solamente
		#Pero es lento y da problemas al editar cuando un com no esta abierto
		#Obvio comentar abajo donde se colocan 100 COM en caso de habilitar 
		#la busqueda de los disponibles
		#puertos = serial_ports()
		puertos = []
		for i in range(101):
			puertos.append('COM'+str(i))
		self.setWindowTitle('Agregar Receptor Serial')
		#Labels
		self.LabelPuertoSerial = QLabel()
		self.LabelPuertoSerial.setText('Puerto')
		self.LabelVelocidad = QLabel()
		self.LabelVelocidad.setText('Velocidad')
		self.LabelTamano = QLabel()
		self.LabelTamano.setText('Tamano')
		self.LabelParidad = QLabel()
		self.LabelParidad.setText('Paridad')
		self.LabelStop = QLabel()
		self.LabelStop.setText('StopBit')
		self.LabelReceptorSerial = QLabel()
		self.LabelReceptorSerial.setText('Receptor')
		self.LabelPrefijo = QLabel()
		self.LabelPrefijo.setText("Prefijo")



		#ComboBox
		self.ComboPuerto = QComboBox()
		self.ComboPuerto.addItems(puertos)
		self.ComboVelocidad = QComboBox()
		self.ListaVelocidad = ('50', '75', '110', '134', '150', '200', '300', '600', '1200', '1800', '2400', '4800', '9600', '19200', '38400', '57600', '115200')
		self.ComboVelocidad.addItems(self.ListaVelocidad)
		self.ComboTamano = QComboBox()
		# sorted(diccionario.keys()) devuelve el una lista de las claves del diccionario
		# list(diccionario.keys()) devuelve la lista tambien pero no ordenada
		self.ListaTamano = sorted(nombresPySerial['Tamano'].keys())
		self.ComboTamano.addItems(self.ListaTamano)
		self.ComboParidad = QComboBox()
		self.ListaParidad = sorted(nombresPySerial['Paridad'].keys())
		self.ComboParidad.addItems(self.ListaParidad)
		self.ComboStop = QComboBox()
		self.ListaStop = sorted(nombresPySerial['Stop'].keys())
		self.ComboStop.addItems(self.ListaStop)
		self.ComboReceptorSerial = QComboBox()
		self.diccionarioReceptores= {'SUR-GARD': 1, 'SENTINEL': 2, 'AES': 3, 'DMP': 11, 'VisorALARM' : 9, 'M1A' : 13, 'M1AHEX' : 14, 'MCDI' : 15, 'SilentKnight' : 4}
		self.listaReceptores=('SUR-GARD', 'SENTINEL', 'DMP', 'AES','VisorALARM', 'M1A', 'M1AHEX', 'MCDI', 'SilentKnight')
		self.ComboReceptorSerial.addItems(self.listaReceptores)
		self.ComboPrefijo = QComboBox()
		self.ListaPrefijo = ['0','1000','2000','3000','4000','5000','6000','7000','8000','9000']
		self.ComboPrefijo.addItems(self.ListaPrefijo)


		#Botones
		self.BotonAdd = QPushButton("Agregar")
		self.BotonCancel = QPushButton("Cancelar")


		#Creando Layouts e Asignandoles Ubicacion entre ellos
		self.layouthorizontal = QHBoxLayout()
		self.setLayout(self.layouthorizontal)
		self.layoutvertical1 = QVBoxLayout()
		self.layoutvertical2 = QVBoxLayout()
		self.layoutvertical3 = QVBoxLayout()
		self.layouthorizontal.addLayout(self.layoutvertical1)
		self.layouthorizontal.addLayout(self.layoutvertical2)
		self.layouthorizontal.addLayout(self.layoutvertical3)

		#Acomodando los Widgets en Layouts
		#Primera Fila de Labels

		self.layoutvertical1.addWidget(self.LabelPuertoSerial)
		self.layoutvertical1.addWidget(self.LabelVelocidad)
		self.layoutvertical1.addWidget(self.LabelTamano)
		self.layoutvertical1.addWidget(self.LabelParidad)
		self.layoutvertical1.addWidget(self.LabelStop)
		self.layoutvertical1.addWidget(self.LabelReceptorSerial)
		self.layoutvertical1.addWidget(self.LabelPrefijo)

		#Segunda Fila de Combos

		self.layoutvertical2.addWidget(self.ComboPuerto)
		self.layoutvertical2.addWidget(self.ComboVelocidad)
		self.layoutvertical2.addWidget(self.ComboTamano)
		self.layoutvertical2.addWidget(self.ComboParidad)
		self.layoutvertical2.addWidget(self.ComboStop)
		self.layoutvertical2.addWidget(self.ComboReceptorSerial)
		self.layoutvertical2.addWidget(self.ComboPrefijo)


		#Tercera Fila Botones
		self.layoutvertical3.addWidget(self.BotonAdd)
		self.layoutvertical3.addWidget(self.BotonCancel)

		#Conexiones
		self.connect(self.BotonAdd, QtCore.SIGNAL("clicked()"), self.AgregarReceptor)
		self.connect(self.BotonCancel, QtCore.SIGNAL("clicked()"), self.Cancelar)

	def AgregarReceptor(self):
		#Tomando los Datos de la Interfaz
		vpuerto=self.ComboPuerto.currentText().replace("COM","")
		vvelocidad= self.ComboVelocidad.currentText()
		vtamano=str(self.ComboTamano.currentText())
		vparidad=str(self.ComboParidad.currentText())
		vstop=str(self.ComboStop.currentText())
		vreceptor=str(self.ComboReceptorSerial.currentText())
		vprefijo=str(self.ComboPrefijo.currentText())
		
		if self.HayBD == True: 
			#Conocer cuantos Receptores hay en Base de Datos
			self.BD.Seleccionar("select PortID from t365_ConfigPortII")
			cantidadreceptores = 0
			#Ahora voy a contar los receptores que estan en la base de datos para agregar el numero
			#del orden del receptor, campo para saber como se van a mostrar en orden aunque todavia
			#no esta funcionando eso, pero igual aprovecho y me traigo en una lista los puertos
			#Usados por otros receptores para dar un error en caso de que ya este ese puerto
			puertoscomutilizados = []
			for row in self.BD.resultado:
				cantidadreceptores = cantidadreceptores + 1
				puertoscomutilizados.append(row[0])
			#Ahora comprobamos si el puerto seleccionado no esta en la lista
			if vpuerto in puertoscomutilizados:
				#Abriendo Mensaje de Error
				ventanaerrorpuerto = QerrorPuerto(self).exec_()
			else:
				#Guardando en la Base de Datos
				configbd = str(vvelocidad+','+vparidad+','+vtamano+','+vstop)
				self.datosparaBD = (str(vpuerto),str(vreceptor),str(configbd),1,0,str(self.diccionarioReceptores[vreceptor]),1,cantidadreceptores+1,1,1,int(vprefijo))
				self.BD.Insertar("INSERT INTO t365_ConfigPortII(PortID,Descrip,Config,type,Port,idReceptor,Heartbeat,orden,Status,geta,prefijo)values(?,?,?,?,?,?,?,?,?,?,?);",self.datosparaBD)
				#Cerrando la Ventana
				self.close()
		elif self.HayBD == False:
			#Me traigo una lista de los puertos utilizados para dar error en caso de que 
			#Ya exista
			archivoconfiguracion = open('conf/config.txt','r')
			puertoscomutilizados = []
			for line in archivoconfiguracion:
				linea = line.split(",")
				puertoscomutilizados.append(linea[0])
			archivoconfiguracion.close()
			#Ahora comprobamos si el puerto seleccionado no esta en la lista
			if str(vpuerto) in puertoscomutilizados:
				#Abriendo Mensaje de Error
				ventanaerrorpuerto = QerrorPuerto(self).exec_()
			else:
				#Guardando en el archivo de Texto
				self.configtxt=open('conf/config.txt','a')
				self.configtxt.write(str(vpuerto)+","+str(vvelocidad)+","+nombresPySerial['Tamano'][vtamano]+","+nombresPySerial['Paridad'][vparidad]+","+nombresPySerial['Stop'][vstop]+","+str(self.diccionarioReceptores[vreceptor])+","+"1"+","+str(vprefijo)+"\n")
				self.configtxt.close()
				self.close()
	def Cancelar(self):
		self.close()


class QnuevoreceptorSocket(QDialog):
	def __init__(self, parent, BD, HayBD):
		#super(Qnuevoreceptor,self).__init__()
		QDialog.__init__(self, parent)
		#Recibo la conexion a la BD
		self.BD = BD
		#Recibo informacion si hay BD
		self.HayBD = HayBD

		self.setWindowTitle('Agregar Receptor Socket')
		self.setMinimumSize(300,100)
		self.setMaximumSize(300,100)
		#Labels
		self.LabelDireccionSocket = QLabel()
		self.LabelDireccionSocket.setText("Direccion")
		self.LabelPuertoSocket = QLabel()
		self.LabelPuertoSocket.setText('Puerto')
		self.LabelReceptorSocket = QLabel()
		self.LabelReceptorSocket.setText('Receptor')
		self.LabelPrefijo = QLabel()
		self.LabelPrefijo.setText('Prefijo')



		#ComboBox
		self.ComboReceptorSocket = QComboBox()
		self.diccionarioReceptores= {'EBSCID': 16,'EBSXML':17,'SS365':18, 'SUR-GARD': 1}
		self.listaReceptores=['EBSCID','EBSXML','SS365','SUR-GARD']
		self.ComboReceptorSocket.addItems(self.listaReceptores)
		self.ComboPrefijo = QComboBox()
		self.ListaPrefijo = ['0','1000','2000','3000','4000','5000','6000','7000','8000','9000']
		self.ComboPrefijo.addItems(self.ListaPrefijo)


		#Botones
		self.BotonAdd = QPushButton("Agregar")
		self.BotonCancel = QPushButton("Cancelar")

		#Spin
		self.SpinPuerto = QSpinBox()
		self.SpinPuerto.setMaximum(9999)

		#LineEdit
		self.DireccionSocket = QLineEdit()


		#Creando Layouts e Asignandoles Ubicacion entre ellos
		self.layouthorizontal = QHBoxLayout()
		self.setLayout(self.layouthorizontal)
		self.layoutvertical1 = QVBoxLayout()
		self.layoutvertical2 = QVBoxLayout()
		self.layoutvertical3 = QVBoxLayout()
		self.layouthorizontal.addLayout(self.layoutvertical1)
		self.layouthorizontal.addLayout(self.layoutvertical2)
		self.layouthorizontal.addLayout(self.layoutvertical3)

		#Acomodando los Widgets en Layouts
		#Primera Fila de Labels
		self.layoutvertical1.addWidget(self.LabelDireccionSocket)
		self.layoutvertical1.addWidget(self.LabelPuertoSocket)
		self.layoutvertical1.addWidget(self.LabelReceptorSocket)
		self.layoutvertical1.addWidget(self.LabelPrefijo)

		

		#Segunda Fila de Combos
		self.layoutvertical2.addWidget(self.DireccionSocket)
		self.layoutvertical2.addWidget(self.SpinPuerto)
		self.layoutvertical2.addWidget(self.ComboReceptorSocket)
		self.layoutvertical2.addWidget(self.ComboPrefijo)

		#Tercera Fila Botones
		self.layoutvertical3.addWidget(self.BotonAdd)
		self.layoutvertical3.addWidget(self.BotonCancel)

		#Conexiones
		self.connect(self.BotonAdd, QtCore.SIGNAL("clicked()"), self.AgregarReceptor)
		self.connect(self.BotonCancel, QtCore.SIGNAL("clicked()"), self.Cancelar)

	def AgregarReceptor(self):
		#Tomando los Valores de la interfaz
		Server = str(self.DireccionSocket.text())
		vpuerto=self.SpinPuerto.value()
		vreceptor=str(self.ComboReceptorSocket.currentText())
		vprefijo=str(self.ComboPrefijo.currentText())
		if self.HayBD == True:
			#Conocer cuantos hay en Base de Datos
			self.BD.Seleccionar("select Port from t365_ConfigPortII")
			cantidadreceptores = 0
			#Ahora voy a contar los receptores que estan en la base de datos para agregar el numero
			#del orden del receptor, campo para saber como se van a mostrar en orden aunque todavia
			#no esta funcionando eso, pero igual aprovecho y me traigo en una lista los puertos
			#Usados por otros receptores para dar un error en caso de que ya este ese puerto
			puertossocketutilizados = []
			for row in self.BD.resultado:
				cantidadreceptores = cantidadreceptores + 1
				puertossocketutilizados.append(row[0])
			#Ahora comprobamos si el puerto seleccionado no esta en la lista
			if vpuerto in puertossocketutilizados:
				#Abriendo Mensaje de Error
				ventanaerrorpuerto = QerrorPuerto(self).exec_()
			else:
				self.datosparaBD = (vpuerto,vreceptor,vpuerto,2,vpuerto,self.diccionarioReceptores[vreceptor],1,cantidadreceptores+1,1,1,int(vprefijo),str(Server))
				self.BD.Insertar("INSERT INTO t365_ConfigPortII(PortID,Descrip,Config,type,Port,idReceptor,Heartbeat,orden,Status,geta,prefijo,server)values(?,?,?,?,?,?,?,?,?,?,?,?); ",self.datosparaBD)
				#Cerrando la Ventana
				self.close()

		elif self.HayBD == False:

			#Guardando en el Archivo de Texto
			#Me traigo una lista de los puertos utilizados para dar error en caso de que 
			#Ya exista
			archivoconfiguracion = open('conf/config.txt','r')
			puertossocketutilizados = []
			for line in archivoconfiguracion:
				linea = line.split(",")
				puertossocketutilizados.append(linea[0])
			archivoconfiguracion.close()
			#Ahora comprobamos si el puerto seleccionado no esta en la lista
			if str(vpuerto) in puertossocketutilizados:
				#Abriendo Mensaje de Error
				ventanaerrorpuerto = QerrorPuerto(self).exec_()
			else:
				#Guardando en el Archivo de Texto
				self.configtxt=open('conf/config.txt','a')
				self.configtxt.write(str(vpuerto)+","+","+","+","+","+str(self.diccionarioReceptores[vreceptor])+","+"2"+","+str(vprefijo)+","+str(Server)+"\n")
				self.configtxt.close()
				self.close()

	def Cancelar(self):
		self.close()

class Qeditarreceptores(QDialog):
	def __init__(self, parent, BD, HayBD):
		#super(Qnuevoreceptor,self).__init__()
		QDialog.__init__(self, parent)
		#Recibo la Conexion a la BD
		self.BD = BD
		#Recibo si hay BD
		self.HayBD = HayBD

		self.setWindowTitle('Editar Receptores')
		self.setMinimumSize(300,500)
		self.setMaximumSize(300,500)
		#Labels
		self.LabelListaReceptores = QLabel()
		self.LabelListaReceptores.setText('Lista de Receptores')

		self.BotonCancelar = QPushButton('Cancelar')

		#Agregando el Boton y Ubicandolo
		layout = QHBoxLayout()
		layoutWidget = QWidget(self)
		layoutWidget.setLayout(layout)
		layoutWidget.setGeometry(100,450,100,50)
		layout.addWidget(self.BotonCancelar)
		layoutWidget.show()


		#TreeWidget
		self.ListWidgetReceptores = QListWidget(self)
		self.ListWidgetReceptores.setGeometry(20,35,260,400)
		self.ListWidgetReceptores.show()

		#Llamar a la funcion Listar
		self.ListarReceptores()

		#Conexiones
		self.connect(self.BotonCancelar, QtCore.SIGNAL("clicked()"), self.Cancelar)
		self.connect(self.ListWidgetReceptores, QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem *)"),self.EditarSeleccionado)

	def ListarReceptores(self):
		self.recepdiccionarioserial = {}
		self.recepdiccionariosocket = {}
		#Si estamos conectados a la Base de Datos
		if self.HayBD == True:
			#Conocer cuantos hay en Base de Datos
			self.BD.Seleccionar("select PortID, Descrip, Config, type, Port, idReceptor from t365_ConfigPortII")
			for row in self.BD.resultado:
				if str(row[3]) == str(1):
					Nombre = str(row[0]) + "," + str(row[2]) + "," + str(row[1])
					item = QListWidgetItem(Nombre)
					self.recepdiccionarioserial[Nombre] = item
					self.ListWidgetReceptores.addItem(item)
				elif str(row[3]) == str(2):
					Nombre = str(row[0]) + "," + str(row[1])
					item = QListWidgetItem(Nombre)
					self.recepdiccionariosocket[Nombre] = item
					self.ListWidgetReceptores.addItem(item)
		#Si estamos en modo Stand Alone
		elif self.HayBD == False:
			archivoconfiguracion = open('conf/config.txt','r')
			for line in archivoconfiguracion:
				linea = line.split(",")
				if str(linea[6]).rstrip('\n') == "1":
					Nombre = str(linea[0]) + "," + str(nombresreceptoresserial[linea[5]]+ "," + "SERIAL" )
					item = QListWidgetItem(Nombre)
					self.recepdiccionarioserial[Nombre] = item
					self.ListWidgetReceptores.addItem(item)
				elif str(linea[6]).rstrip('\n') == "2":
					Nombre = str(linea[0]) + "," + str(nombresreceptoressocket[linea[5]]+ "," + "SOCKET")
					item = QListWidgetItem(Nombre)
					self.recepdiccionariosocket[Nombre] = item
					self.ListWidgetReceptores.addItem(item)



	def Cancelar(self):
		self.close()

	def EditarSeleccionado(self,item):
		for name, obj in self.recepdiccionarioserial.items():
			if obj == item:
				ventanaeditarserial = QeditarReceptorSerial(self, name, self.BD, self.HayBD)
				ventanaeditarserial.show()
			else:
				pass
		for name, obj in self.recepdiccionariosocket.items():
			if obj == item:
				ventanaeditarsocket = QeditarReceptorSocket(self, name, self.BD, self.HayBD)
				ventanaeditarsocket.show()
			else: 
				pass
		

class QeditarReceptorSerial(QDialog):
	def __init__(self, parent, nombre, BD, HayBD):
		
		#super(Qnuevoreceptor,self).__init__()
		QDialog.__init__(self, parent)
		self.setWindowTitle('Editar Receptor Serial')

		#Le asigno el Padre(Qeditarreceptores) en una variable
		#Para luego manejar sus widgets desde aca.
		self.padre = parent
		self.nombre = nombre
		#Me traigo Conexion a BD
		self.BD = BD
		#Me traigo si hay BD
		self.HayBD = HayBD
		#Descomentar Abajo si queremos los puertos disponibles solamente
		#Pero es lento y da problemas al editar cuando un com no esta abierto
		#Obvio comentar abajo donde se colocan 100 COM en caso de habilitar 
		#la busqueda de los disponibles
		#puertos = serial_ports()
		puertos = []
		for i in range(101):
			puertos.append('COM'+str(i))
		if HayBD == True:
			#Identificar que receptor Cargar de la Base de Datos
			self.nombre = self.nombre.split(',')
			self.BD.SeleccionarUno("select PortID, Config, idReceptor, prefijo from t365_ConfigPortII where PortID = ?", self.nombre[0])
			self.numeropuerto = self.BD.resultado.PortID
			self.puertoactual = ("COM" + self.BD.resultado.PortID)
			configuracionactual = self.BD.resultado.Config.split(',')
			velocidadactual = str(configuracionactual[0])
			tamanoactual = str(configuracionactual[2])
			paridadactual = str(configuracionactual[1])
			stopactual = str(configuracionactual[3])
			receptoractual = int(self.BD.resultado.idReceptor)
			prefijoactual = str(self.BD.resultado.prefijo)


		elif HayBD == False:
			#Identificar que receptor Cargar del archivo de Texto
			self.nombre = self.nombre.split(',')
			archivoconfiguracion = open('conf/config.txt','r')
			for line in archivoconfiguracion:
				linea = line.split(",")
				if linea[0] == self.nombre[0]:
					self.numeropuerto = linea[0]
					self.puertoactual = ("COM" + self.numeropuerto)
					velocidadactual = str(linea[1])
					for name, obj in nombresPySerial["Tamano"].items():
						if obj == str(linea[2]):
							tamanoactual = str(name)
					for name, obj in nombresPySerial["Paridad"].items():
						if obj == str(linea[3]):
							paridadactual = str(name)
					for name, obj in nombresPySerial["Stop"].items():
						if obj == str(linea[4]):
							stopactual = str(name)
					receptoractual = int(linea[5])
					prefijoactual = str(linea[7]).rstrip("\n")


		#Labels
		self.LabelPuertoSerial = QLabel()
		self.LabelPuertoSerial.setText('Puerto')
		self.LabelVelocidad = QLabel()
		self.LabelVelocidad.setText('Velocidad')
		self.LabelTamano = QLabel()
		self.LabelTamano.setText('Tamano')
		self.LabelParidad = QLabel()
		self.LabelParidad.setText('Paridad')
		self.LabelStop = QLabel()
		self.LabelStop.setText('StopBit')
		self.LabelReceptorSerial = QLabel()
		self.LabelReceptorSerial.setText('Receptor')
		self.LabelPrefijo = QLabel()
		self.LabelPrefijo.setText('Prefijo')

		#ComboBox
		self.ComboPuerto = QComboBox()
		self.ComboPuerto.addItems(puertos)
		self.ComboPuerto.setCurrentIndex(int(puertos.index(self.puertoactual)))
		self.ComboVelocidad = QComboBox()
		self.ListaVelocidad = ('50', '75', '110', '134', '150', '200', '300', '600', '1200', '1800', '2400', '4800', '9600', '19200', '38400', '57600', '115200')
		self.ComboVelocidad.addItems(self.ListaVelocidad)
		self.ComboVelocidad.setCurrentIndex(self.ListaVelocidad.index(velocidadactual))
		self.ComboTamano = QComboBox()
		# sorted(diccionario.keys()) devuelve el una lista de las claves del diccionario
		# list(diccionario.keys()) devuelve la lista tambien pero no ordenada
		self.ListaTamano = sorted(nombresPySerial['Tamano'].keys())
		self.ComboTamano.addItems(self.ListaTamano)
		self.ComboTamano.setCurrentIndex(self.ListaTamano.index(tamanoactual))
		self.ComboParidad = QComboBox()
		self.ListaParidad = sorted(nombresPySerial['Paridad'].keys())
		self.ComboParidad.addItems(self.ListaParidad)
		self.ComboParidad.setCurrentIndex(self.ListaParidad.index(paridadactual))
		self.ComboStop = QComboBox()
		self.ListaStop = sorted(nombresPySerial['Stop'].keys())
		self.ComboStop.addItems(self.ListaStop)
		self.ComboStop.setCurrentIndex(self.ListaStop.index(stopactual))
		self.ComboReceptorSerial = QComboBox()
		self.diccionarioReceptores= {'SUR-GARD': 1, 'SENTINEL': 2, 'AES': 3, 'DMP': 11, 'VisorALARM': 9, 'M1A': 13, 'M1AHEX': 14, 'MCDI' : 15, 'SilentKnight' : 4}
		self.listaReceptores=['SUR-GARD', 'SENTINEL', 'DMP', 'AES', 'VisorALARM', 'M1A', 'M1AHEX', 'MCDI', 'SilentKnight']
		self.ComboReceptorSerial.addItems(self.listaReceptores)
		for name, number in self.diccionarioReceptores.items():
			if number == int(receptoractual):
				nombrereceptoractual = name
		self.ComboReceptorSerial.setCurrentIndex(self.listaReceptores.index(nombrereceptoractual))
		self.ComboPrefijo = QComboBox()
		self.ListaPrefijo = ['0','1000','2000','3000','4000','5000','6000','7000','8000','9000']
		self.ComboPrefijo.addItems(self.ListaPrefijo)
		self.ComboPrefijo.setCurrentIndex((self.ListaPrefijo.index(prefijoactual)))

		#Botones
		self.BotonAdd = QPushButton("Editar")
		self.BotonBorrar = QPushButton("Borrar")
		self.BotonCancel = QPushButton("Cancelar")


		#Creando Layouts e Asignandoles Ubicacion entre ellos
		self.layouthorizontal = QHBoxLayout()
		self.setLayout(self.layouthorizontal)
		self.layoutvertical1 = QVBoxLayout()
		self.layoutvertical2 = QVBoxLayout()
		self.layoutvertical3 = QVBoxLayout()
		self.layouthorizontal.addLayout(self.layoutvertical1)
		self.layouthorizontal.addLayout(self.layoutvertical2)
		self.layouthorizontal.addLayout(self.layoutvertical3)

		#Acomodando los Widgets en Layouts
		#Primera Fila de Labels

		self.layoutvertical1.addWidget(self.LabelPuertoSerial)
		self.layoutvertical1.addWidget(self.LabelVelocidad)
		self.layoutvertical1.addWidget(self.LabelTamano)
		self.layoutvertical1.addWidget(self.LabelParidad)
		self.layoutvertical1.addWidget(self.LabelStop)
		self.layoutvertical1.addWidget(self.LabelReceptorSerial)
		self.layoutvertical1.addWidget(self.LabelPrefijo)

		#Segunda Fila de Combos

		self.layoutvertical2.addWidget(self.ComboPuerto)
		self.layoutvertical2.addWidget(self.ComboVelocidad)
		self.layoutvertical2.addWidget(self.ComboTamano)
		self.layoutvertical2.addWidget(self.ComboParidad)
		self.layoutvertical2.addWidget(self.ComboStop)
		self.layoutvertical2.addWidget(self.ComboReceptorSerial)
		self.layoutvertical2.addWidget(self.ComboPrefijo)

		#Tercera Fila Botones
		self.layoutvertical3.addWidget(self.BotonAdd)
		self.layoutvertical3.addWidget(self.BotonBorrar)
		self.layoutvertical3.addWidget(self.BotonCancel)

		#Conexiones
		self.connect(self.BotonAdd, QtCore.SIGNAL("clicked()"), self.EditarReceptor)
		self.connect(self.BotonCancel, QtCore.SIGNAL("clicked()"), self.Cancelar)
		self.connect(self.BotonBorrar, QtCore.SIGNAL("clicked()"), self.Borrar)

	def EditarReceptor(self):
		#Tomando los Datos de la Interfaz
		vpuerto=self.ComboPuerto.currentText().replace("COM","")
		vvelocidad= self.ComboVelocidad.currentText()
		vtamano=str(self.ComboTamano.currentText())
		vparidad=str(self.ComboParidad.currentText())
		vstop=str(self.ComboStop.currentText())
		vreceptor=str(self.ComboReceptorSerial.currentText())
		vprefijo=str(self.ComboPrefijo.currentText())

		if self.HayBD == True:
			#Conocer cuantos Receptores hay en Base de Datos
			self.BD.Seleccionar("select PortID from t365_ConfigPortII")
			#cantidadreceptores = 0
			#Ahora voy a contar los receptores que estan en la base de datos para agregar el numero
			#del orden del receptor, campo para saber como se van a mostrar en orden aunque todavia
			#no esta funcionando eso, pero igual aprovecho y me traigo en una lista los puertos
			#Usados por otros receptores para dar un error en caso de que ya este ese puerto
			puertoscomutilizados = []
			for row in self.BD.resultado:
			#	cantidadreceptores = cantidadreceptores + 1
				puertoscomutilizados.append(row[0])
			#Ahora le Borramos el Puerto que estamos editando Actualmente
			#Porque si le vamos a cambiar por ejemplo la paridad
			#Nos va a decir al guardar que el puerto ya esta siendo utilizado
			#Para eso eliminamos el puerto que estamos editando de la lista
			puertoscomutilizados.remove(self.puertoactual.replace('COM',''))
			#Ahora comprobamos si el puerto seleccionado no esta en la lista
			if vpuerto in puertoscomutilizados:
				#Abriendo Mensaje de Error
				ventanaerrorpuerto = QerrorPuerto(self).exec_()
			else:
				#Guardando en la Base de Datos
				configbd = str(vvelocidad+','+vparidad+','+vtamano+','+vstop)
				self.BD.Actualizar("UPDATE t365_ConfigPortII SET PortID = ?, Descrip = ?, Config = ?, type = ?, idReceptor = ?, prefijo = ? WHERE PortID = ?", int(vpuerto), vreceptor, configbd, 1 , str(self.diccionarioReceptores[vreceptor]),int(vprefijo), self.numeropuerto)
				#Cerrando la Ventana
				self.close()
		elif self.HayBD == False:
			#Me traigo una lista de los puertos utilizados para dar error en caso de que 
			#Ya exista
			archivoconfiguracion = open('conf/config.txt','r')
			puertoscomutilizados = []
			for line in archivoconfiguracion:
				linea = line.split(",")
				puertoscomutilizados.append(linea[0])
			archivoconfiguracion.close()
			#Ahora le Borramos el Puerto que estamos editando Actualmente
			#Porque si le vamos a cambiar por ejemplo la paridad
			#Nos va a decir al guardar que el puerto ya esta siendo utilizado
			#Para eso eliminamos el puerto que estamos editando de la lista
			puertoscomutilizados.remove(self.puertoactual.replace('COM',''))
			#Ahora comprobamos si el puerto seleccionado no esta en la lista
			if str(vpuerto) in puertoscomutilizados:
				#Abriendo Mensaje de Error
				ventanaerrorpuerto = QerrorPuerto(self).exec_()
			else:
				#Buscando donde estaba en el archivo de texto y guardandolo nuevamente
				archivoconfiguracion=open('conf/config.txt','r')
				archivoactual = archivoconfiguracion.read()
				archivoconfiguracion.close()
				archivoconfiguracion=open('conf/config.txt','r')
				for line in archivoconfiguracion:
					linea = line.split(",")
					if str(linea[0]) == str(self.numeropuerto):
						lineaeditar = line
				nuevalinea = str(vpuerto)+","+str(vvelocidad)+","+nombresPySerial['Tamano'][vtamano]+","+nombresPySerial['Paridad'][vparidad]+","+nombresPySerial['Stop'][vstop]+","+str(self.diccionarioReceptores[vreceptor])+","+"1"+","+str(vprefijo)+"\n"
				archivoeditado = archivoactual.replace(lineaeditar,nuevalinea)
				archivoconfiguracion.close()
				archivoconfiguracion=open('conf/config.txt','w')
				archivoconfiguracion.write(archivoeditado)
				archivoconfiguracion.close()
				#Cerrando la Ventana
				self.close()
		#Borro la lista de items del QListWidget del padre
		self.padre.ListWidgetReceptores.clear()
		#Llamo a la funcion de listar nuevamente los receptores en el padre
		self.padre.ListarReceptores()


	def Borrar(self):
		if self.HayBD == True:
			self.BD.Borrar("delete from t365_ConfigPortII where PortID = ?", self.numeropuerto)
		if self.HayBD == False:
			#Buscando donde estaba en el archivo de texto y guardandolo nuevamente
			archivoconfiguracion=open('conf/config.txt','r')
			archivoactual = archivoconfiguracion.read()
			archivoconfiguracion.close()
			archivoconfiguracion=open('conf/config.txt','r')
			for line in archivoconfiguracion:
				linea = line.split(",")
				if str(linea[0]) == str(self.numeropuerto):
					lineaeditar = line
			archivoeditado = archivoactual.replace(lineaeditar,'')
			archivoconfiguracion.close()
			archivoconfiguracion=open('conf/config.txt','w')
			archivoconfiguracion.write(archivoeditado)
			archivoconfiguracion.close()
		#Borro la lista de items del QListWidget del padre
		self.padre.ListWidgetReceptores.clear()
		#Llamo a la funcion de listar nuevamente los receptores en el padre
		self.padre.ListarReceptores()
		
		self.close()

	def Cancelar(self):
		self.close()

class QeditarReceptorSocket(QDialog):
	def __init__(self, parent, nombre, BD, HayBD):
		#super(Qnuevoreceptor,self).__init__()
		QDialog.__init__(self, parent)
		self.padre = parent
		self.BD = BD
		self.HayBD = HayBD
		self.nombre = nombre
		self.setWindowTitle('Editar Receptor Socket')
		self.setMinimumSize(300,100)
		self.setMaximumSize(300,100)
		
		#Identificar que receptor Cargar
		if self.HayBD == True:
			self.nombre = self.nombre.split(',')
			self.BD.SeleccionarUno("""select PortID, idReceptor, prefijo, Server from t365_ConfigPortII where PortID = ? """, self.nombre[0])
			self.puertoactual = self.BD.resultado.PortID
			receptoractual = int(self.BD.resultado.idReceptor)
			self.prefijoactual = str(self.BD.resultado.prefijo)
			self.serveractual = self.BD.resultado.Server
			if not self.serveractual:
				self.serveractual = ''
		elif self.HayBD == False:
			#Identificar que receptor Cargar del archivo de Texto
			self.nombre = self.nombre.split(',')
			archivoconfiguracion = open('conf/config.txt','r')
			for line in archivoconfiguracion:
				linea = line.split(",")
				if linea[0] == self.nombre[0]:
					self.puertoactual = linea[0]
					#self.puertoactual = ("SOCKET" + self.numeropuerto)
					receptoractual = int(linea[5])
					self.prefijoactual = str(linea[7])
					self.serveractual = linea[8].rstrip("\n")
					if not self.serveractual:
						self.serveractual = ''

		#Labels
		self.LabelServidor = QLabel()
		self.LabelServidor.setText("Direccion")
		self.LabelPuertoSocket = QLabel()
		self.LabelPuertoSocket.setText('Puerto')
		self.LabelReceptorSocket = QLabel()
		self.LabelReceptorSocket.setText('Receptor')
		self.LabelPrefijoSocket = QLabel()
		self.LabelPrefijoSocket.setText('Prefijo')
		#ComboBox
		self.ComboReceptorSocket = QComboBox()
		self.diccionarioReceptores= {'EBSCID': 16,'EBSXML':17,'SS365':18,'SUR-GARD': 1}
		self.listaReceptores=['EBSCID','EBSXML','SS365','SUR-GARD']
		self.ComboReceptorSocket.addItems(self.listaReceptores)
		for name, number in self.diccionarioReceptores.items():
			if number == int(receptoractual):
				nombrereceptoractual = name
		self.ComboReceptorSocket.setCurrentIndex(self.listaReceptores.index(nombrereceptoractual))
		self.ComboPrefijoSocket = QComboBox()
		self.ListaPrefijoSocket = ['0','1000','2000','3000','4000','5000','6000','7000','8000','9000']
		self.ComboPrefijoSocket.addItems(self.ListaPrefijoSocket)
		self.ComboPrefijoSocket.setCurrentIndex(self.ListaPrefijoSocket.index(self.prefijoactual))

		#Botones
		self.BotonAdd = QPushButton("Editar")
		self.BotonBorrar = QPushButton("Borrar")
		self.BotonCancel = QPushButton("Cancelar")
		#Spin
		self.SpinPuerto = QSpinBox()
		self.SpinPuerto.setMaximum(9999)
		self.SpinPuerto.setValue(int(self.puertoactual))

		self.Direccion = QLineEdit()
		self.Direccion.setText(self.serveractual)
		#Creando Layouts e Asignandoles Ubicacion entre ellos
		self.layouthorizontal = QHBoxLayout()
		self.setLayout(self.layouthorizontal)
		self.layoutvertical1 = QVBoxLayout()
		self.layoutvertical2 = QVBoxLayout()
		self.layoutvertical3 = QVBoxLayout()
		self.layouthorizontal.addLayout(self.layoutvertical1)
		self.layouthorizontal.addLayout(self.layoutvertical2)
		self.layouthorizontal.addLayout(self.layoutvertical3)
		#Acomodando los Widgets en Layouts
		

		#Primera Fila de Labels
		self.layoutvertical1.addWidget(self.LabelServidor)
		self.layoutvertical1.addWidget(self.LabelPuertoSocket)
		self.layoutvertical1.addWidget(self.LabelReceptorSocket)
		self.layoutvertical1.addWidget(self.LabelPrefijoSocket)
		#Segunda Fila de Combos
		self.layoutvertical2.addWidget(self.Direccion)
		self.layoutvertical2.addWidget(self.SpinPuerto)
		self.layoutvertical2.addWidget(self.ComboReceptorSocket)
		self.layoutvertical2.addWidget(self.ComboPrefijoSocket)
		#Tercera Fila Botones
		self.layoutvertical3.addWidget(self.BotonAdd)
		self.layoutvertical3.addWidget(self.BotonBorrar)
		self.layoutvertical3.addWidget(self.BotonCancel)
		#Conexiones
		self.connect(self.BotonAdd, QtCore.SIGNAL("clicked()"), self.EditarReceptor)
		self.connect(self.BotonCancel, QtCore.SIGNAL("clicked()"), self.Cancelar)
		self.connect(self.BotonBorrar, QtCore.SIGNAL("clicked()"), self.Borrar)

	def EditarReceptor(self):
		#Tomando los Valores de la interfaz
		vdireccion = str(self.Direccion.text())
		vpuerto=self.SpinPuerto.value()
		vreceptor=str(self.ComboReceptorSocket.currentText())
		vprefijo=str(self.ComboPrefijoSocket.currentText())
		if self.HayBD == True:
			#Guardando en la Base de Datos
			#Conocer cuantos hay en Base de Datos
			self.BD.Seleccionar("select Port from t365_ConfigPortII")
			puertossocketutilizados = []
			for row in self.BD.resultado:
				puertossocketutilizados.append(row[0])
			#Ahora le Borramos el Puerto que estamos editando Actualmente
			#Porque si le vamos a cambiar por ejemplo la paridad
			#Nos va a decir al guardar que el puerto ya esta siendo utilizado
			#Para eso eliminamos el puerto que estamos editando de la lista
			puertossocketutilizados.remove(int(self.puertoactual))
			#Ahora comprobamos si el puerto seleccionado no esta en la lista
			if vpuerto in puertossocketutilizados:
				#Abriendo Mensaje de Error
				ventanaerrorpuerto = QerrorPuerto(self).exec_()
			else:
				self.BD.Actualizar("UPDATE t365_ConfigPortII SET PortID = ?, Descrip = ?, Config = ?, type = ?, Port = ?, idReceptor = ?, prefijo = ?, server = ? WHERE PortID = ?", int(vpuerto), vreceptor, int(vpuerto), 2 ,int(vpuerto), str(self.diccionarioReceptores[vreceptor]), int(vprefijo),str(vdireccion),self.puertoactual)
				#Cerrando la Ventana
				self.close()
		elif self.HayBD == False:
			#Guardando en el Archivo de Texto
			#Me traigo una lista de los puertos utilizados para dar error en caso de que 
			#Ya exista
			archivoconfiguracion = open('conf/config.txt','r')
			puertossocketutilizados = []
			for line in archivoconfiguracion:
				linea = line.split(",")
				puertossocketutilizados.append(linea[0])
			archivoconfiguracion.close()
			#Ahora le Borramos el Puerto que estamos editando Actualmente
			#Porque si le vamos a cambiar por ejemplo la paridad
			#Nos va a decir al guardar que el puerto ya esta siendo utilizado
			#Para eso eliminamos el puerto que estamos editando de la lista
			puertossocketutilizados.remove(self.puertoactual)
			#Ahora comprobamos si el puerto seleccionado no esta en la lista
			if str(vpuerto) in puertossocketutilizados:
				#Abriendo Mensaje de Error
				ventanaerrorpuerto = QerrorPuerto(self).exec_()

			else:
				#Buscando donde estaba en el archivo de texto y guardandolo nuevamente
				archivoconfiguracion=open('conf/config.txt','r')
				archivoactual = archivoconfiguracion.read()
				archivoconfiguracion.close()
				archivoconfiguracion=open('conf/config.txt','r')
				for line in archivoconfiguracion:
					linea = line.split(",")
					if str(linea[0]) == str(self.puertoactual):
						lineaeditar = line
				nuevalinea = str(vpuerto)+","+","+","+","+","+str(self.diccionarioReceptores[vreceptor])+","+"2"+","+str(vprefijo)+","+str(vdireccion)+"\n"
				archivoeditado = archivoactual.replace(lineaeditar,nuevalinea)
				archivoconfiguracion.close()
				archivoconfiguracion=open('conf/config.txt','w')
				archivoconfiguracion.write(archivoeditado)
				archivoconfiguracion.close()
				self.close()
		#Borro la lista de items del QListWidget del padre
		self.padre.ListWidgetReceptores.clear()
		#Llamo a la funcion de listar nuevamente los receptores en el padre
		self.padre.ListarReceptores()

	def Borrar(self):
		if self.HayBD == True:
			if self.serveractual:
				self.BD.Borrar("delete from t365_ConfigPortII where PortID = ? and Server = ?", (self.puertoactual,self.serveractual))
			else:
				self.BD.Borrar("delete from t365_ConfigPortII where PortID = ? and Server is null",self.puertoactual)

		if self.HayBD == False:
			#Buscando donde estaba en el archivo de texto y guardandolo nuevamente
			archivoconfiguracion=open('conf/config.txt','r')
			archivoactual = archivoconfiguracion.read()
			archivoconfiguracion.close()
			archivoconfiguracion=open('conf/config.txt','r')
			for line in archivoconfiguracion:
				linea = line.split(",")
				if str(linea[0]) == str(self.puertoactual):
					lineaeditar = line
			archivoeditado = archivoactual.replace(lineaeditar,'')
			archivoconfiguracion.close()
			archivoconfiguracion=open('conf/config.txt','w')
			archivoconfiguracion.write(archivoeditado)
			archivoconfiguracion.close()
		#Borro la lista de items del QListWidget del padre
		self.padre.ListWidgetReceptores.clear()
		#Llamo a la funcion de listar nuevamente los receptores en el padre
		self.padre.ListarReceptores()
		self.close()
	
	def Cancelar(self):
		self.close()
