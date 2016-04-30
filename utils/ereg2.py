import re
patron = re.compile('(?P<Inicio><packet.{5,100}>)(?P<IncioMsg><msg )(?P<Dispositivo>dt="..")(?P<Separacion1> )(?P<Serial>sn="\d{0,20}")(?P<Separacion2> )(?P<FechaDisp>dts="\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d"|)(?P<Separacion3> |)(?P<FechaOSM>csts="\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d"|)(?P<Separacion4> )(?P<SRC>src="[^"]{1,20}")(?P<Separacion5> )(?P<Evento>evt="[^"]{1,25}")(?P<Separacion6> |)(?P<DataEvento>evtData="[^"]{0,500}"|)(?P<Separacion7> |)(?P<CSQ>CSQ="[^"]{0,6}"|)(?P<Separacion8> |)(?P<EstatusConexion>ConnectionStatus="[^"]{0,50}"|)(?P<Separacion9> |)(?P<Bateria>BattVol="[^"]{0,15}"|)(?P<Separacion10> |)(?P<EstatusPower>PowerStatus="[^"]{0,80}"|)(?P<Separacion11> |)(?P<ActividadMovimiento>MovementActivity="[^"]{0,6}"|)(?P<Separacion12> |)(?P<GPS>gps="[^"]{0,100}"|)')
prueba = patron.search('<packet sq="28" id="1" count="1" rep="1" group="ALL"><msg dt="at" sn="404683" dts="2016-01-18 14:30:14" csts="2016-01-18 19:29:35" src="FPX_ACTITRACK" evt="TEST"/></packet>')

print prueba.groups()	



#101001      0325 A  82
#1011      0325 A  82



