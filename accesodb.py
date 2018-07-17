from flask import Flask, request, render_template, current_app, send_file
import MySQLdb
import xlwt
from datetime import time, date, datetime, timedelta
from pytz import timezone
import json
app = Flask(__name__)
var_gl = 0

workbook = xlwt.Workbook()
sheet = workbook.add_sheet("Historico",cell_overwrite_ok=True) # name of the worksheet

with open("datos_acceso_db.json", "r") as archivo_datos:
	datos_db = json.load(archivo_datos)
	db = MySQLdb.connect(host= datos_db["host"],
	                     user= datos_db["user"],
        	             passwd= datos_db["passwd"],
                	     db= datos_db["db"])

cur = db.cursor()

#db.close()
@app.route("/download")
def return_files_tut():
	try:
		return send_file('/home/ec2-user/literate-garbanzo/test.xls', attachment_filename='test.xls')
	except Exception as e:
		return str(e)

@app.route("/link", methods = ['GET','POST'])
def funcion_html():

	if request.method == 'POST':
		desde = request.form['desde']
		hasta = request.form['hasta']
		#print (desde)
		#print (hasta)

		cur.execute("SELECT data,datetime FROM Valores WHERE DATE(datetime) >= '{0}' AND DATE(datetime) <= '{1}'".format(desde,hasta))
		rowNum = 1 #keep track of rows
		colNum = 0 #keep track of columns

		sheet.write(0, 0, 'Valor')
		sheet.write(0, 1, 'Fecha y hora')
		# print all the cells of the row to excel sheet
		for row in cur.fetchall() :
			colNum = 0
			for item in row:
				sheet.write(rowNum, colNum,str(item)) # row, column, value
				colNum = colNum + 1
			rowNum = rowNum + 1

		workbook.save("test.xls")

		try:
                	return send_file('/home/ec2-user/literate-garbanzo/test.xls', attachment_filename='test.xls')

        	except Exception as e:
                	return str(e)

	return render_template('calendar1.html')

@app.route("/historico", methods = ['GET','POST'])
def select_datos():

	tam = 20
	global var_gl
	if request.method == 'POST':
		indice_tabla = request.form['indice']
		fecha = request.form['fecha']
		var_gl = var_gl + int(indice_tabla)
		if var_gl < 0: var_gl = 0

		#fecha = request.form['fecha']

	diff = timedelta(days=3)
        fmt = "%Y-%m-%d"
        ahora = datetime.now(timezone('America/Buenos_Aires')) - diff
        hoy =  ahora.strftime(fmt)
	print(fecha)

	cur.execute("SELECT data FROM Valores WHERE DATE(datetime) = '{0}' ORDER BY ID DESC LIMIT {1},{2}".format(hoy, var_gl, tam))
	dato = cur.fetchall()
	temperaturas = []
	for elem in dato:
		for subelem in elem:
			temperaturas.insert(0,subelem)
	#print(temperaturas)

	cur.execute("SELECT TIME(datetime) FROM Valores WHERE DATE(datetime) = '{0}' ORDER BY ID DESC LIMIT {1},{2}".format(hoy, var_gl,tam))
        datodt = cur.fetchall()
	print(datodt)
	times = []
	for ele in datodt:
		for subele in ele:
			if subele != None:
				valortimedel = subele
				valor = (datetime.min + valortimedel).time()
				times.insert(0,valor)
	#print(hoy)
	#print (times)

	return render_template('time_chart.html', values=temperaturas, labels=times, legend="Temperaturas", datenow=hoy)

@app.route('/')
def index():
	return render_template ('test.html', name='Pablinchex')

@app.route('/setTemp', methods = ['POST'])
def guardar_parametros():

	req_data = request.get_json()

	id = req_data['id']
	mac = req_data['mac']
	valor = req_data['valor']*0.1

	#fmt = "%Y-%m-%d %H:%M:%S"
	ahora = datetime.now(timezone('America/Buenos_Aires'))
        #ahora_f =  ahora.strftime(fmt)
	print(mac)

	try:
		cur.execute("INSERT INTO Valores (data,datetime) VALUES(%s,%s)",(valor,ahora))
		db.commit()
	except:
		db.rollback()

	return format(valor)

if __name__ == "__main__":
        app.debug = True
        app.run(host='0.0.0.0', port=5000)
