from flask import (
    Blueprint, render_template, request, url_for, redirect, flash
)

import mysql.connector

midb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="TPI"
)

cursor = midb.cursor(dictionary=True)

bp = Blueprint('proyecto', __name__, url_prefix='/')

@bp.route('/', methods=['GET', 'POST'])

    
def index():
    return render_template('proyecto/index.html')

@bp.route('/mail', methods=['POST'])
def mail():
    if request.method == "POST":
        usuario = request.form['usuario']
        email = request.form['email']
        propuesta = request.form["propuesta"]
        sql = "insert into propuestas (usuario, email, propuesta) values (%s, %s, %s)"
        values = (usuario, email, propuesta)
        cursor.execute(sql, values)
        midb.commit()

    
    return render_template('proyecto/sent_mail.html')

@bp.route('/propuestas', methods=['GET'])
def propuestas():
    cursor.execute('select * from propuestas')
    propuestas = cursor.fetchall()
    cursor.execute('select * from respuestas')
    respuestas = cursor.fetchall()
    cursor.execute('select * from propuestas;')
    n = cursor.fetchall()
    print(n == [])

    return render_template('proyecto/propuestas.html', propuestas=propuestas, respuestas=respuestas, n = n)

@bp.route('/eliminar-propuesta/<id>')
def borrar_propuesta(id):
    cursor.execute(f"DELETE FROM propuestas WHERE id = {id}")
    midb.commit()
    

    return redirect(url_for('proyecto.propuestas'))

@bp.route('/editar/<id>', methods=['GET', 'POST'])
def editar_propuesta(id):
    if request.method == 'POST':
        usuario = request.form['usuario']
        email = request.form['email']
        propuesta = request.form['propuesta']
        sql = 'UPDATE propuestas SET usuario= %s, email = %s, propuesta = %s WHERE id = %s'
        values = (usuario, email, propuesta, id)
        cursor.execute(sql, values)
        midb.commit()

        return redirect(url_for('proyecto.propuestas'))

    return render_template('proyecto/editar.html', id = id)

@bp.route('/respuesta/<id>', methods=['POST'])
def respuesta(id):
    if request.method == 'POST':
        respuesta = request.form['respuesta']
        sql = 'insert into respuestas (id_propuesta, respuesta) values (%s, %s)'
        values = (id, respuesta)
        cursor.execute(sql, values)
        midb.commit()


    return redirect(url_for('proyecto.propuestas'))


@bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == "POST":
        usuario = request.form['usuario']
        email = request.form['email']
        password = request.form['password']
        sql = "insert into usuarios (usuario, email, contraseña) values (%s, %s, %s)"
        values = (usuario, email, password)
        cursor.execute(sql, values)
        midb.commit()

        return render_template('proyecto/login.html')

    return render_template('proyecto/registro.html')


@bp.route('/borrar-respuesta/<id>')
def borrar_respuesta(id):
    cursor.execute(f"DELETE FROM respuestas WHERE id = {id}")
    midb.commit()

    return redirect(url_for('proyecto.propuestas'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        contraseña = request.form['contraseña']
        cursor.execute('select * from usuarios')
        usuarios = cursor.fetchall()
        for usuario in usuarios:
            if usuario['email'] == email and usuario['contraseña'] == contraseña:
                current_user = email
                return render_template('proyecto/index.html', current_user = current_user)


    return render_template('proyecto/login.html')