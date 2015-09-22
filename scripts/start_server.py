import os
import argparse
import json
import logging
import datetime
import pymongo
import logging.handlers
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from pymongo import MongoClient

logger = logging.getLogger(__name__)

class Echo(DatagramProtocol):

    def __init__(self, *args, **kwargs):
        self.client = MongoClient()
        self.db = self.client.database
        try:
            self.collection = self.db.create_collection('collection', capped=True, size=100)
            print 'creating new collection'
        except pymongo.errors.CollectionInvalid:
            self.collection = self.db.collection

    def datagramReceived(self, data, (host, port)):
        document = {}
        document['datetime'] = datetime.datetime.now()
        document['msg'] = data
        result = self.collection.insert_one(document)
        logger.info(data)
        
        # self.transport.write(data, (host, port))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Starts a basic UDP server.")
    parser.add_argument('--port', type=int, default=9999)
    parser.add_argument('--log-file', default='log.log')
    args = parser.parse_args()

    print 'args:', args

    handler = logging.handlers.RotatingFileHandler(args.log_file, maxBytes=1e6, backupCount=3)
    formatter = logging.Formatter("%(asctime)s: %(message)s", '%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    reactor.listenUDP(9999, Echo())
    reactor.run()
