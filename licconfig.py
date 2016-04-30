from Crypto.Cipher import XOR
from base64 import b64encode, b64decode
from getpass import getpass
import uuid
from time import sleep
from socket import gethostname
from ConfigParser import ConfigParser

def CualBD():
    while True:
        print 'Indique la version de BD'
        print '1 - SQL2000'
        print '2 - SQL2005'
        print '3 - SQL2008'
        print '4 - SQL2012'
        print '5 - SQL2014'
        cualbd = raw_input('Indique: ')
        if int(cualbd) <= 5:
            if cualbd == '1':
                stringdb = 'DRIVER={SQL Server};SERVER=NOMBREPC;DATABASE=NOMBREBD;UID=USUARIOBD;PWD=PASSWORDBD'
            elif cualbd == '2':
                stringdb = 'Driver={SQL Native Client};Server=NOMBREPC;Database=NOMBREBD;Uid=USUARIOBD;Pwd=PASSWORDBD'
            elif cualbd == '3':
                stringdb = 'Driver={SQL Server Native Client 10.0};Server=NOMBREPC;Database=NOMBREBD;Uid=USUARIOBD;Pwd=PASSWORDBD'
            elif cualbd == '4':
                stringdb = 'Driver={SQL Server Native Client 11.0};Server=NOMBREPC;Database=NOMBREBD;Uid=USUARIOBD;Pwd=PASSWORDBD'
            elif cualbd == '5':
                stringdb = 'Driver={SQL Server Native Client 11.0};Server=NOMBREPC;Database=NOMBREBD;Uid=USUARIOBD;Pwd=PASSWORDBD'
            return stringdb
        else:
            print 'La opcion no es valida'

def ConvertirDatos(stringbd,lic,cualmodo,dondebd):
    print 'Convirtiendo Datos'
    if dondebd == '1':
        stringbd = stringbd.replace('NOMBREPC',str(gethostname()))
    elif dondebd == '2':
        print 'Indique la direccion donde se encuentra la Base de Datos' 
        direccionremota = raw_input('Indique una direccion IP o un DNS para la conexion a Base de Datos: ')
        stringbd = stringbd.replace('NOMBREPC','mc24.no-ip.net')
    stringbd = stringbd.replace('NOMBREBD','365DB')
    stringbd = stringbd.replace('USUARIOBD','sa')
    stringbd = stringbd.replace('PASSWORDBD','jerm')
    deco = XOR.new(b64decode('MjAxMDE3MzMtOTYwOTkyNg=='))
    stringbd =  b64encode(deco.encrypt(str(stringbd)))
    deco = XOR.new(b64decode('MjAxMDE3MzMtOTYwOTkyNg=='))
    lic =  b64encode(deco.encrypt(str(lic)))
    deco = XOR.new(b64decode('MjAxMDE3MzMtOTYwOTkyNg=='))
    cualmodo =  b64encode(deco.encrypt(str(cualmodo)))
    print 'Datos Convertidos'
    CrearArchivo(stringbd,lic,cualmodo)

def CrearArchivo(stringbd,lic,cualmodo):
    print 'Creando Archivo'
    try:
        cfgfile = open("conf/config.ini",'w')
        Config = ConfigParser()
        Config.add_section('BASE DE DATOS')
        Config.set('BASE DE DATOS','Conexion',stringbd)
        Config.add_section('CUENTA')
        Config.set('CUENTA','Lic',lic)
        Config.set('CUENTA','Modo',cualmodo)
        Config.write(cfgfile)
        print 'Archivo Creado'
        cfgfile.close()
    except:
        print 'Error de Ubicacion'

print 'Configurador de Licencia 365'
usuarioiniciar = '' #raw_input('Usuario: ')
passwordiniciar = '' #getpass(prompt='Contrasena: ')
if usuarioiniciar == '' and passwordiniciar == '':
    while True:
        print 'Indique el MODO del Receptor'
        print '1 - BD'
        print '2 - StandAlone'
        cualmodo = raw_input('Indique: ')
        if cualmodo == '1' or cualmodo == '2':
            break
        else:
            print 'La opcion no es valida'
    #MODO BASE DE DATOS
    if cualmodo == '1':
        while True:
            print 'Indique si la base de datos es Local o Remota'
            print '1 - Local'
            print '2 - Remota'
            dondebd = raw_input('Indique: ')
            if dondebd == '1' or dondebd == '2':
                break
            else:
                print 'La opcion no es valida'
        if dondebd == '1':
            stringbd = CualBD()
        elif dondebd == '2':
            stringbd = CualBD()
    #MODO STANDALONE
    elif cualmodo == '2':
        dondebd = False
        stringbd = 'NoHayBaseDeDatos'
    lic = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1])
    print 'Introduza la clave Generadora de Licencia'
    clavegeneradora = ''
    #b64decode('OTYwOTkyNi0yMDEwMTczMw==')
    if clavegeneradora == '':
        print 'Generando Datos'
        sleep(1)
        print 'Datos Generados'
        ConvertirDatos(stringbd,lic,cualmodo,dondebd)
        
        
    
        
            
        
        
