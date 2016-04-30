# -*- coding: utf-8 -*-
import socket
from urllib2 import urlopen
from json import load
from bd import BasedeDatos
from globalvars import Modo

class PCInfo(object):
    def __init__(self):
        pass
    def ObtenerIPPublica(self):
        try:
            self.my_ip = urlopen('http://ip.42.pl/raw').read().encode('utf8')
        except:
            self.my_ip = load(urlopen('http://jsonip.com'))['ip'].encode('utf8')
        else:
            self.my_ip = load(urlopen('http://httpbin.org/ip'))['origin'].encode('utf8')

        return self.my_ip

    def ObtenerNombreIpLocal(self):
        self.nombre = socket.gethostname()
        self.direccion_equipo = socket.gethostbyname(self.nombre)
        return [self.nombre,self.direccion_equipo]
    def ObtenerNombreClienteBD(self):
        if Modo == "1":
            BDNombreCliente = BasedeDatos()
            BDNombreCliente.Conectar()
            Nombre = BDNombreCliente.SeleccionarUno("select top 1 nombre from t365_Empresas where master = ?",1)
        elif Modo == "2":
            Nombre = "Sin Nombre Modo StandAlone"
        return Nombre








