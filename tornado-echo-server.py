#!/usr/bin/env python

import logging
from tornado.ioloop import IOLoop
from tornado import gen
from tornado.iostream import StreamClosedError
from tornado.tcpserver import TCPServer
from tornado.options import options, define

define("port", default=1234, help="TCP port to listen on")
logger = logging.getLogger(__name__)


class EchoServer(TCPServer):
    @gen.coroutine
    def handle_stream(self, stream, address):
            try:
                while True:
                    data = yield stream.read_bytes(8192, partial=True)
                    yield stream.write(data)
            except StreamClosedError:
                logger.warning("Lost client at host %s", address[0])
            except Exception as e:
                print(e)

if __name__ == "__main__":
    options.parse_command_line()
    server = EchoServer()
    server.listen(options.port)
    logger.info("Listening on TCP port %d", options.port)
    IOLoop.current().start()