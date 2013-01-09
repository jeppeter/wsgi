import os
import sys
 
from socket import gethostname
 
from OpenSSL import crypto
 
 
def generate_self_signed_cert(cert_dir,prefix, is_valid=True):
    """Generate a SSL certificate.
 
    If the cert_path and the key_path are present they will be overwritten.
    """
    key_f = prefix + '.key'
    crt_f = prefix + '.crt'
    if not os.path.exists(cert_dir):
        os.makedirs(cert_dir)
    cert_path = os.path.join(cert_dir, crt_f)
    key_path = os.path.join(cert_dir, key_f)
 
    if os.path.exists(cert_path):
        os.unlink(cert_path)
    if os.path.exists(key_path):
        os.unlink(key_path)
 
    # create a key pair
    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 1024)
 
    # create a self-signed cert
    cert = crypto.X509()
    cert.get_subject().C = 'UK'
    cert.get_subject().ST = 'London'
    cert.get_subject().L = 'London'
    cert.get_subject().O = 'Canonical'
    cert.get_subject().OU = 'Ubuntu One'
    cert.get_subject().CN = gethostname() if is_valid else gethostname()[::-1]
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60) 
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(key)
    cert.sign(key, 'sha1')
 
    with open(cert_path, 'wt') as fd: 
        fd.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
 
    with open(key_path, 'wt') as fd: 
        fd.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
 
    return cert_path, key_path

if __name__ == '__main__':
	if (len(sys.argv)<3):
		sys.stderr.write("%s dir prefix to make the x509 cert and key file"%(__file__))
		sys.exit(3)
	generate_self_signed_cert(sys.argv[1],sys.argv[2])