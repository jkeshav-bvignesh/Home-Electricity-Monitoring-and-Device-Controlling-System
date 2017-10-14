from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify
import sqlite3 as sql
import os
import requests
import json
import pandas as pd
from flask_cors import CORS, cross_origin
from sklearn.neural_network import MLPRegressor
import numpy as np


def insert_db_for_retrain(test,result):
    with sql.connect("ECOSENSE.db") as conn:
        curs = conn.cursor()
        curs.execute('''insert into Readings values(DateTime('now','localtime'),? ,? ,? ,?);''',(result, test[0], test[1], test[2]))


class data_analysis:
    clf=0
    quota = 100
    username = "admin"
    phone = "99999999"
    password = "admin"
    b1 = "false"
    b2 = "true"
    b3 = "false"
    def setQuota(self, newVal):
        self.quota = newVal

    def getQuota(self):
        return self.quota

    def setUsername(self, newVal):
        self.username = newVal

    def getUsername(self):
        return self.username
    
    def setPassword(self, newVal):
        self.password = newVal

    def getPassword(self):
        return self.password
    
    def setPhone(self, newVal):
        self.phone = newVal

    def getPhone(self):
        return self.phone

    def setbutton(self, newVal):
        self.b1 = newVal[0]
        self.b2 = newVal[1]
        self.b3 = newVal[2]

    def getbutton(self):
        b = [self.b1]
        b.append(self.b2)
        b.append(self.b3)
        return b
		
def set_quota(newVal):
    analyse_object.setQuota(newVal)

def get_quota():
    return analyse_object.getQuota();

def set_username(newVal):
    analyse_object.setUsername(newVal)

def get_username():
    return analyse_object.getUsername();

def set_password(newVal):
    analyse_object.setPassword(newVal)

def get_password():
    return analyse_object.getPassword();

def set_phone(newVal):
    analyse_object.setPhone(newVal)

def get_phone():
    return analyse_object.getPhone();

def set_button(newVal):
    analyse_object.setbutton(newVal)

def get_button():
    return analyse_object.getbutton();

analyse_object=data_analysis()
analyse_object.getQuota() 
      
app = Flask(__name__)
CORS(app)
print('Server started')

@app.route('/login', methods=['GET','POST'])
def login_page():
	if request.form['password'] == get_password() and request.form['username']==get_username():
		session['logged_in'] = True
	else:
		flash('Please check the username and password and try again')
	return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    flash('Successfully logged out. Please log in again to access dashboard.')
    return home()

@app.route('/')
@cross_origin()
def home():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		return render_template('t_index.html')	
       
@app.route('/morrisdata', methods=['GET'])
def morissis():
        with sql.connect("ECOSENSE.db") as conn:
                curs = conn.cursor()
                df = pd.read_sql_query("SELECT date,inner,outer,humidity FROM Readings LIMIT 10 OFFSET(SELECT COUNT(*) FROM Readings) - 10;", conn)
                jsondata1 = df.to_json(orient = 'records')
                df2 = pd.read_sql_query("SELECT date,inner,prefered FROM Readings LIMIT 10 OFFSET(SELECT COUNT(*) FROM Readings) - 10;", conn)
                jsondata2 = df2.to_json(orient = 'records')
                jsonpacked = {
                                'graph1':json.loads(jsondata1),
                                'graph2':json.loads(jsondata2)
                             }
        return jsonify(jsonpacked)


@app.route('/setnewquota', methods=['POST'])
def setNewQuota():
    new_quota = request.form['quota']
    print("New Quota: ", new_quota)
    set_quota(new_quota)
    val = 1
    jdata ={
        'val': val
        }
    return jsonify(jdata)

@app.route('/getquota', methods=['GET'])
def getQuota():
    val = get_quota()
    jdata ={
        'val': val
        }
    return jsonify(jdata)

@app.route('/setdetails', methods=['POST'])
def setDetails():
    new_uname = request.form['username']
    new_phone = request.form['phone']
    set_username(new_uname)
    set_phone(new_phone)
    val = 1
    jdata ={
        'val': val
        }
    return jsonify(jdata)

@app.route('/getdetails', methods=['GET'])
def getDetails():
    uname = get_username()
    phone = get_phone()
    jdata ={
        'username': uname,
        'phone':phone
        }
    return jsonify(jdata)

@app.route('/setbuttonstate', methods=['POST'])
def setButton():
    new_b1 = request.form['b1']
    new_b2 = request.form['b2']
    new_b3 = request.form['b3']
    b = [new_b1]
    b.append(new_b2)
    b.append(new_b3)
    set_button(b)
    val = 1
    jdata ={
        'val': val
        }
    return jsonify(jdata)

@app.route('/getbuttonstate', methods=['GET'])
def getButton():
    b = get_button()
    jdata ={
        'b1': b[0],
	'b2': b[1],
        'b3': b[2]
        }
    return jsonify(jdata)

if __name__=='__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True, port=9000, host='0.0.0.0',use_reloader=False)
