from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.backends import default_backend

def them(number):
    number+=1
    with open('private_key.pem', 'rb') as pem_in: #loads the registration authority's private key in  order to sign certificates
        pemlines = pem_in.read()
    private_key = load_pem_private_key(pemlines, None, default_backend())
    a = open("author_cert.pem", "rb") #loads the registration authority that will issue the certificate
    r = a.read()
    cert = x509.load_pem_x509_certificate(r)
    
    v = True
    while v :
        algo = input("please enter the signing algorithm you wish to use (SHA1, SHA256, SHA512)\n")
        if algo.casefold() == "SHA256".casefold():
            algr = hashes.SHA256()
            v = False
        elif algo.casefold() == "SHA1".casefold():
            algr = hashes.SHA1()
            v = False
        #elif algo.casefold() == "MD5".casefold():
            #algr = hashes.MD5()
            #v = False
        elif algo.casefold() == "SHA512".casefold():
            algr = hashes.SHA512()
            v = False
        else : 
            print("sorry, couldn't proceed")

    c = True
    while c :
        cipher = input("enter the cipher you wish to use (rsa, EC)\n")
        if(cipher.casefold() == "rsa".casefold()):
            priv_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
            )
            c = False
        #elif(cipher.casefold() == "dh".casefold()):
            #parameters = dh.generate_parameters(generator=2, key_size=2048)
            #priv_key = parameters.generate_private_key()
            #c = False
        elif(cipher.casefold() == "EC".casefold()):
            priv_key = ec.generate_private_key(ec.SECP384R1())
            c = False
        else:
            print("sorry couldn't proceed")



    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Val-de-Marne"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"Ivry-sur-Seine"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"ESIEA"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"firts_CA" + str(number)),
    ])
    certif = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        cert.issuer
    ).public_key(
        priv_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=3650)
    ).sign(private_key, algr, default_backend())

    with open("basic_certs/cert.pem" +str(number), "wb") as d :
        d.write(certif.public_bytes(serialization.Encoding.PEM))
    return number
