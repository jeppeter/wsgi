#!/usr/bin/python
# Copyright (c) 2009 Denis Bilenko. See LICENSE for details.

"""Spawn multiple workers and wait for them to complete"""


import gevent
from gevent import monkey
import sys
import datetime


# patches stdlib (including socket and ssl modules) to cooperate with other greenlets
monkey.patch_all()

import urllib2

def print_head(url):
	print ('Starting %s' % url)
	data = urllib2.urlopen(url).read()
	print ('%s: %s bytes' % (url, len(data)))

def main():	
	start_time = datetime.datetime.now()
	jobs = [gevent.spawn(print_head, url) for url in sys.argv[1:]]
	gevent.joinall(jobs)
	end_time = datetime.datetime.now()
	print("Running time is %s"%(str(end_time - start_time)))

if __name__ == '__main__':
	main()
