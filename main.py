import flask
from flask import request, session, redirect, send_file
import sqlite3


app = flask.Flask(__name__)
db = db = sqlite3.connect('db/agtdb.db', check_same_thread=False)

''' inventario '''

@app.route('/')
def index():
    cur = db.cursor()
    cur.execute('select * from inventario')
    data = cur.fetchall()
    print(data)
    return flask.render_template('inventario2.html', data=data)





'''cargar un elemento a la db'''

@app.route('/agregar', methods= ['GET','POST'])
def agregar():
    if request.method == 'POST':
            producto = request.form['producto']
            marca = request.form['marca']
            stock = int(request.form['stock'])
            ubicacion = request.form['deposito']
            nota = request.form['nota']
            cur = db.cursor()
            cur.execute(f"insert into inventario (producto,marca,stock,ubicacion,nota) values('{producto}','{marca}',{stock},'{ubicacion}','{nota}')") #carga los datos provinientes del frontend
            db.commit()
            return redirect('/')
    else:
        return flask.render_template('cargar.html')





'''actualizar un elemnto de la db''' #agregar una tabla de notas con fecha de cada nota agregada

@app.route('/actualizar', methods=['GET','POST'])
def update():
    if request.method == 'POST':
        producto = request.form['producto']
        marca = request.form['marca']
        stock = request.form['stock']
        ubicacion = request.form['ubicacion']
        nota = request.form['nota']
        id = request.form['id']
        cur = db.cursor()
        cur.execute("UPDATE inventario SET producto = ?, marca = ?, stock = ?, ubicacion = ? WHERE id = ?", 
            (producto, marca, stock, ubicacion, id))
        db.commit()
        return redirect('/')
    id = int(request.args.get('id'))
    cur = db.cursor()
    cur.execute(f"select * from inventario where id = {id}")
    data = cur.fetchall()
    print(data)
    return flask.render_template('actualizar2.html',dato=data[0])


#elimina un elemento de la db

@app.route('/eliminar')
def eliminar():
    id = request.args.get('id')
    id = int(id)
    cur = db.cursor()
    cur.execute(f"delete FROM inventario WHERE id={id}")
    db.commit()
    return redirect('/')




if __name__ == '__main__':
    app.run(debug=True)