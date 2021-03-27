import os

def _get(name, ifNone=None):
    val = os.environ.get(name, ifNone)
    if val == 'placeholder': raise Exception("configuration issue {key}".format(key=name))
    return val if val is not None and val != 'None' else ifNone

config = dict(
#for firebase services
GOOGLE_CLOUD_PROJECT = _get('GOOGLE_CLOUD_PROJECT','None'),
#for odbc connection
ODBC_CONNECTION_STRING = _get('ODBC_CONNECTION_STRING','DRIVER={ODBC Driver 17 for SQL Server};SERVER=db;PORT=1433;DATABASE=RODesign;'),
ODBC_CONNECTION_CREDENTIAL = _get('ODBC_CONNECTION_CREDENTIAL','UID=sa;PWD=password;'),
#for sqlalchemy connection
SQLALCHEMY_URL = _get('SQLALCHEMY_URL',"mysql+pymysql://root:password@db/mysql?charset=utf8mb4"),
MARIADB_KEY_LOCATION = _get('MARIADB_KEY_LOCATION'),
#for flask client side cookie encryption
FLASK_SECRET_KEY = _get('FLASK_SECRET_KEY',b'this_is_only_for_test_not_production_use'),
#for redis server
REDIS_URL = _get('REDIS_URL','rediss://db:6379'),
#for api hosting domain
API_HOST = _get('API_HOST','None'),
#for api hosting domain
IPFS_API_URL = _get('IPFS_API_URL','/dns/db/tcp/5001/http'),
#for api hosting domain
FIREBASE_CONFIG_JSON_FILE = _get('FIREBASE_CONFIG_JSON_FILE','d:/firebase_service_account.json')
)

def get(name, ifNone=None): 
    val = config.get(name)
    if val == 'placeholder': raise Exception("configuration issue {key}".format(key=name))

    return val if val is not None and val != 'None' else ifNone
