from flask import Flask, request, jsonify
import json
import threading
import base64
import datetime

from bd import BasedeDatos

app = Flask(__name__)
 
BD = BasedeDatos()
BD.Conectar()

def shutdown_server():
	func = request.environ.get('werkzeug.server.shutdown')
	if func is None:
		raise RuntimeError('Not running with the Werkzeug Server')
	func()

@app.route('/shutdown', methods=['GET'])
def shutdown():
	shutdown_server()
	return 'Server shutting down...'		
 
@app.route("/authenticate", methods=['POST'])
def autenticacion():
	Json =  request.get_json(force=True)
	print type(Json)
	print Json['code']
	code = Json['code']

	Codigo = BD.Seleccionar('SELECT TOP 1 id,relacion,type,fecha FROM t365_AuthWebApiMobile WHERE codigo = ?',code)
	if Codigo:
		if Codigo[0].type == 1:
			Datos = BD.Seleccionar("""SELECT TOP 1 t365_Usuarios.id, t365_EmpresasParametros.webServiceCall, t365_EmpresasParametros.webServiceSMS FROM t365_Clientes INNER JOIN t365_Usuarios ON t365_Clientes.id_cliente = t365_Usuarios.id_cliente LEFT OUTER JOIN t365_EmpresasParametros ON t365_Clientes.id_empresa = t365_EmpresasParametros.id_empresa WHERE (t365_Usuarios.id = ?)""",Codigo[0].relacion)

			respuesta = {'error':False,'mensaje':'OK','data':{'type':'user','id':int(Datos[0].id),'sms':"'"+str(Datos[0].webServiceSMS)+"'",'telf':"'"+str(Datos[0].webServiceCall)+"'",'tracker':int(300)}}
			
			return json.dumps(respuesta)

		elif Codigo[0].type == 2:
			Datos = BD.Seleccionar("""SELECT TOP 1 t365_Clientes.id_cliente, t365_EmpresasParametros.webServiceCall, t365_EmpresasParametros.webServiceSMS FROM t365_Clientes LEFT OUTER JOIN t365_EmpresasParametros ON t365_Clientes.id_empresa = t365_EmpresasParametros.id_empresa WHERE t365_Clientes.id_cliente = ? """,Codigo[0].relacion)
			respuesta = {'error':False,'mensaje':'OK','data':{'type':'guard','id':int(Datos[0].id_cliente),'sms':"'"+str(Datos[0].webServiceSMS)+"'",'telf':"'"+str(Datos[0].webServiceCall)+"'",'tracker':int(300)}}
			return json.dumps(respuesta)
	respuesta = {'error':True,'mensaje':'ERROR'}
	return jsonify(respuesta)

@app.route("/action/panic", methods=['POST'])
def panico():
	values = request.get_json(force=True)
	print values
	if 'type' in values and 'id' in values and 'latitud' in values and 'longitud' in values and 'data' in values and 'fecha' in values:
		print 'ok aqui'
		if values['type'] == 'user':
			print 'panicousuario'
			if values['id'] == '10' or values['id'] == 10:
				print type(values['id'])
				print 'entre en usuario 10'
				respuesta = {'error':False,'mensaje':'OK','tracker':int(300)}
			else:
				respuesta = {'error':True,'mensaje':'InvalidID'}
		elif values['type'] == 'guard':
			if values['id'] == '1':
				respuesta = {'error':False,'mensaje':'OK','tracker':int(300)}
			else:
				respuesta = {'error':True,'mensaje':'InvalidID'}
	else:
		respuesta = {'error':True,'mensaje':'InvalidCommand'}

	return jsonify(respuesta)

@app.route("/action/fire", methods=['POST'])
def fuego():
	values = request.get_json(force=True)
	print values
	if 'type' in values and 'id' in values and 'latitud' in values and 'longitud' in values and 'data' in values and 'fecha' in values:
		print 'ok aqui'
		if values['type'] == 'user':
			print 'panicousuario'
			if values['id'] == '10' or values['id'] == 10:
				print type(values['id'])
				print 'entre en usuario 10'
				respuesta = {'error':False,'mensaje':'OK','tracker':int(300)}
			else:
				respuesta = {'error':True,'mensaje':'InvalidID'}
		elif values['type'] == 'guard':
			if values['id'] == '1' or values['id'] == 1:
				respuesta = {'error':False,'mensaje':'OK','tracker':int(300)}
			else:
				respuesta = {'error':True,'mensaje':'InvalidID'}
	else:
		respuesta = {'error':True,'mensaje':'InvalidCommand'}

	return jsonify(respuesta)


	#BD.Insertar("exec t365_InsertarTramaWebApiMobile ?,?,?,?,?,?,?,?,?,?,?", ColaParaGuardarSenalSistema.pop(0))

