from sendmail import EnviarEmailPlain
from pcinfo import PCInfo
from getxxmc import xxmx

def AvisodeApertura(lic):
	try:
		Asunto = 'Evento de Receptor Abierto'
		informacion = PCInfo()
		Mensaje = 'Receptor Abierto por la IP Publica= ' + str(informacion.ObtenerIPPublica()) + '\r\n' + 'Nombre del Equipo BD= ' + str(informacion.ObtenerNombreClienteBD())+ '\r\n' + 'Nombre del Equipo e IP Local= ' + str(informacion.ObtenerNombreIpLocal()) + '\r\n' + 'Direccion MAC= ' + str(xxmx) + '\r\n' + "Licencia= " + str(lic)
		EnviarEmailPlain('jermsoft@gmail.com',Asunto,Mensaje)
		#EnviarEmailPlain('vioren@gmail.com',Asunto,Mensaje)
	except:
		pass
