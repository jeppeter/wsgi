#! python

import ConfigParser
import sys
class BaseConfig(ConfigParser.ConfigParser):
	def __init__(self,file):
		try:
			super.__init__(self)
			sys.stderr.write("File "+file)
			super.read(file)
		except:
			raise IOError("can not parse %s"%(file))

def CallOption(file):
	try:
		bc = BaseConfig(file)
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
