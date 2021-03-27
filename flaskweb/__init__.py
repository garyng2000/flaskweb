"""
The flask application package.
"""
import os
import sys
import uuid
import redis
from flask import Flask, _app_ctx_stack, session
from flask_jsonrpc import JSONRPC, JSONRPCView  # noqa: E402   pylint: disable=C0413
from sqlalchemy.orm import scoped_session
from .model.database import SessionLocal
from .api import AuthorizationView, modules
from .api.auth import auth
import flaskweb.config as config

app = Flask(__name__)
app.secret_key = config.get('FLASK_SECRET_KEY')
app.redis = config.get('REDIS_URL')
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = app.redis
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_FOLDER'] = 'uploads'

app.db_session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)

jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True, jsonrpc_site_api=AuthorizationView)
jsonrpc.register_blueprint(app, modules, url_prefix='/index', enable_web_browsable_api=True)
jsonrpc.register_blueprint(app, auth, url_prefix='/auth', enable_web_browsable_api=True)

@app.before_request
def before_request():
    if 'identifier' not in session:
        session['identifier'] = str(uuid.uuid4())

@app.teardown_appcontext
def remove_session(*args, **kwargs):
    app.db_session.remove()

import flaskweb.views