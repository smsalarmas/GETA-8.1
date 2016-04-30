# servchat.py
# Creamos un servidor de chat.

import socket
import select

def accept_new_connection():

 try:
     global server
     global desc
     newsock, (remhost, remport) = server.accept()
     server.settimeout(.1)
     print "Se ha conectado %s:%s" % (str(remhost), str(remport))
     desc.append(newsock)
 except:
     pass

def broadcast(msg, sock):

 global desc
 global server
 host, port = sock.getpeername()
 msg = "[%s:%s]: %s" % (str(host), str(port), str(msg))
 for destsock in desc:
     if destsock != sock and destsock != server:
         destsock.send(msg)

def get_msg(sock):

 try:
     msg = sock.recv(1024)
     sock.settimeout(.1)
     return msg
 except:
     global desc
     host, port = sock.getpeername()
     print "[%s:%s] ha salido." % (str(host), str(port))
     desc.remove(sock)
     return None
  

global server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("", 8000))
server.listen(5)
global desc
desc = [server]
while 1:
 accept_new_connection()
 (sread, swrite, sexc) = select.select(desc, [], [])
 for sock in sread:
     if sock != server:
         flag = get_msg(sock)
         if flag:
             broadcast(flag, sock)



global server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("", 8000))
server.listen(5)
global desc
desc = [server]
while 1:
 accept_new_connection()
 (sread, swrite, sexc) = select.select(desc, [], [])
 for sock in sread:
     if sock != server:
         flag = get_msg(sock)
         if flag:
             broadcast(flag, sock)