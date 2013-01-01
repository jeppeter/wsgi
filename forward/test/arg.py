#! python

from optparse import OptionParser
import sys

def Usage(excode=0):
    if excode == 0:
        sys.stdout.write("%s [OPTIONS]"%(__file__))
    else:
        sys.stdout.write("%s [OPTIONS]"%(__file__))
    sys.exit(excode)
def CallBackOpt(option,opt,value,parser):
    setattr(parser.values,option.dest,value)
    sys.stderr.write("option (%s) opt (%s) value (%s)\n"%(str(option),str(opt),str(value)))
    return

par = OptionParser()
par.add_option("-f","--file",dest="filename",help="specify the filename")
par.add_option("-p","--port",dest="PORT",help="specify the local address")
par.add_option("-c","--call",type="string",action="callback",callback=CallBackOpt,help="call back test")

(options,args)=par.parse_args()

print "Options"
print options
print "args"
print args
