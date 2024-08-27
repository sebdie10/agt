import flask
from flask import request, session, redirect, send_file
import sqlite3
from datetime import datetime
from werkzeug.utils import secure_filename
import os


app = flask.Flask(__name__)
db = sqlite3.connect('db/agtdb.db', check_same_thread=False)


app.secret_key = 'cortina'
app.config['ruta_imagen'] = 'static/img/productos/'




def guardar_imagen(file): #guarda la imagen en la carpeta raiz imagenes
  basepath = os.path.dirname(__file__)
  filename = secure_filename(file.filename)
  extension = os.path.splitext(filename)[1]
  nuevoNombreFile = filename[0] + extension

  # Verificar si el archivo ya existe en el directorio
  while os.path.exists(os.path.join(basepath, app.config['ruta_imagen'], nuevoNombreFile)):
      # Si el archivo existe, agregar un sufijo numérico al nombre del archivo
      nombre_base, extension = os.path.splitext(nuevoNombreFile)
      contador = 1
      nuevoNombreFile = f"{nombre_base}_{contador}{extension}"
      contador += 1

  upload_path = os.path.join(basepath, app.config['ruta_imagen'], nuevoNombreFile)
  file.save(upload_path)
  return nuevoNombreFile



def guardar_imagen_(file): #guarda la imagen en la carpeta raiz imagenes no utilizable
  #Script para archivo

  basepath = os.path.dirname(
      __file__)  #La ruta donde se encuentra el archivo actual
  filename = secure_filename(file.filename)  #Nombre original del archivo

  #capturando extensión del archivo ejemplo: (.png, .jpg, .pdf ...etc)
  extension = os.path.splitext(filename)[1]
  nuevoNombreFile = filename[0] + extension
  print(nuevoNombreFile)

  upload_path = os.path.join(basepath, app.config['ruta_imagen'],
                             nuevoNombreFile)
  file.save(upload_path)
  return nuevoNombreFile


#Redireccionando cuando la página no existe
@app.errorhandler(404)
def not_found(error):
  return flask.render_template('404.html')





''' inventario '''  

@app.route('/') #pagina de inicio y carga de la tabla inventario
def index():
  if 'operador' in session:
    user_agent = request.headers.get('User-Agent')
    if 'Mobile' in user_agent:
        cur = db.cursor()
        cur.execute('select * from inventario where stock >= 1')
        data = cur.fetchall()
        return flask.render_template('inventario-mobile.html', data=data)
    else:
      if 'stock_cero' in  session and session['stock_cero'] == 'desactivado':
        cur = db.cursor()
        cur.execute('select * from inventario where stock >= 1')
        data = cur.fetchall()
        return flask.render_template('inventario2.html', data=data, stock='desactivado')
      elif 'stock_cero' in session and session['stock_cero']== 'activado':
        cur = db.cursor()
        cur.execute('select * from inventario')
        data = cur.fetchall()
        #print(data)
        return flask.render_template('inventario2.html', data=data, stock='activado')
      else:
        cur = db.cursor()
        cur.execute('select * from inventario')
        data = cur.fetchall()
        return flask.render_template('inventario2.html', data=data, stock='activado')
  else:
      return redirect('/log')







'''cargar un elemento a la db'''


@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
  if request.method == 'POST':
    producto = request.form['producto']
    marca = request.form['marca']
    stock = int(request.form['stock'])
    ubicacion = request.form['deposito']
    nota = request.form['nota']

    file = request.files['imagen']
    if str(file) != "<FileStorage: '' ('application/octet-stream')>":
      imagen = guardar_imagen(file)
      cur = db.cursor()
      cur.execute(
          f"insert into inventario (producto,marca,stock,ubicacion,nota,imagen) values('{producto}','{marca}',{stock},'{ubicacion}','{nota}','{imagen}')"
      )  #carga los datos provinientes del frontend
      db.commit()
    else:
      cur = db.cursor()
      cur.execute(
          f"insert into inventario (producto,marca,stock,ubicacion,nota) values('{producto}','{marca}',{stock},'{ubicacion}','{nota}')"
      )  #carga los datos provinientes del frontend
      db.commit()
    return redirect('/')
  else:
    if 'operador' in session:
      return flask.render_template('cargar.html')
    else:
      return redirect('/log')






