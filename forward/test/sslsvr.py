#! python


import gevent
from gevent import monkey
# patches stdlib (including socket and ssl modules) to cooperate with other greenlets
monkey.patch_all()
from gevent import socket,ssl
import sys

def EchoServer(gsock,paddr):
	rsslsock = ssl.wrap_socket(gsock,server_side=True,certfile="cert",keyfile="key",ssl_version=ssl.PROTOCOL_SSLv23)
	count = 0
	while True:
		try:
			data = rsslsock.recv(1024)
			if not data or len(data)==0:
				break
			rsslsock.send(data)
			count += len(data)
		except:
			sys.stderr.write("in sock %s error %s"%(repr(gsock),sys.exc_info()))
			break
	gsock.close()
	sys.stderr.write("client %s closed send (%d)bytes\n"%(repr(paddr),count))
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
	if len(sys.argv) < 2:
		sys.stderr.write("%s addr:port\n"%(__file__))
		sys.exit(3)
	source = parse_ipport(sys.argv[1])
	try:
		ssock = socket.tcp_listener(source)
		sys.stderr.write("Listen on %s\n"%(repr(source)))
	except:
		sys.stderr.write("listen %s error %s\n"%(repr(source),sys.exc_info()))
		sys.exit(3)
	while True:
		try:
			csock,paddr = ssock.accept()
			gevent.spawn(EchoServer,csock,paddr)
		except KeyboardInterrupt as e:
			sys.stderr.write("User Interrupt\n")
			break
		except :
			csock.shutdown()
			sys.stderr.write("accept error %s %s\n"%(sys.exc_info(),repr(e)))
			pass
	ssock.close()
	sys.stderr.write("Exit\n")	
