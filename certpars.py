import os
from cryptography import x509

def parser():
    path = "basic_certs"
    for filename in os.listdir("basic_certs"):
        with open(path + "\\" + filename, 'rb') as f:
            m = f.read()
            cer = x509.load_pem_x509_certificate(m)
            print("certificate validity from " + str(cer.not_valid_before) + " to " + str(cer.not_valid_after)+ "\ncertificate id : " + str(cer.signature_algorithm_oid))