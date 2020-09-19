from flask import Flask, render_template, request, redirect
from werkzeug import secure_filename
from flask import g, session
from flask_session import Session


import csv
import os
from web_gestionale import *


app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)



@app.route('/board/<name>')
def showboard(name):
    if os.path.isfile('templates/'+name):
        return render_template(name)
    else:
        return "board not found" #404 page



#questo e' codice GET
@app.route('/')
def index():
    files=os.listdir('templates')
    things =[]
    for f in files:
        if f.startswith("board_"):
            things.append({"name":f})
    rendered = render_template('index.html', \
        title = "Boards", \
        people = things)
    return rendered
#aggiungere codice POST per free-movement
#aggiungere 4 frecce nel html che fanno le POST


@app.route('/assign_position')
def assign_position():
    return "questa scheda probabilmente non ha piu senso"


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        if len(f.filename)> 0:
            if f.filename.startswith("board_"):
                f.save("templates/"+secure_filename(f.filename))
            else:
                f.save("templates/board_"+secure_filename(f.filename))
    return redirect("/", code = 302)

@app.route('/component/<test>')
def component(test):
    print(test)
    c=test.split(',')
    if 'storage' not in session:
        session['storage']= StorageManager()
    session['storage'].show_storage_place(c[0],c[1])
    if 'on_led' not in session:
        session["on_led"] = None
    #global on_led
    old = session["on_led"]
    session["on_led"] = test
    #app.app_context().push()
    print ('it was %s now it is %s'%(str(old),str(session["on_led"])))
    return "ok"

add_tutto(app)
app.run(debug=True, port=80, host='0.0.0.0')

