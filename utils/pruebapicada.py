trama = '&041403"072235"01"4810"05001.1039"18160200000"18335400000"18140001000R'

picartrama = trama.split('"',4)
print picartrama
#Como la Trama viene con muchos eventos, la pico en el primer " para Tener
#El principio de la trama para todos los eventos
tramadividida = picartrama[4].split('"',1)
print tramadividida
#Ahora pico todos los eventos por su "
listadeeventos = tramadividida[1].split('"')

for i in listadeeventos:
	tr = picartrama[0] + '"' + picartrama[1] + '"' + picartrama[2] + '"' + picartrama[3] + '"' + tramadividida[0] + '"' + i 
	print tr
