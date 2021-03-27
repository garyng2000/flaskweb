import imghdr
import os
from flask import current_app as app, request, g
from typing import Any, Dict, List, Union, NoReturn, Optional
import google.auth.transport.requests
import google.oauth2.id_token
import flaskweb.config as config

HTTP_REQUEST = google.auth.transport.requests.Request()

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

def get_firebase_claim(oauth_token: Optional[str] = None) -> Any:
    id_token = oauth_token or request.headers['Authorization'].split(' ').pop()
    if (not id_token or id_token == 'Bearer'): return None
    claims = google.oauth2.id_token.verify_firebase_token(id_token, HTTP_REQUEST, audience=config.get('GOOGLE_CLOUD_PROJECT'))
    return claims, id_token