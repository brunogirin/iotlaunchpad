#!/usr/bin/python
import socket
import logging
import argparse
import json

logger = logging.getLogger(__name__)

class Socket(socket.socket):

    def __init__(self, x=socket.AF_INET, y=socket.SOCK_DGRAM, *args, **kwargs):
        super(Socket, self).__init__(x, y, *args, **kwargs)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Sends a UDP packet to a socket.")
    parser.add_argument('--msg', default='Hello world!')
    parser.add_argument('--ip', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=9999)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    logger.info('args: {}'.format(args))

    sock = Socket() #socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    logger.info('Sending message to {ip}:{port}: msg: "{message}"\n'.format(ip=args.ip, port=args.port, message=args.msg))
    
    response = sock.sendto(args.msg, (args.ip, args.port))
    
    logger.info('Response: {}'.format(response))

    # msg = {
    #     'x': 10,
    #     'y': 11,
    #     'z': 12,
    # }
    # response = sock.sendto(json.dumps(msg), (args.ip, args.port))