@app.route("/action/medic", methods=['POST'])
def medica():
	values = request.get_json(force=True)
	print values
	if 'type' in values and 'id' in values and 'latitud' in values and 'longitud' in values and 'data' in values and 'fecha' in values:
		print 'ok aqui'
		if values['type'] == 'user':
			print 'panicousuario'
			if values['id'] == '10' or values['id'] == 10:
				print type(values['id'])
				print 'entre en usuario 10'
				respuesta = {'error':False,'mensaje':'OK','tracker':int(300)}
			else:
				respuesta = {'error':True,'mensaje':'InvalidID'}
		elif values['type'] == 'guard':
			if values['id'] == '1':
				respuesta = {'error':False,'mensaje':'OK','tracker':int(300)}
			else:
				respuesta = {'error':True,'mensaje':'InvalidID'}
	else:
		respuesta = {'error':True,'mensaje':'InvalidCommand'}

	return jsonify(respuesta)


	#BD.Insertar("exec t365_InsertarTramaWebApiMobile ?,?,?,?,?,?,?,?,?,?,?", ColaParaGuardarSenalSistema.pop(0))

@app.route("/action/tracker", methods=['POST'])
def gps():
	values = request.get_json(force=True)
	print values
	if 'type' in values and 'id' in values and 'latitud' in values and 'longitud' in values and 'data' in values and 'fecha' in values:
		print 'ok aqui'
		if values['type'] == 'user':
			print 'panicousuario'
			if values['id'] == '10' or values['id'] == 10:
				print type(values['id'])
				print 'entre en usuario 10'
				respuesta = {'error':False,'mensaje':'OK','tracker':int(300)}
			else:
				respuesta = {'error':True,'mensaje':'InvalidID'}
		elif values['type'] == 'guard':
			if values['id'] == '1':
				respuesta = {'error':False,'mensaje':'OK','tracker':int(300)}
			else:
				respuesta = {'error':True,'mensaje':'InvalidID'}
	else:
		respuesta = {'error':True,'mensaje':'InvalidCommand'}

	return jsonify(respuesta)

@app.route("/action/cancel", methods=['POST'])
def cancelar():
	values = request.get_json(force=True)
	print values
	if 'type' in values and 'id' in values and 'latitud' in values and 'longitud' in values and 'data' in values and 'fecha' in values:
		print 'ok aqui'
		if values['type'] == 'user':
			print 'panicousuario'
			if values['id'] == '10' or values['id'] == 10:
				print type(values['id'])
				print 'entre en usuario 10'
				respuesta = {'error':False,'mensaje':'OK','tracker':int(300)}
			else:
				respuesta = {'error':True,'mensaje':'InvalidID'}
		elif values['type'] == 'guard':
			if values['id'] == '1':
				respuesta = {'error':False,'mensaje':'OK','tracker':int(300)}
			else:
				respuesta = {'error':True,'mensaje':'InvalidID'}
	else:
		respuesta = {'error':True,'mensaje':'InvalidCommand'}

	return jsonify(respuesta)

@app.route("/action/read", methods=['POST'])
def lectura():
	values = request.get_json(force=True)
	print values
	if 'type' in values and 'id' in values and 'latitud' in values and 'longitud' in values and 'data' in values and 'fecha' in values:
		print 'ok aqui'
		if values['type'] == 'user':
			print 'panicousuario'
			if values['id'] == '10' or values['id'] == 10:
				print type(values['id'])
				print 'entre en usuario 10'
				respuesta = {'error':False,'mensaje':'OK','tracker':int(300)}
			else:
				respuesta = {'error':True,'mensaje':'InvalidID'}
		elif values['type'] == 'guard':
			if values['id'] == '1':
				respuesta = {'error':False,'mensaje':'OK','tracker':int(300)}
			else:
				respuesta = {'error':True,'mensaje':'InvalidID'}
	else:
		respuesta = {'error':True,'mensaje':'InvalidCommand'}

	return jsonify(respuesta)

