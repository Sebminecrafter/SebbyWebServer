mkdir cert
openssl req -x509 -newkey rsa:2048 -keyout cert/private.key -out cert/cert.pem -days 1461
