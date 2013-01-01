#! python

from ConfigParser import ConfigParser
import sys

def CallOption(file):
	try:
		bc = ConfigParser()
		bc.read(file)
		secs = bc.sections()
		for s in secs:
			opts = bc.options(s)
			print("[%s]"%(s))
			for o in opts:
				v = bc.get(s,o)
				print("\t%s = %s"%(o,v))			
	except IOError as e:
		sys.stderr.write(str(e))

def main():
	for a in sys.argv[1:]:
		CallOption(a)

if __name__ == '__main__':
	main()
