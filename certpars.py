import os
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from cryptography.hazmat.primitives.asymmetric.ec import ECDSA

def parser():
    a = open("author_cert.pem", "rb")
    r = a.read()
    cert = x509.load_pem_x509_certificate(r)
    publick = cert.public_key()
    path = "basic_certs"
    for filename in os.listdir("basic_certs"):
        with open(path + "\\" + filename, 'rb') as f:
            m = f.read()
            cer = x509.load_pem_x509_certificate(m)
            print("certificate validity from " + str(cer.not_valid_before) + " to " + str(cer.not_valid_after)+ "\nbeginning verification:")  
            #we check for the validity of the cerificate key
            try:
                publick.verify(
                    cer.signature,
                    cer.tbs_certificate_bytes,
                    padding.PKCS1v15(),
                    cer.signature_hash_algorithm
                )
                print("cryptographic validity successfully proven")
            except:   
                print("couldn't verify cerificate") 
        