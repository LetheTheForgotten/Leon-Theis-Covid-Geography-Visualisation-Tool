"""
Routes and views for the flask application.
"""


from datetime import datetime
from flask import render_template, send_file
from RKIDataViz_Backend import app






#chromium breaks without this header
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response



@app.route('/')
def home():
    return render_template('index.html') 

@app.route('/<file>')
def staticFix(file):
    if(file=="graph" or  file=="table"):
        return render_template('index.html') 
    return send_file('templates/'+file)


