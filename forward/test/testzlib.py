#! python

import zlib
import sys

def CmprOut(data):
	sys.stdout.write(data)

def DeCmprOut(data):
	#sys.stdout.write(data)
	pass

def Compress():
	count = 0
	rcount = 0
	cmprobj=zlib.compressobj(zlib.Z_BEST_COMPRESSION)
	for data in sys.stdin:
		cmprdata = cmprobj.compress(data)
		#sys.stderr.write("Read "+data)
		rcount += len(data)
		if cmprdata :
			count += len(cmprdata)
			CmprOut(cmprdata)
	cmprdata = cmprobj.flush()
	CmprOut(cmprdata)
	count += len(cmprdata)
	sys.stderr.write("Compress %d read %d\n"%(count,rcount))
    

def DeCompress():
    todata = ''
    count = 0
    dcount = 0
    decmprobj = zlib.decompressobj()
    while True:
		data = sys.stdin.read(1024)
		count += len(data)
		if len(data) ==0:
			break
		dedata = decmprobj.decompress(data)
		if dedata:
			dcount += len(dedata)
			DeCmprOut(dedata)
    dedata = decmprobj.flush()
    dcount += len(dedata)
    DeCmprOut(dedata)
    sys.stderr.write("De Read %d out %d\n"%(count ,dcount))
    

if __name__ == '__main__':
	if len(sys.argv) == 1:
		DeCompress()
	else:
		Compress()
