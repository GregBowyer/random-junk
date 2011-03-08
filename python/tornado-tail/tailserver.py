#!/usr/bin/env python

import logging
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.options import define, options
import os
import subprocess
import fcntl

define("port", default=7777, help="Run server on a specific port", type=int)
PROCESS = ['dstat', '--noheaders', '-c']

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info("Info")
        self.write("Running")

def process(Process):
    process = subprocess.Popen(PROCESS, stdout = subprocess.PIPE)
    pipe = process.stdout
    fcntl.fcntl(pipe.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)

    data = ""

    first_run = True

    while process:
        try:
            data += os.read(pipe.fileno(), 1024)
            if data:
                lines = data.split('\n')

                if first_run:
                    lines = lines[2:]
                    first_run = False

                for line in lines[:-1]:
                    yield line
                
                # The last line is leftover data
                data = lines[-1]
            else:
                yield None
        except:
            yield None


class LogStreamer(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        interval_ms = 200
        try:
            self.ioloop = tornado.ioloop.IOLoop.instance()
            self.scheduler = tornado.ioloop.PeriodicCallback(self.async_callback(self.go), interval_ms, io_loop = self.ioloop)
            self.scheduler.start()
            self.process = process(PROCESS)
        except Exception, e:
            logging.error("Exception in LogStreamer: ", exc_info = True)

    def go(self):
        if self.request.connection.stream.closed():
            logging.debug("Client gone....")
            self.scheduler.stop()
            self.scheduler = None
            return
        else: 
            logging.debug("Returning to client")

            for data in self.process:
                if data:
                    self.write(data)
                    self.flush()
                else:
                    break

class WebSocketStreamer(tornado.websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        tornado.websocket.WebSocketHandler.__init__(self, *args, **kwargs)

    def open(self):
        proc = process(PROCESS)

        interval_ms = 100
        try:
            self.ioloop = tornado.ioloop.IOLoop.instance()
            self.scheduler = tornado.ioloop.PeriodicCallback(self.async_callback(self.go), interval_ms, io_loop = self.ioloop)
            self.scheduler.start()
            self.process = process(PROCESS)
        except Exception, e:
            logging.error("Exception in LogStreamer: ", exc_info = True)

    def go(self):
        if self.request.connection.stream.closed():
            logging.debug("Client gone....")
            self.scheduler.stop()
            self.scheduler = None
            return
        else: 
            logging.debug("Returning to client")

            for data in self.process:
                if data:
                    print data
                    self.write_message(data)
                else:
                    break

    def on_message(self, message):
        pass
        # 

    def on_connection_close(self):
        pass

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "xsrf_cookies": True,
}
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/ws", WebSocketStreamer),
    (r"/tail", LogStreamer)
], **settings)

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    tornado.options.parse_command_line()
    http_server.listen(options.port)
    logging.info("TornadoLog started. Point your browser to http://localhost:%d/tail" % options.port)
    tornado.ioloop.IOLoop.instance().start()