@app.route("/action/callme", methods=['POST'])
def llamame():
	values = request.get_json(force=True)
	print values
	if 'type' in values and 'id' in values and 'latitud' in values and 'longitud' in values and 'data' in values and 'fecha' in values:
		print 'ok aqui'
		if values['type'] == 'user':
			print 'panicousuario'
			if values['id'] == '10' or values['id'] == 10:
				print type(values['id'])
				print 'entre en usuario 10'
				respuesta = {'error':False,'mensaje':'OK','tracker':int(300)}
			else:
				respuesta = {'error':True,'mensaje':'InvalidID'}
		elif values['type'] == 'guard':
			if values['id'] == '1':
				respuesta = {'error':False,'mensaje':'OK','tracker':int(300)}
			else:
				respuesta = {'error':True,'mensaje':'InvalidID'}
	else:
		respuesta = {'error':True,'mensaje':'InvalidCommand'}

	return jsonify(respuesta)

@app.route("/action/callyou", methods=['POST'])
def llamar():
	values = request.get_json(force=True)
	print values
	if 'type' in values and 'id' in values and 'latitud' in values and 'longitud' in values and 'data' in values and 'fecha' in values:
		print 'ok aqui'
		if values['type'] == 'user':
			print 'panicousuario'
			if values['id'] == '10' or values['id'] == 10:
				print type(values['id'])
				print 'entre en usuario 10'
				respuesta = {'error':False,'mensaje':'OK','tracker':int(300)}
			else:
				respuesta = {'error':True,'mensaje':'InvalidID'}
		elif values['type'] == 'guard':
			if values['id'] == '1':
				respuesta = {'error':False,'mensaje':'OK','tracker':int(300)}
			else:
				respuesta = {'error':True,'mensaje':'InvalidID'}
	else:
		respuesta = {'error':True,'mensaje':'InvalidCommand'}

	return jsonify(respuesta)
@app.route("/action/image", methods=['POST'])
def foto():
	values = request.get_json(force=True)
	print values
	if 'type' in values and 'id' in values and 'latitud' in values and 'longitud' in values and 'data' in values and 'fecha' in values:
		print 'VOY A GUARDAR IMAGEN'
		foto = values['data']
		imgdata = base64.b64decode(foto)
		filename = str(values['id'])+str(values['type'])+datetime.datetime.now().strftime("%d_%b_%Y_%H_%M_%S")+str('.jpg')
		print 'Ya tiene nombre'
		print filename
		with open(filename, 'wb') as f:
		    f.write(imgdata)
		print 'ok aqui'
		if values['type'] == 'user':
			print 'panicousuario'
			if values['id'] == '10' or values['id'] == 10:
				print type(values['id'])
				print 'entre en usuario 10'
				respuesta = {'error':False,'mensaje':'OK','tracker':int(300)}
			else:
				respuesta = {'error':True,'mensaje':'InvalidID'}
		elif values['type'] == 'guard':
			if values['id'] == '1':
				respuesta = {'error':False,'mensaje':'OK','tracker':int(300)}
			else:
				respuesta = {'error':True,'mensaje':'InvalidID'}
	else:
		respuesta = {'error':True,'mensaje':'InvalidCommand'}

	return jsonify(respuesta)


@app.route("/action/logout", methods=['POST'])
def logout():
	values = request.get_json(force=True)
	print values
	if 'type' in values and 'id' in values and 'latitud' in values and 'longitud' in values and 'data' in values and 'fecha' in values:
		print 'ok aqui'
		if values['type'] == 'user':
			print 'panicousuario'
			if values['id'] == '10' or values['id'] == 10:
				print type(values['id'])
				print 'entre en usuario 10'
				respuesta = {'error':False,'mensaje':'OK','tracker':int(300)}
			else:
				respuesta = {'error':True,'mensaje':'InvalidID'}
		elif values['type'] == 'guard':
			if values['id'] == '1':
				respuesta = {'error':False,'mensaje':'OK','tracker':int(300)}
			else:
				respuesta = {'error':True,'mensaje':'InvalidID'}
	else:
		respuesta = {'error':True,'mensaje':'InvalidCommand'}

	return jsonify(respuesta)

	#BD.Insertar("exec t365_InsertarTramaWebApiMobile ?,?,?,?,?,?,?,?,?,?,?", ColaParaGuardarSenalSistema.pop(0))

app.run(host='0.0.0.0')



#if __name__ == "__main__":
#a = threading.Thread(target=lanzar)
#app.run()


