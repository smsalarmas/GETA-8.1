import re
patron = re.compile('(?P<Identificador>.)(?P<Receptor>..)(?P<Linea>.)(?P<Separador>      )(?P<Abonado>....)(?P<Separador2> )(?P<T>.)(?P<Separador3>  )(?P<Evento>..)')
prueba = patron.search('1003      0000 T  40')

print prueba.groups()	



#101001      0325 A  82
#1011      0325 A  82



