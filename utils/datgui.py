import re
patron = re.compile('(?P<Inicio><packet.{5,100}>)(?P<IncioMsg><msg )(?P<Dispositivo>dt="..")(?P<Separacion1> )(?P<Serial>sn=".{0,20}")(?P<Separacion2> )(?P<FechaDisp>dts="\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d"|)(?P<Separacion3> |)(?P<FechaOSM>csts="\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d"|)(?P<Separacion4> )(?P<SRC>src="[^"]{1,20}")(?P<Separacion5> )(?P<Evento>evt="[^"]{1,25}")(?P<Separacion6> |)(?P<DataEvento>evtData="[^"]{0,500}"|)(?P<Separacion7> |)(?P<CSQ>CSQ="[^"]{0,6}"|)(?P<Separacion8> |)(?P<EstatusConexion>ConnectionStatus="[^"]{0,50}"|)(?P<Separacion9> |)(?P<Bateria>BattVol="[^"]{0,15}"|)(?P<Separacion10> |)(?P<EstatusPower>PowerStatus="[^"]{0,80}"|)(?P<Separacion11> |)(?P<ActividadMovimiento>MovementActivity="[^"]{0,6}"|)(?P<Separacion12> |)(?P<GPS>gps="[^"]{0,100}"|)')

dividida = patron.search('<packet sq="12184" id="1" count="1" rep="1" group="ALL"><msg dt="lx" sn="LX-0020" dts="2016-03-26 12:12:00" csts="2016-03-26 17:13:27" src="LX20" evt="DATA DTMF" evtData="0x00003030323031383334303130313030342A"/></packet>')
#datosparaGUI = (dividida.group('Abonado'),dividida.group('Evento'),dividida.group('ZonaUsuario'),dividida.group('Particion')




"""Dispositivo = str(dividida.group('Dispositivo')).replace('dt="','').replace('"','')
Serial = str(dividida.group('Serial')).replace('sn="','').replace('"','')
FechaDisp = str(dividida.group('FechaDisp')).replace('dts="','').replace('"','')
FechaOSM = str(dividida.group('FechaOSM')).replace('csts="','').replace('"','')
Source = str(dividida.group('SRC')).replace('src="','').replace('"','')
Evento = str(dividida.group('Evento')).replace('evt="','').replace('"','')
DataEvento = str(dividida.group('DataEvento')).replace('evtData="','').replace('"','')

Signal = str(dividida.group('CSQ')).replace('CSQ="','').replace('"','')
EstatusConexion = str(dividida.group('EstatusConexion')).replace('ConnectionStatus="','').replace('"','')
EstatusPower = str(dividida.group('EstatusPower')).replace('PowerStatus="','').replace('"','')
ActividadMovimiento = str(dividida.group('ActividadMovimiento')).replace('MovementActivity="','').replace('"','')
GPS = str(dividida.group('GPS')).replace('gps="','').replace('"','')"""


print dividida.groups()