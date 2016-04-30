import re

def tratar(trama,numpuerto,prefijo):
	#colaSIA3.append(trama)
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
				patron = re.compile('(?P<Nada>&......"......".."....".)(?P<Receptor>\d\d)(?P<Linea>[0-9a-zA-Z]{1,3})(?P<Espacio>.)(?P<Abonado>....)(?P<Separador>")(?P<Particion>ri.)(?P<Separador2>")(?P<Evento>..)(?P<ZonaUsuario>\d{2,})')
				dividida = patron.search(tr)
				#Agregando el prefijo al Abonado en caso de que lo tenga
				Abonado = str(dividida.group('Abonado'))
				if int(prefijo) >= 1000:
					Abonado = int(Abonado) + int(prefijo)
				datosparaGUI = (str(Abonado),dividida.group('Evento'),dividida.group('ZonaUsuario'),str(particionactual.replace("ri","")),dividida.group('Linea'),"nombreformato","LaFecha.damefecha()")
				datosparaBD = (trama,dividida.group('Linea'),str(Abonado),dividida.group('Evento'),dividida.group('ZonaUsuario'),"numprotocolo",str(particionactual.replace("ri","")),"numpuerto",'0')
				print dividida.groups()
#Si es una trama que trae un solo evento entonces
	else:
		patron = re.compile('(?P<Nada>&......"......".."....".)(?P<Receptor>\d\d)(?P<Linea>[0-9a-zA-Z]{1,3})(?P<Espacio>.)(?P<Abonado>....)(?P<Separador>")(?P<Particion>ri.)(?P<Separador2>")(?P<Evento>..)(?P<ZonaUsuario>\d{2,})')
		dividida = patron.search(trama)
		#Agregando el prefijo al Abonado en caso de que lo tenga
		Abonado = str(dividida.group('Abonado'))
		if int(prefijo) >= 1000:
			Abonado = int(Abonado) + int(prefijo)
		datosparaGUI = (str(Abonado),dividida.group('Evento'),dividida.group('ZonaUsuario'),dividida.group('Particion'),dividida.group('Linea'),"nombreformato","LaFecha.damefecha()")
		datosparaBD = (trama,dividida.group('Linea'),str(Abonado),dividida.group('Evento'),dividida.group('ZonaUsuario'),"numprotocolo",dividida.group('Particion'),"numpuerto",'0')

		print dividida.groups()


tratar('&041403"004239"01"4520"00401.1152"ri1"OR00"BH13"ri0"YK00"RY00"YK00"RY00o','1','0')