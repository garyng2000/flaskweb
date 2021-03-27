import os
import hashlib
from flask import Flask, current_app as app, request, g
from flask_jsonrpc import JSONRPC, JSONRPCBlueprint, JSONRPCView  # noqa: E402   pylint: disable=C0413
from typing import Any, Dict, List, Union, NoReturn, Optional
from flaskweb.model.database import SessionLocal

class UnauthorizedError(Exception):
    pass

class AuthorizationView(JSONRPCView):
    def check_auth(self) -> bool:
        username = request.headers.get('X-Username')
        password = request.headers.get('X-Password')

        claims = get_firebase_claim()
        #if not claims:
        #    return False
            #return 'Unauthorized', 401
        if claims != None:
            g.oauth_claims = claims
            session = app.db_session
            user_id = claims['user_id']
            user_id_hash = hashlib.sha256(user_id.encode('utf-8')).hexdigest()
            users = session.query(Person).filter(Person.oauth_id == 'firebase:' + user_id_hash)
            g.user = users.first()
            return g.user is not None

        #return username == 'username' and password == 'secret'
        return False

    def dispatch_request(self):
        if not self.check_auth():
            raise UnauthorizedError()
        return super().dispatch_request()

modules = JSONRPCBlueprint('modules', __name__, jsonrpc_site_api=AuthorizationView)

@modules.method("")
def index() -> List[str]:
    return ["artist","person"]

