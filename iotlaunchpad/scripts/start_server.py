import json
import logging
import datetime
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from pymongo import MongoClient

logger = logging.getLogger(__name__)

class Echo(DatagramProtocol):

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
        
        # self.transport.write(data, (host, port))

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    reactor.listenUDP(9999, Echo())
    reactor.run()
