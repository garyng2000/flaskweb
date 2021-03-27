import imghdr
import sys
import os
import tempfile
import shutil
from os import environ
from datetime import datetime
from flask import render_template, Response, current_app, request, jsonify
from werkzeug.utils import secure_filename
from flaskweb import app
import ipfshttpclient
import json

def allowed_file(filename): return True

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')


