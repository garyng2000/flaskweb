import os
import uuid
import hashlib
from flask import current_app as app, request, g
from flask_jsonrpc import JSONRPCBlueprint
from flask_jsonrpc.exceptions import JSONRPCError
from typing import Any, Dict, List, Union, NoReturn, Optional
from numbers import Real
from flaskweb.api import AuthorizationView
from flaskweb.model.database import SessionLocal
from datetime import datetime
from flaskweb.helper import get_firebase_claim
from typing import Any, Dict, List, Union, NoReturn, Optional

from flaskweb.model.database import SessionLocal
from flaskweb.service.hdwallet import new_wallet

auth = JSONRPCBlueprint('auth', __name__)

@auth.method('register')
def register(first_name: Optional[str]=None, last_name: Optional[str]=None, id_token: Optional[str] = None, commit: Optional[bool] = True) -> Any:
    claims = None
    try:
        claims, id_token = get_firebase_claim(id_token)
    except:
        raise 

    if not claims: raise JSONRPCError(message='unknown identity', code=-30000)
    user_id = claims['user_id']
    if not claims: raise JSONRPCError(message='unknown identity', code=-30000)
    session = app.db_session
    user_id_hash = hashlib.sha256(user_id.encode('utf-8')).hexdigest()
    wallet = new_wallet()
    return { "person_id" : user_id_hash, "id_token":id_token, "claims": claims, "wallet" : wallet}