#! python

import gevent
from gevent import monkey
from gevent import socket,ssl
from gevent.server import StreamServer
import traceback
import sys
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

def parse_ipport(str):
	host,port = str.split(":")
	if not host or \
		not port or \
		len(host) == 0 or \
		len(port) == 0 :
		sys.stderr.write("%s not valid for host:port\n"%(str))
		sys.exit(3)
	return host,port

if __name__ == '__main__':
	if len(sys.argv) < 3:
		sys.stderr.write("%s local:port remote:port"%(__file__))
		sys.exit(3)
	source=parse_ipport(sys.argv[1])
	dest = parse_ipport(sys.argv[2])
	sys.stdout.write("source %s dest %s\n"%(repr(source),repr(dest)))
	try:
		ssock = socket.tcp_listener(source)
	except:
		sys.stderr.write("listen %s error\n"%(source))
		sys.exit(3)
	while True:
		try:
			csock,paddr = ssock.accept()
			gevent.spawn(CliSSL,(csock,dest))
		except:
			sys.stderr.write("accept error %s\n"%(sys.exp_info()[0]))
			pass
	ssock.close()
	sys.stderr.write("Exit\n")