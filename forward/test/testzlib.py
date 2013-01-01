#! python

import zlib
import sys

def Compress():
    todata = ''
    for data in sys.stdin:
		todata += data
		sys.stderr.write("Read "+data)
    data = zlib.compress(todata,zlib.Z_BEST_COMPRESSION)
    sys.stderr.write("Compress %d\n"%(len(data)))
    sys.stdout.write(data)
    

def DeCompress():
    todata = ''
    count = 0
    while True:
		data = sys.stdin.read(1024)
		count += len(data)
		sys.stderr.write("read %d\n"%(count))
		if len(data) ==0:
			break
		todata += data
    sys.stderr.write("De Read %d "%(len(todata)))
    data =zlib.decompress(todata)

if __name__ == '__main__':
	if len(sys.argv) == 1:
		DeCompress()
	else:
		Compress()
