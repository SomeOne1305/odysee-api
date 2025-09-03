import app
def application(environ, start_response):
    """WSGI wrapper to prevent PythonAnywhere timeouts"""
    environ['wsgi.url_scheme'] = 'https'
    return app(environ, start_response)