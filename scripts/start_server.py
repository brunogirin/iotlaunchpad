import os
import argparse
import json
import logging
import datetime
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from pymongo import MongoClient

logger = logging.getLogger(__name__)

class Echo(DatagramProtocol):

    def __init__(self, log_file=None, *args, **kwargs):
        self.log_file = log_file
        print self.log_file
        # DatagramProtocol.__init__(self, *args, **kwargs)
        # super(Echo, self).__init__(*args, **kwargs)

    def datagramReceived(self, data, (host, port)):
        try:
            json_ = json.loads(data)
            client = MongoClient()
            logging.info('MongoDB client: {}'.format(client))
            logging.info('Creating/getting collection: tfl_data')
            db = client.tfl_data
            logging.info('db: {}'.format(db))
            logging.info('Creating/getting my_collection')
            collection = db.my_collection
            logging.info('my_collection: {}'.format(collection))
            logging.info('inserting entry into collection:')
            json_['datetime'] = datetime.datetime.now()
            result = collection.insert_one(json_)
            logging.info('returned output: {}'.format(result))
            logging.info('collection contents:')
            cursor = collection.find()
            for document in cursor:
                logging.info(document)
            
        except ValueError as e:
            print "received %r from %s:%d" % (data, host, port)

        if self.log_file:
            self.log_file.write('{datetime}: {data}\n'.format(datetime=datetime.datetime.now(), data=data))
        
        # self.transport.write(data, (host, port))

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description="Starts a basic UDP server.")
    parser.add_argument('--port', type=int, default=9999)
    parser.add_argument('--log-file', default='log.log')
    args = parser.parse_args()

    print args

    with open(args.log_file, 'wb', 0) as f:

        reactor.listenUDP(9999, Echo(f))
        reactor.run()
