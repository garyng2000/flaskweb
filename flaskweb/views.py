"""
Routes and views for the flask application.
"""
import sys
from os import environ
from datetime import datetime
from flask import render_template, Response, current_app
from flaskweb import app
import pyodbc

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template('index.html',
        title='Home Page',
        year=datetime.now().year,)

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template('contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.')

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template('about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.')
@app.route('/hello')
def test():
    return Response(sql_query(),  mimetype='text/plain')

def sql_query():
    try:
        with app.app_context():
            app_root_path = current_app.root_path
            yield app_root_path + '\n'
        connection_string = environ.get('ODBC_CONNECTION_STRING','DRIVER={ODBC Driver 17 for SQL Server};SERVER=db;DATABASE=OASDesign;UID=sa')
        pwd = ';PWD=password'
        conn = pyodbc.connect(connection_string + pwd)
        cursor = conn.cursor()
        cursor.execute("SELECT UsrId, UsrName FROM dbo.Usr") 
        yield format(cursor.description) + '\n'
        for data in cursor.fetchall():
            yield '{0.UsrId} - {0.UsrName}'.format(data) + '\n'
        params = (1,1,1,1)
        cursor.execute("{CALL dbo.GetUsrPref(?,?,?,?)}",params)
        yield format(cursor.description) + '\n'
        for data in cursor.fetchall():
            yield format(data) + '\n'
        conn.close()
        yield "ODBC_CONNECTION_STRING: {0}".format(connection_string + pwd)    
    except Exception as err:
        #return to client - only for debugging
        yield f"{err.__class__.__name__}: {err}"
        #let general exception handling handle it(log etc.)
        raise err
