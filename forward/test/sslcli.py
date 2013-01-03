#! python

import gevent
from gevent import monkey
from gevent import socket,ssl
import traceback
# patches stdlib (including socket and ssl modules) to cooperate with other greenlets
monkey.patch_all()


def CliSSL(gsock,paddr):
	try:
		rsock = socket.create_connection(paddr)
		rsslsock = ssl.SSLSocket(rsock)
	except:
		gsock.shutdown()
		return -1

	while True:
		
