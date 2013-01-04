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
		sys.stderr.write("try to connect %s\n"%(repr(paddr)))
		rsock = socket.create_connection(paddr)
		sys.stderr.write("try connect %s succ\n"%(repr(paddr)))
		rsslsock = ssl.SSLSocket(rsock)
	except:
		sys.stderr.write("except %s\n"%(sys.exc_info()))
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
	gsock.shutdown()
	rsslsock.shutdown()
	return 0

def parse_ipport(str):
	host,port = str.split(":")
	if not host or \
		not port or \
		len(host) == 0 or \
		len(port) == 0 :
		sys.stderr.write("%s not valid for host:port\n"%(str))
		sys.exit(3)
	return host,int(port)

if __name__ == '__main__':
	if len(sys.argv) < 3:
		sys.stderr.write("%s local:port remote:port"%(__file__))
		sys.exit(3)
	source=parse_ipport(sys.argv[1])
	dest = parse_ipport(sys.argv[2])
	sys.stdout.write("source %s dest %s\n"%(repr(source),repr(dest)))
	try:
		ssock = socket.tcp_listener(source)
		sys.stderr.write("Listen on %s\n"%(repr(source)))
	except:
		sys.stderr.write("listen %s error %s\n"%(repr(source),sys.exc_info()))
		sys.exit(3)
	while True:
		try:
			csock,paddr = ssock.accept()
			gevent.spawn(CliSSL,csock,dest)
		except KeyboardInterrupt as e:
			sys.stderr.write("User Interrupt\n")
			break
		except :
			csock.shutdown()
			sys.stderr.write("accept error %s %s\n"%(sys.exc_info(),repr(e)))
			pass
	ssock.close()
	sys.stderr.write("Exit\n")