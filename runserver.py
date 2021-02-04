"""
This script runs the flaskweb application using a development server.
"""

from os import environ
from flaskweb import app

def handle_exceptions(err):
    # Log exception in your logs
    # get traceback and sys exception info and log as required   
    # app.logger.error(getattr(e, 'description', str(e)))

    # Print traceback

    # return your response using getattr(e, 'code', 500) etc. 
    return f"{err.__class__.__name__}: {err}"
    # Exception is used to catch all exceptions
app.register_error_handler(Exception, handle_exceptions)

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
