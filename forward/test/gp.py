#! python

import getpass
fp = getpass.win_getpass("Password:")
fpa = getpass.win_getpass("Confirm Password:")

if fp != fpa:
    print ("%s != %s"%(fp,fpa))
else:
    print ("your password %s"%(fp))
