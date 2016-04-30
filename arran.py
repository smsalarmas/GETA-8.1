import re
import datetime


a = '3401'
print a[0]
if a[0] == '1':
	a = 'E'+a[1:]
elif a[0] == '3':
	a = 'R'+a[1:]

print a


"""with open("DTMF.dat") as f:
	for line in f:
		#print line
		patron = re.compile('(?P<Inicio><packet.{5,100}>)(?P<IncioMsg><msg )(?P<Dispositivo>dt="..")(?P<Separacion1> )(?P<Serial>sn="\d{0,20}")(?P<Separacion2> )(?P<FechaDisp>dts="\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d"|)(?P<Separacion3> |)(?P<FechaOSM>csts="\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d"|)(?P<Separacion4> )(?P<SRC>src="[^"]{1,20}")(?P<Separacion5> )(?P<Evento>evt="[^"]{1,25}")(?P<Separacion6> |)(?P<DataEvento>evtData="[^"]{0,500}"|)(?P<Separacion7> |)(?P<CSQ>CSQ="[^"]{0,6}"|)(?P<Separacion8> |)(?P<EstatusConexion>ConnectionStatus="[^"]{0,50}"|)(?P<Separacion9> |)(?P<Bateria>BattVol="[^"]{0,15}"|)(?P<Separacion10> |)(?P<EstatusPower>PowerStatus="[^"]{0,80}"|)(?P<Separacion11> |)(?P<ActividadMovimiento>MovementActivity="[^"]{0,6}"|)(?P<Separacion12> |)(?P<GPS>gps="[^"]{0,100}"|)')
		dividida = patron.search(line)
		#print line
		#Dispositivo =dividida.group('Dispositivo').replace('dt="','').replace('"','')
		#Serial =dividida.group('Serial').replace('sn="','').replace('"','')
		#FechaDisp =dividida.group('FechaDisp').replace('dts="','').replace('"','')
		#FechaOSM =dividida.group('FechaOSM').replace('csts="','').replace('"','')
		#Source =dividida.group('SRC').replace('src="','').replace('"','')
		#Evento =dividida.group('Evento').replace('evt="','').replace('"','')
		DataEvento =dividida.group('DataEvento').replace('evtData="','').replace('"','')[2:]
		#print DataEvento
		#print DataEvento
		print DataEvento
"""