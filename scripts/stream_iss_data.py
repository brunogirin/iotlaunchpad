#!/usr/bin/python
import socket
import logging
import json
import requests
import time
import datetime

logger = logging.getLogger(__name__)

class Socket(socket.socket):

    def __init__(self, x=socket.AF_INET, y=socket.SOCK_DGRAM, *args, **kwargs):
        super(Socket, self).__init__(x, y, *args, **kwargs)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    sock = Socket() #socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        response = requests.get('http://api.open-notify.org/iss-now.json')
        print response.content
        sock.sendto(response.content, ('127.0.0.1', 9999))
        time.sleep(5)
