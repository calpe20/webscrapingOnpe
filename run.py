#Flask es un microframework web
from flask import Flask
from flask import render_template, request
import urllib2
#libreia para hacer web scraping
from BeautifulSoup import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('form_miembro.html')

@app.route('/miembrodemesa', methods=['GET','POST'])
def miembrodemesa():
	error = None
	if request.method=='POST':
		dni = request.form['dni']
        # Esta es la url donde jalo la informaciond e donde me toca dufragar
        # pasando un parametro como es el numero de DNI.
		url = "http://www.infogob.com.pe/ERM_2014/ficha.aspx?IdDni="+dni+"&IdTab=1"
        #traemos la web
		page = urllib2.urlopen(url).read()
		soup = BeautifulSoup(page)
        # dentro del codigo html buscamos un div con su id "conten-nombre"
        # y solo extraemos los textos planos sin las etiquetas html el nombre los camp
		nombre = soup.find(id='content-nombre').text
		links = soup.find(id='content-datos-right')
        #nos damos cuenta que dentro del DIv hay varios td, entonces buscamos todos los td
        # y lo capturamos en pagina
		pagina = links.findAll('td')
		tds = []
		limpio = []
		a = 0
        # y lo demas ya es historia. veanlo y analicenlo un poco.
		for dato in pagina:
			a += 1
			dato = dato.text
			titulo=''
			if dato == ":" or dato == "DISTRITO" or dato == "MIEMBRO DE MESA" or a == 4 or a == 7 or a == 10:
				pass
			else:
				if a == 3:
					titulo = 'DISTRITO\t\t\t: '
				elif a == 6:
					titulo = 'MESA DE VOTACION  : '
				elif a == 9:
					titulo = 'LUGAR DE VOTACION : '
				elif a == 12:
					titulo = 'DIRECCION         : '
				elif a == 15:
					titulo = 'MIEMBRO DE MESA   : '
				guardar = titulo+dato	
				limpio.append(guardar) 
		return render_template('miembrodemesa.html',data=limpio, nombre=nombre)
	else:
		return url_for('index')

if __name__=='__main__':
	app.run(host='0.0.0.0', debug=True, port=8080)
