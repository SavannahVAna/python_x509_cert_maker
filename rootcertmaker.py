import datetime

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

def makeroo():
    root_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Val-de-Marne"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"Ivry-sur-Seine"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"ESIEA"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"root_CA"),
    ])
    root_cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        root_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=3650)
    ).sign(root_key, hashes.SHA256(), default_backend())

    # Now we want to generate a cert from that root
    cert_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    new_subject = x509.Name([
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Val-de-Marne"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"Ivry-sur-Seine"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"crypto_registration_auth"),
    ])
    registration_cert = x509.CertificateBuilder().subject_name(
        new_subject
    ).issuer_name(
        root_cert.issuer
    ).public_key(
        cert_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
    datetime.datetime.utcnow() + datetime.timedelta(days=30)
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName(u"esiea.fr")]),
        critical=False,
    ).sign(root_key, hashes.SHA256(), default_backend())
    #next we save the certificates as .pem files
    with open("root_cert.pem", 'wb') as f:
        f.write(root_cert.public_bytes(serialization.Encoding.PEM))
    with open("author_cert.pem", 'wb') as d:
        d.write(registration_cert.public_bytes(serialization.Encoding.PEM))


