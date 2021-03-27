import os
import sqlalchemy
import pyodbc
from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import flaskweb.config as config
odbc_connection_string = config.get('ODBC_CONNECTION_STRING')
odbc_connection_credential = config.get('ODBC_CONNECTION_CREDENTIAL')
sqlalchemy_engine_url = config.get('SQLALCHEMY_URL')
mariadb_key_location = config.get('MARIADB_KEY_LOCATION')
if mariadb_key_location is None or mariadb_key_location == 'None':
    mysql_connect_args = {}
else:
    mysql_connect_args = { 
        "ssl_ca": os.path.join(mariadb_key_location, "mariadb-ca.pem"), 
        "ssl_cert":os.path.join(mariadb_key_location, "mariadb-cert.pem"), 
        "ssl_key":os.path.join(mariadb_key_location, "mariadb-key.pem"),
    
        #"check_same_thread":False # only for sqlite ! 
        }
engine = create_engine(sqlalchemy_engine_url,connect_args=mysql_connect_args)

SessionLocal = sessionmaker(bind = engine, autocommit=False, autoflush = False)

Base = declarative_base()

def mssql_query(connection):
        cursor = connection.cursor()
        cursor.execute("SELECT UsrId, UsrName FROM dbo.Usr") 
        yield format(cursor.description) + '\n'
        for data in cursor.fetchall():
            yield '{0.UsrId} - {0.UsrName}'.format(data) + '\n'
        params = (1,1,1,1)
        cursor.execute("{CALL dbo.GetUsrPref(?,?,?,?)}",params)
        yield format(cursor.description) + '\n'
        for data in cursor.fetchall():
            yield format(data) + '\n'

def mysql_query(connection):
        cursor = connection.cursor()
        cursor.execute("SELECT first_name, last_name FROM person") 
        yield format(cursor.description) + '\n'
        for data in cursor.fetchall():
            yield '{0.first_name} - {0.last_name}'.format(data) + '\n'

def sql_query():
    try:
        with app.app_context():
            app_root_path = current_app.root_path
            yield app_root_path + '\n'
        connection_string = config.get('ODBC_CONNECTION_STRING')
        connection_credential = config.get('ODBC_CONNECTION_CREDENTIAL')
        #below is for mysql/mariadb, interchangeable, either /etc/odbcinst.ini or use windows ODBC data source admin to find the name of driver
        #connection_string = 'Driver={MySQL};PORT=3306;Server=db;Database=oas;Option=10; sslca=d:\oas\oas-api\mariadb-ca.pem; sslcert=d:\oas\oas-api\mariadb-cert.pem;sslkey=d:\oas\oas-api\mariadb-key.pem;sslverify=0;'
        #connection_string = 'Driver={MARIADB ODBC 3.1 Driver};PORT=3306;Server=db;Database=oas;Option=10; sslca=d:\oas\oas-api\mariadb-ca.pem; sslcert=d:\oas\oas-api\mariadb-cert.pem;sslkey=d:\oas\oas-api\mariadb-key.pem;sslverify=0;'
        #connection_credential = 'UID=root;PWD=password;'
        #below is for freeTDS(only linux) which is needed for ARM64 platform, PORT is a must unlike MS driver
        #connection_string = 'DRIVER={FreeTDS};PORT=1433;SERVER=db;DATABASE=OASDesign;TDS_Version=7.4'
        #connection_credential = 'UID=root;PWD=password;'
        conn = pyodbc.connect(connection_string + connection_credential)
        #yield from mssql_query(conn)
        yield from mysql_query(conn)
        conn.close()
        yield "ODBC_CONNECTION_STRING: {0}".format(connection_string)    
    except Exception as err:
        #return to client - only for debugging
        yield f"{err.__class__.__name__}: {err}"
        #let general exception handling handle it(log etc.)
        raise err
