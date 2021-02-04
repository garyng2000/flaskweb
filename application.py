#this is specifically for AWS elastic beanstalk

import logging.handlers
from os import environ
from flaskweb import app 

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Handler 
LOG_FILE = '/tmp/sample-app.log'
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1048576, backupCount=5)
handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add Formatter to Handler
handler.setFormatter(formatter)

# add Handler to Logger
logger.addHandler(handler)



def handle_exceptions(err):
    # Log exception in your logs
    # get traceback and sys exception info and log as required   
    app.logger.error(getattr(err, 'description', str(err)))

    # Print traceback

    # return your response using getattr(e, 'code', 500) etc. 
    return f"{err.__class__.__name__}: {err}"
    # Exception is used to catch all exceptions
app.register_error_handler(Exception, handle_exceptions)

#what AWS EB looks for 'application'
application = app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5000'))
    except ValueError:
        PORT = 5000
    application.run(HOST, PORT)