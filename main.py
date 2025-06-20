# Sebby Web Server
# Code by Sebminecrafter
# Warning: Not fully tested for security
# Not for production use (yet)
from http.server import *
import os, ssl, mimetypes
ver = 1.0
strver = str(ver)
codePaths = []
codePathFuncs = []
mimetypes.init()

def evalRequest(path):
    output = None
    if path in codePaths:
        output = eval(f"{codePathFuncs[codePaths.index(path)]}()")
        status = 200
    else:
        path2 = f"{os.getcwd()}{path}"
        if os.path.isfile(path2):
            status = 200
            if str(mimetypes.guess_file_type(path2)[0]) == 'text/html':
                with open(path2, 'r') as f:
                    output = f"{output}{append}".encode('UTF-8')
                type = 'text/html'
            else:
                with open(path2, 'rb') as f:
                    output = f.read()
                type = str(mimetypes.guess_file_type(path2)[0])
        elif os.path.isfile(f"{path2}index.html"):
            with open(f"{path2}index.html") as f:
                output = f.read()
                status = 200
                output = f"{output}{append}".encode('UTF-8')
                type = 'text/html'
        elif os.path.isfile(f"{path2}/index.html"):
            with open(f"{path2}/index.html") as f:
                output = f.read()
                status = 200
                output = f"{output}{append}".encode('UTF-8')
                type = 'text/html'
        else:
            output = notfoundpage.encode('UTF-8')
            status = 404
            type = 'text/html'
    return output,status,type

class SebbyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        response = evalRequest(self.path)
        self.send_response(response[1])
        self.send_header("Content-type", response[2]); self.end_headers()
        self.wfile.write(response[0])

#    :)                             --------Config-----------------------------------------------------
port = 443                          #Which port to serve on (default for http: 80, https: 443)
host = ''                           #Hostname/ip change if you aren't just devtesting
keyfilelocation = 'cert/private.key'#Only required for ssl, location of your key file (private.key)
certfilelocation = 'cert/cert.pem'  #Only required for ssl, location of your certificate (cert.pem)
sebby_using_ssl = True              #Whether you ar using SSL (HTTPS) or not (HTTP)
handler_class=SebbyServer           #Only change if you know are testing/editing/etc. ()
append = f"\n<br><center><p>Running SebbyWebServer Version {strver}</p></center>" #Appended at end of page
notfoundpage = f"<h1>404 File/Function not found: {path}</h1>"   #File not found (404) page

if __name__ == '__main__':
    server_address = (host, port)
    httpd = ThreadingHTTPServer(server_address, handler_class)
    if seeby_using_ssl:
        sslctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        sslctx.check_hostname = False
        sslctx.load_cert_chain(certfile=certfilelocation, keyfile=keyfilelocation)
        httpd.socket = sslctx.wrap_socket(httpd.socket, server_side=True)
        print("HTTPS is enabled! :)")
    else:
        print("Running in HTTP mode. :/")
    if server_address[0] == '': printserver = '127.0.0.1 or localhost'
    else: printserver = server_address[0]
    print(f"SebbyWebServer\nServing on {printserver}:{server_address[1]}\nPress Ctrl+C to stop")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    print("Stopping server...")
    httpd.server_close()
    print("Stopped.")