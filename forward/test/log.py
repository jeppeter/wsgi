#! python

import logging
import sys
from optparse import OptionParser

def SetLevel(option,opt,value,parser):
    if str(value).lower() == "debug".lower():
    	setattr(parser.values,option.dest,logging.DEBUG)
    elif str(value).lower() == "warning".lower() or str(value).lower() == "warn".lower():
    	setattr(parser.values,option.dest,logging.WARNING)
    elif str(value).lower() == "critical".lower():
    	setattr(parser.values,option.dest,logging.CRITICAL)
    elif str(value).lower() == "info".lower():
    	setattr(parser.values,option.dest,logging.INFO)
    elif str(value).lower() == "error".lower():
    	setattr(parser.values,option.dest,logging.ERROR)
    else:
    	sys.stderr.write("level not valid (%s) option(%s) opt(%s)\n"%(str(value),str(option),str(opt)))
    	sys.exit(3)

opta = OptionParser()
opta.add_option("--level","-l",dest="level",default=logging.ERROR,action="callback",type="string",callback=SetLevel,help="specify the debug level")
opta.add_option("--format","-f",dest="format",type="string",default='%(levelname)-8s %(asctime)-12s [%(filename)-10s:%(funcName)-20s:%(lineno)-5s] %(message)s',help="specify the format")
opta.add_option("--datefmt","-d",dest="datefmt",type="string",default="%b %d %H:%M:%S",help="specify the date format")
opt,args = opta.parse_args()

print "opt %s"%(type(opt))
print opt
print args

logging.basicConfig(level=opt.level,format=opt.format)

for s in args:
	logging.debug(s)
	logging.warning(s)
	logging.info(s)
	logging.critical(s)
	#logging.exception(s)

