from flask import Flask, render_template
import csv

app= Flask(__name__)

@app.route('/')
def index():
    f =  open('movements.txt', 'r')
    reader = csv.reader(f, delimiter=',', quotechar='"')
    movements =  list(reader)
    return render_template('index.html', mvm=movements)