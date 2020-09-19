from flask import Flask, render_template, request, redirect
from werkzeug import secure_filename
from flask import g, session
#from flask_session.__init__ import Session
from flask_session import Session


import csv
import os
from database_lib import *

def add_tutto(app):

    @app.route('/uploader_cat', methods = [ 'POST'])
    def recv_cat():
        if request.method == 'POST':
            f = request.files['file']
            if len(f.filename)>0:
                f.save('files/cat.csv')
        return ""
    
    @app.route('/uploader_sotto_cat', methods = [ 'POST'])
    def recv_sottocat():
        if request.method == 'POST':
            f = request.files['file']
            if len(f.filename)>0:
                f.save('files/sotto_cat.csv')
        return ""
    
    @app.route('/uploader_BOM', methods = [ 'POST'])
    def recv_bom():
        if request.method == 'POST':
            f = request.files['file']
            if len(f.filename)>0:
                f.save('files/boms/'+secure_filename(f.filename))
                dbm = DBmanager()
                succ,failed=dbm.read_eeschema_bom(secure_filename(f.filename))
        ret=""
        for fail,err in failed:
            ret+=str(fail)+"-----"+ str(err) + "<br>"
        ret+="NOW GOOD <br>"
        for success in succ:
            ret+=str(success)+"<br>"
        return ret


    @app.route('/gestionale')
    def gestionale():
        cat = request.args.get('cat', default=0, type=int)
        sottocat = request.args.get('sottocat', default=0, type=int)
        dbm = DBmanager()
        cats = dbm.get_categories()
        print(cats)
        if int(cat) != 0:
            subcats = dbm.get_sottocategories(cat)
            print(subcats)
        else:
            subcats = []
        #search products by category
        prod=dbm.search_product(id_cat=cat)
        rendered = render_template('gestionale.html', categorie=cats, selc=int(cat), sottocategorie=subcats, selsc=int(sottocat), products= prod)


        return rendered


