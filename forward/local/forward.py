#! python

import sys
import signal
import gevent
from gevent.server import StreamServer
from gevent.socket import create_connection, gethostbyname


class ForwardServer(StreamServer):
