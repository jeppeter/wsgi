#! python

import gevent
from gevent import monkey
from gevent import socket,ssl
import traceback
# patches stdlib (including socket and ssl modules) to cooperate with other greenlets
monkey.patch_all()

def CliRemoteRead(sslsock,gsock):	
	while True:
		try:
			data = sslsock.recv(1024)
			if not data or len(data)==0 :
				break
			gsock.send(data)
		except:
			break
	return 0

def CliSSL(gsock,paddr):
	try:
		rsock = socket.create_connection(paddr)
		rsslsock = ssl.SSLSocket(rsock)
	except:
		gsock.shutdown()
		return -1
	chld = gevent.spawn(CliRemoteRead,(rsslsock,gsock,))
	while True:
		try:
			data = gsock.recv(1024)
			if not data or len(data) == 0 :
				break
			rsslsock.send(data)
		except:
			break
	gevent.join(chld)
	return 0


