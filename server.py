from io import StringIO
from socket import socket, SHUT_RDWR, SO_REUSEADDR, SOL_SOCKET

from functools import partial
from typing import Any, Tuple, Union


REQUEST_PARTS = Tuple[str, str, str, dict, str]


class WSGIServer:
    socket: 'socket'
    address: Tuple[str, int]

    def __init__(self, host: str, port: int):
        self.address = host, port

        self.socket = socket()
        self.socket.bind(self.address)
        self.socket.listen(1)

    @staticmethod
    def parse_request(data: str) -> REQUEST_PARTS:
        request, *headers, _, body = data.split('\r\n')
        method, path, protocol = request.split(' ')
        processed_headers = dict(
            item.split(': ')
            for item in headers
        )
        return method, path, protocol, processed_headers, body

    def _to_environ(self, request_data: str) -> dict:
        (
            method, path, protocol,
            processed_headers, body
        ) = self.parse_request(request_data)

        host, port = self.address
        return {
            'wsgi.version': (1, 0),
            'REQUEST_METHOD': method,
            'PATH_INFO': path,
            'SERVER_NAME': host,
            'SERVER_PORT': str(port),
            'SERVER_PROTOCOL': protocol,
            'wsgi.url_scheme': 'http',
            'wsgi.input': StringIO(body)
        }

    @staticmethod
    def _start_response(conn: 'socket', status: int, headers: Union[list, tuple]) -> None:
        status_line = f'HTTP/1.1 {status}\r\n'.encode()
        conn.sendall(status_line)

        for header, value in headers:
            data = f'{header}: {value}\r\n'.encode()
            conn.sendall(data)

        final_message = '\r\n'.encode()
        conn.sendall(final_message)

    def run(self, app: Any) -> None:
        while True:
            conn, client_address = self.socket.accept()
            request = conn.recv(1024).decode('utf-8')
            environ = self._to_environ(request)
            start_response = partial(self._start_response, conn)
            response = app(environ, start_response)
            for data in response:
                conn.sendall(data)

    def stop(self):
        self.socket.shutdown(SHUT_RDWR)
        self.socket.close()

