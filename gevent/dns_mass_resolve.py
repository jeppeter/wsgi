#!/usr/bin/python
"""Resolve hostnames concurrently, exit after 2 seconds.

Under the hood, this might use an asynchronous resolver based on
c-ares (the default) or thread-pool-based resolver.

You can choose between resolvers using GEVENT_RESOLVER environment
variable. To enable threading resolver:

    GEVENT_RESOLVER=thread python dns_mass_resolve.py
"""
from __future__ import with_statement
import sys
import gevent
from gevent import socket
from gevent.pool import Pool
import datetime

N = 1000
# limit ourselves to max 10 simultaneous outstanding requests
pool = Pool(100)
finished = 0
success = 0


def job(url):
	global finished
	global success
	try:
		try:
			ip = socket.gethostbyname(url)
			print ('%s = %s' % (url, ip))
			success += 1
		except socket.gaierror:
			ex = sys.exc_info()[1]
			print ('%s failed with %s' % (url, ex))
	finally:
		finished += 1

start_time = datetime.datetime.now()
with gevent.Timeout(100, False):
    for x in xrange(10, 10 + N):
        pool.spawn(job, '%s.com' % x)
    pool.join()

end_time = datetime.datetime.now()
print ('finished within 100 seconds: %s(%s)/%s time %s' % (finished, success,N,str(end_time-start_time)))
