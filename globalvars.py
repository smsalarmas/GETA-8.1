global listass365disprog
listass365disprog = []
global globalvar
globalvar =  {"listadepuertosSOCKET" : {},"listadepuertosCOM" : {}, "listadetabs" : {}, "listadetablas" : {}, "listadelayout" : {} }
global listadereceptores
listadereceptores = {}
global nombresreceptoresserial
nombresreceptoresserial = {'1' : "Sur-Gard", '2' : "SENTINEL", '3' : "AES", '11' : "DMP", '9' : "VisorAlarm", '13' : "M1A", '14' : "M1AHEX", '15' : "MCDI", '4' : 'SilentKnight'}
global nombresreceptoressocket
nombresreceptoressocket = {'16' : "EBSCID",'17':'EBSXML','18':"SS365",'1' : "Sur-Gard"}

global listatabscreados
listatabscreados = []

global ColaParaGuardar
ColaParaGuardar = []
global ColaParaGuardarSenalSistema
ColaParaGuardarSenalSistema = []
#Diccionario con Puertos Corriendo para Detener
PuertosCorriendoCOM = {}
PuertosCorriendoSOCKET = {}
PuertosCorriendoTWISTED = {}
#Variable para saber cuando ya se inicio el reactor y no iniciarlo nuevamente
global ReactorIniciado
ReactorIniciado = False
#Boolean para Detener Puertos y parar WhileTrue para ue no de problema al hacerle close
#cuando se le da al boton detener
#DetenerPuertos = False
#Diccionario para cambiar los nombres como los necesita Pyserial
nombresPySerial = {'Tamano': {'5':'serial.FIVEBITS','6':'serial.SIXBITS','7':'serial.SEVENBITS','8':'serial.EIGHTBITS'}, 'Paridad': {'N':'serial.PARITY_NONE','E':'serial.PARITY_EVEN','O':'serial.PARITY_ODD','M':'serial.PARITY_MARK'}, 'Stop': {'1':'serial.STOPBITS_ONE','1.5':'serial.STOPBITS_ONE_POINT_FIVE','2':'serial.STOPBITS_TWO'}}

#Variable Global Modo de Funcionamiento del Software
#Si es BD = 1 si es STAND ALONE = 2
from check import BDCheck
global Modo
Modo = BDCheck()

