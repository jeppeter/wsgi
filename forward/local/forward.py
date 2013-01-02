#! python

import sys
import gevent
from gevent.pywsgi import WSGIServer
import logging

def DebugEnv(env):
	res = ''
	for k,v in env.items():
		curres = "evn[%s] = %s"%(k,v)
		logging.info(curres)
		curres += "\n"
		res += curres
	return res

"""
	@brief Proxy to handle the proxy 
	      in the form like this
	      Enc-Method:
	      Enc-Url:
	  	  ....

	 @param env environment dict
	 @param start_response callback function to send response

	 @return value content of the response
"""
def proxy_application(env,start_response):
	resbody = DebugEnv(env)
	status = '200 OK'
	response_headers = [('Content-Type', 'text/plain'),
                  ('Content-Length', str(len(resbody)))]
	start_response(status, response_headers)
	return [resbody]



if __name__ == '__main__':
	if len(sys.argv) < 2:
		sys.stderr.write("%s hostip:port\n"%(__file__))
		sys.exit(3)
	logging.basicConfig(level=logging.INFO,format="%(levelname)-8s %(asctime)-12s [%(filename)-10s:%(funcName)-20s:%(lineno)-5s] %(message)s")
	arg = sys.argv[1]
	listenip,listenport=arg.split(":")
	listenport = int(listenport)
	logging.info("listen on %s:%d"%(listenip,listenport))
	WSGIServer((listenip,listenport), proxy_application).serve_forever()
