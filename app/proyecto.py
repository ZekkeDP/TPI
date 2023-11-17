from flask import (
    Blueprint, render_template, request, url_for, redirect, abort
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

login = False


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

    return render_template('proyecto/propuestas.html', propuestas=propuestas)

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
