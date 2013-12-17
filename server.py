import tornado.ioloop
import tornado.web
from tornado.web import HTTPError
import sys
import signal
import logging
import logging.config 
from configobj import ConfigObj
import pymongo
from pymongo import MongoClient
from bson import json_util
from bson.objectid import ObjectId

#Set up logging
logging.config.fileConfig('logging.conf')
LOGGER = logging.getLogger(__name__)

class Empty(object):
    pass

class PingHandler(tornado.web.RequestHandler):
    def get(self):
        LOGGER.info('Got ping, replying pong')
        self.write('pong')

class StaticHandler(tornado.web.RequestHandler):
    def get(self, resource):
        if resource is None or resource == '':
            resource = 'index.html'
        LOGGER.info('Got request for page: ' + resource)
        
        try: 
            with open('static/' + resource, mode='r') as file:
                if '.css' in resource:
                    self.set_header('Content-Type', 'text/css')
                if '.js' in resource:
                    self.set_header('Content-Type', 'text/javascript')
                self.write(file.read())
        except:
            e = sys.exc_info()
            LOGGER.error('StaticHandler: Exception %s %s' % (e[0],e[1]))
            self.write('404: File not found: ' + resource)
            raise HTTPError(404)
                
backend = tornado.web.Application([
    (r"/ping", PingHandler),
    (r"/(.*)", StaticHandler),
])

class Manager(object):
    def __init__(self, ioloop):
        self.ioloop = ioloop
        
    def gracefulExit(self, signal, frame): 
        ioloop.stop()

if __name__ == "__main__":
    LOGGER.info('Starting interplan server')
    
    config = ConfigObj('server.conf')
    backend.conf = Empty()
    backend.conf.externalPort = int(config['server']['port'])
    backend.conf.externalSecurePort = int(config['server']['sslPort'])
    
    ioloop = tornado.ioloop.IOLoop.instance()
    
    backend.manager = Manager(ioloop)
    
    backend.listen(backend.conf.externalPort)
    #backendSSL.listen(backend.conf.externalSecurePort, ssl_options={
    #     'certfile': config['server']['crt'],
    #     'keyfile': config['server']['key'],
    #})
    
    signal.signal(signal.SIGINT, backend.manager.gracefulExit)
    signal.signal(signal.SIGQUIT, backend.manager.gracefulExit)
    signal.signal(signal.SIGTERM, backend.manager.gracefulExit)
    
    ioloop.start()
    
    