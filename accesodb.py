from flask import Flask, request, render_template
import MySQLdb
from datetime import time, date, datetime
from pytz import timezone
import json

app = Flask(__name__)

with open("datos_acceso_db.json", "r") as archivo_datos:
	datos_db = json.load(archivo_datos)
	db = MySQLdb.connect(host= datos_db["host"],
                     user= datos_db["user"],
                     passwd= datos_db["passwd"],
                     db= datos_db["db"])

cur = db.cursor()

#db.close()
@app.route("/historico")
def select_datos():

	cur.execute("SELECT data FROM Valores ORDER BY ID DESC LIMIT 18")
	dato = cur.fetchall()
	temperaturas = []
	for elem in dato:
		for subelem in elem:
			temperaturas.insert(0,subelem)
	#print(temperaturas)

	cur.execute("SELECT TIME(datetime) FROM Valores ORDER BY ID DESC LIMIT 18")
        datodt = cur.fetchall()
	times = []
	for ele in datodt:
		for subele in ele:
			if subele != None:
				valortimedel = subele
				valor = (datetime.min + valortimedel).time()
				times.insert(0,valor)
	#print (times)

	return render_template('time_chart.html', values=temperaturas, labels=times, legend="Temperaturas")

@app.route("/time_chart")
def time_chart():
    legend = 'Temperaturas'
    temperatures = [73.7, 73.4, 73.8, 72.8, 68.7, 65.2,
                    61.8, 58.7, 58.2, 58.3, 60.5, 65.7,
                    70.2, 71.4, 71.2, 70.9, 71.3, 71.1]
    times = [time(hour=11, minute=14, second=15),
             time(hour=11, minute=14, second=30),
             time(hour=11, minute=14, second=45),
             time(hour=11, minute=15, second=00),
             time(hour=11, minute=15, second=15),
             time(hour=11, minute=15, second=30),
             time(hour=11, minute=15, second=45),
             time(hour=11, minute=16, second=00),
             time(hour=11, minute=16, second=15),
             time(hour=11, minute=16, second=30),
             time(hour=11, minute=16, second=45),
             time(hour=11, minute=17, second=00),
             time(hour=11, minute=17, second=15),
             time(hour=11, minute=17, second=30),
             time(hour=11, minute=17, second=45),
             time(hour=11, minute=18, second=00),
             time(hour=11, minute=18, second=15),
             time(hour=11, minute=18, second=30)]
    return render_template('time_chart.html', values=temperatures, labels=times, legend=legend)
@app.route("/line_chart")
def line_chart():
    legend = 'Temperaturas'
    temperatures = [73.7, 73.4, 73.8, 72.8, 68.7, 65.2,
                    61.8, 58.7, 58.2, 58.3, 60.5, 65.7,
                    70.2, 71.4, 71.2, 70.9, 71.3, 71.1]
    times = ['12:00PM', '12:10PM', '12:20PM', '12:30PM', '12:40PM', '12:50PM',
             '1:00PM', '1:10PM', '1:20PM', '1:30PM', '1:40PM', '1:50PM',
             '2:00PM', '2:10PM', '2:20PM', '2:30PM', '2:40PM', '2:50PM']
    return render_template('line_chart.html', values=temperatures, labels=times, legend=legend)


@app.route("/simple_chart")
def chart():
    legend = 'Monthly Data'
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]
    return render_template('chart.html', values=values, labels=labels, legend=legend)

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
