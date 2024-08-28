import sqlite3


db = sqlite3.connect('db/agtdb.db', check_same_thread=False)

''' LLamado simple a la base de datos obteniendo los productos dependiendo la cantidad necesitada
recibiendo en el parametro n como dato desde el backend del main. '''
def get_index(n): #obtener datos de unicio.
    list=[1,0]
    if n in list:
        cur = db.cursor()
        cur.execute(f'select * from inventario where stock >= {n}')
        data = cur.fetchall()
    return data

def get_ubicacion(ubi):
    print(ubi)
    print(type(ubi))
    cur = db.cursor()
    #cur.execute(f'select * from inventario where ubicacion = {ubi}')
    cur.execute('select * from inventario where ubicacion = ?', (ubi,))
    data = cur.fetchall()
    return data

def delete(id):# Elimina un elemento del inventario segun el ID
    cur = db.cursor()
    cur.execute(f"delete FROM inventario WHERE id={id}")
    db.commit()
