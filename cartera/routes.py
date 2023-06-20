from cartera import app
from flask import render_template, request, redirect
import csv
@app.route('/')
def index():
    f =  open('movements.dat', 'r')
    reader = csv.DictReader(f, delimiter=',', quotechar='"')
    movements =  list(reader)
    return render_template('index.html', mvm=movements)

@app.route('/new-movement', methods=['GET','POST'])
def new_movement():
    if request.method == 'GET':
    
        return render_template('new.html')
    else:
        data = request.form
        f = open('movements.dat','a')
        writer = csv.DictWriter(f, fieldnames=data.keys())
        writer.writerow(data)
        f.close()

        return redirect('/')

