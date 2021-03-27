"""
Routes and views for the flask application.
"""
import sys
import os
import tempfile
import shutil
from os import environ
from datetime import datetime
from flask import render_template, Response, current_app, request, jsonify
from flaskweb import app
from werkzeug.utils import secure_filename
import flaskweb.config as config
from .upload import allowed_file
from .helper import get_firebase_claim
from .service.hdwallet import new_wallet
import pyodbc
import simplejson as json
import flask_cors
#from google.appengine.ext import ndb
import google.auth.transport.requests
import google.oauth2.id_token
import flask_cors
import ipfshttpclient
import re

flask_cors.CORS(app)
HTTP_REQUEST = google.auth.transport.requests.Request()

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
def hello():
    return Response(sql_query(),  mimetype='text/plain')

@app.route('/test')
def test():
    """Renders the about page."""
    return render_template('test.html',
        title='Test',
        year=datetime.now().year,
        jsonrpc_request = '{"jsonrpc": "2.0","method": "register", "params": [],"id": "2"}',
        message = 'Your application description page',
        api_host = config.get('API_HOST') or request.host_url
        )

#class Note(ndb.Model):
#    """NDB model class for a user's note.

#    Key is user id from decrypted token.
#    """
#    friendly_id = ndb.StringProperty()
#    message = ndb.TextProperty()
#    created = ndb.DateTimeProperty(auto_now_add=True)


# [START gae_python_query_database]
#def query_database(user_id):
#    """Fetches all notes associated with user_id.

#    Notes are ordered them by date created, with most recent note added
#    first.
#    """
#    ancestor_key = ndb.Key(Note, user_id)
#    query = Note.query(ancestor=ancestor_key).order(-Note.created)
#    notes = query.fetch()

#    note_messages = []

#    for note in notes:
#        note_messages.append({
#            'friendly_id': note.friendly_id,
#            'message': note.message,
#            'created': note.created
#        })

#    return note_messages
# [END gae_python_query_database]


@app.route('/notes', methods=['GET'])
def list_notes():
    """Returns a list of notes added by the current Firebase user."""

    # Verify Firebase auth.
    # [START gae_python_verify_token]
    id_token = request.headers['Authorization'].split(' ').pop()
    claims = google.oauth2.id_token.verify_firebase_token(
        id_token, HTTP_REQUEST, audience=oas_config.get('GOOGLE_CLOUD_PROJECT'))
    if not claims:
        return 'Unauthorized', 401
    # [END gae_python_verify_token]

    #notes = query_database(claims['sub'])

    return jsonify(claims)


@app.route('/notes', methods=['POST', 'PUT'])
def add_note():
    """
    Adds a note to the user's notebook. The request should be in this format:

        {
            "message": "note message."
        }
    """

    # Verify Firebase auth.
    id_token = request.headers['Authorization'].split(' ').pop()
    claims = google.oauth2.id_token.verify_firebase_token(
        id_token, HTTP_REQUEST, audience=oas_config.get('GOOGLE_CLOUD_PROJECT'))
    if not claims:
        return 'Unauthorized', 401

    # [START gae_python_create_entity]
    data = request.get_json()

    # Populates note properties according to the model,
    # with the user ID as the key name.
    note = Note(
        parent=ndb.Key(Note, claims['sub']),
        message=data['message'])

    # Some providers do not provide one of these so either can be used.
    note.friendly_id = claims.get('name', claims.get('email', 'Unknown'))
    # [END gae_python_create_entity]

    # Stores note in database.
    note.put()

    return 'OK', 200

@app.route('/form_post',methods=['GET','POST'])
def form_post():
    if request.method == 'POST':
        tempdir = None
        filenames = []
        content_json = request.form.get('params')
        content = json.loads(content_json) if content_json else {}
        try:
            # check if the post request has the file part
            #if not request.files:
            #    return Response("{}", status=200, mimetype='application/json')
            authorization = request.headers.get('Authorization')
            claims = get_firebase_claim()
            for name,files in request.files.items():
                for file in request.files.getlist(name):
                    filename = file.filename
                    # if user does not select file, browser also
                    # submit an empty part without filename
                    if file.filename == '':
                        return Response("{}", status=200, mimetype='application/json')

                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        filenames.append(filename)
                        mimetype = file.mimetype
                        try:
                            if not tempdir:
                                tempdir = tempfile.mkdtemp()
                            save_to = os.path.join(tempdir, filename)
                            file.save(save_to)
                        except:
                            pass
        finally:
            if tempdir: 
                dirname = os.path.split(tempdir)[-1]
                try:
                    ipfs_client = ipfshttpclient.connect(config.get('IPFS_API_URL','/dns/db/tcp/5001/http'))
                    result = ipfs_client.add(tempdir, pattern="**",wrap_with_directory=False)
                    folder = result[-1]
                    hash = folder["Hash"]
                except Exception as err:
                    error = str(err)
                    result = None
                    pass
                finally:
                    shutil.rmtree(tempdir, ignore_errors=True)
                    if result:
                        return Response(json.dumps({
                            "ipfs": [dict(Name=re.sub('^' + dirname + '/?','', x["Name"]), Hash=x["Hash"], Size=x["Size"]) for x in result]
                            }
                            ), status=200, mimetype='application/json')
                    else:
                        return Response("{{{error}}}".format(error=error), status=200, mimetype='application/json')
            else: 
                return Response(json.dumps({
                    "ifps":[]
                    }
                    ), status=200, mimetype='application/json')
                        
        return Response("{{{to}}}".format(to=save_to or tempdir), status=200, mimetype='application/json')
    return Response("what")
