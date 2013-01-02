#! python

import sys
import signal
import gevent
from gevent.server import StreamServer
from gevent.socket import create_connection, gethostbyname

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
def Proxy(env,start_response):
	

class ForwardServer(StreamServer):
