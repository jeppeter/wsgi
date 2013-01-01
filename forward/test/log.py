#! python

import logging
import sys
from optparse import OptionParser

def SetLevel(option,opt,value,parser):
    if value == "debug":
    	setattr(parser.values,option.dest,loggin.DEBUG)
    elif value == "warning" || value == "warn":
    	setattr(parser.values,option.dest,loggin.WARNING)
    elif value == "critical":
    	setattr(parser.values,option.dest,loggin.CRITICAL)
    elif value == "info":
    	setattr(parser.values,option.dest,loggin.INFO)
    else:
    	sys.stderr.write("level not valid (%s)\n"%(str(value)))
    	sys.exit(3)

optarg = OptionParser()
optarg.add_option("--level","-l",dest="Level",default=loggin.ERROR,action="callback",callback=SetLevel,help="specify the debug level")
optarg.add_option("--format","-f",dest="Format",help="specify the format")

optarg.parse_args()



logging.info()
