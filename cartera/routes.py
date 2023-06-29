from cartera import app
from cartera.models import Movement, MovementDAO
from flask import render_template, request, redirect, flash, url_for
import csv

dao = MovementDAO('movements.dat')
@app.route('/')
def index():
    try:
        movements = dao.all()
        return render_template("index.html", the_movements=movements, title="Todos")
    except ValueError as e:
        flash("Su fichero de datos está corrupto")
        flash(str(e))
        return render_template("index.html", the_movements=[], title="Todos")


@app.route('/new_movement', methods=['GET','POST'])
def new_movement():
    if request.method == 'GET':
    
        return render_template('new.html', the_form = {})
    else:
        data = request.form
        try:
            dao.insert(Movement(data['date'], data['abstract'],data['amount'],data['currency']))
            return redirect('/')
        except ValueError as e:
            flash(str(e))
            return render_template('new.html', the_form = data)
        
@app.route('/update_movement/<int:pos>', methods=['GET', 'POST'])
def upd_mov(pos):
    if request.method == "GET":
        mov = dao.get(pos)
        return render_template('update.html', title="Moodificación de movimientos", the_form=mov, pos=pos)
    else:
        data = request.form
        try:
            mv = Movement(data['date'], data['abstract'],data['amount'],data['currency'])
            dao.update(pos, mv)
            return redirect(url_for('index'))
            
        except :
            
            pass


