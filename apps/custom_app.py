def custom_app(environ, start_response):
    path = environ['PATH_INFO']
    response = f'Hello from {path}'.encode()
    status = '200 OK'
    headers = [('Content-Length', len(response))]
    start_response(status, headers)
    return [response]
