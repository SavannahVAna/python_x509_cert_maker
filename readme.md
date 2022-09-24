## Project description
This python project is made to create X509 certificates and parse them to assert their cryptographic validity


## Project composition
This project is composed of 4 scripts :
-base.py controls the 3 other scripts
-mainf.py creates the root certificate authority and registration authority
-deuetap.py lets you create certificates with chosen cipher and signature algorithms
-certpars.py parses the generated certificates

## Usage
Provided that you have installed the cryptography library, you can just launch base.py for the project to work.
It will automatically create a root certificate and registration authority.
Then you will be asked if you want to create certificates and you will be asked which signing and cipher algorithm to use, and put the created cerificates in basic_certs folder.
Finally it will parse the certificates in the basic_certs folder and display their ID and validity period. 