'''actualizar un elemnto de la db'''  #ya se agrego notas

@app.route('/actualizar', methods=['GET', 'POST'])
def update():
  if request.method == 'POST':
      producto = request.form['producto']
      marca = request.form['marca']
      stock = request.form['stock']
      ubicacion = request.form['ubicacion']
      nota = request.form['nota']
      id = request.form['id']
      try:
          file= request.files['imagen']
      except:
          file="<FileStorage: '' ('application/octet-stream')>"
      print(file)
      if str(file) != "<FileStorage: '' ('application/octet-stream')>":
          imagen= guardar_imagen(file)
          cur = db.cursor()
          cur.execute("UPDATE inventario SET producto = ?, marca = ?, stock = ?, ubicacion = ?, imagen=? WHERE id = ?", 
              (producto, marca, stock, ubicacion,imagen, id))
          fecha = datetime.now()
          fecha = str(fecha)
          cur.execute(f"insert into notas(producto_id,fecha,nota) values({id},'{fecha[0:10]}','{nota}')")
          db.commit()
      else:
          cur = db.cursor()
          cur.execute("UPDATE inventario SET producto = ?, marca = ?, stock = ?, ubicacion = ? WHERE id = ?", 
              (producto, marca, stock, ubicacion, id))
          fecha = datetime.now()
          fecha = str(fecha)
          tecnico = session['operador']
          cur.execute(f"insert into notas(producto_id,fecha,nota,tecnico) values({id},'{fecha[0:10]}','{nota}','{tecnico}')")
          db.commit()
      return redirect('/')
  id = int(request.args.get('id'))
  cur = db.cursor()
  cur.execute(f"select * from inventario where id = {id}")
  data = cur.fetchall()
  cur.execute(f"select * from notas where producto_id = {id} order by nota_id desc")
  notas = cur.fetchall()
  print(data, notas)
  return flask.render_template('actualizar2.html',dato=data[0], notas=notas)




#elimina un elemento de la db

@app.route('/eliminar') #Elimina un elemento de la db
def eliminar():
  id = request.args.get('id')
  id = int(id)
  cur = db.cursor()
  cur.execute(f"delete FROM inventario WHERE id={id}")
  db.commit()
  return redirect('/')


@app.route('/log', methods=['GET', 'POST']) #pagiina de logeo de usuarios
def login():
  if request.method == 'POST':
    usuario = request.form['usuario']
    contraseña = request.form['contrasena']
    #print(usuario, contraseña)
    if contraseña == '4v3ng3r5':
      print(usuario)
      session['operador'] = usuario
      print(session['operador'])
      return redirect('/')

  return flask.render_template('auth.html')


@app.route('/logout') #limpia todas laas variables sessions del navegador
def cerrar():
  print(f"{session['operador']} a salido de la session")
  session.clear()
  return redirect('/')


@app.route('/dbe', methods=['GET', 'POST'])
def editdb():
  if 'Diego' == session['operador']:
    if request.method == 'POST':
      consulta = request.form['consulta']
      print(consulta)
      cur = db.cursor()
      cur.execute(consulta)
      db.commit()
    return flask.render_template('execute.html')
  else:
    return redirect('/log')



@app.route('/dbv')
def select():
  if session['operador'] == 'Diego':  
   return flask.render_template('insert.html')
  else:
    return redirect('/logout')



@app.route('/stock') #controla si el usuario oculto los productos que tiene stock 0
def cambiarEstado():
    estado = request.args.get('estado')
    session['stock_cero']= estado
    return redirect('/')


if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')