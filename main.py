# Sebby Web Server
# Code by Sebminecrafter
# Warning: Not fully tested for security
# Not for production use (yet)
from http.server import *
import os, ssl, mimetypes
ver = 1.1
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

class SebbyServer(BaseHTTPRequestHandler): #just runs another function -_-
    def do_GET(self):
        response = evalRequest(self.path)
        self.send_response(response[1])
        self.send_header("Content-type", response[2]); self.end_headers()
        self.wfile.write(response[0])

#Load config file
try:
    with open('config.txt', 'r') as config:
        configlines = config.readlines()
        for i in configlines:
            eval(i) #its lit just python T-T, be careful bro
        config.close() #close file cuz yes
except Exception:
    print("Failed to load config file, defaulting to default settings (please fix this though)")
    #Apply defaults because bro forgor to set their settings
    port = 80; host = ''; keyfilelocation = ''; certfilelocation = ''; sebby_using_ssl = False; handler_class=SebbyServer; append = f"\n<br><center><p>Running SebbyWebServer Version {strver}</p></center>"; notfoundpage = f"<h1>404 File/Function not found: {path}</h1>"

if __name__ == '__main__':
    server_address = (host, port)
    httpd = ThreadingHTTPServer(server_address, handler_class)
    if seeby_using_ssl:
        sslctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        sslctx.check_hostname = False
        sslctx.load_cert_chain(certfile=certfilelocation, keyfile=keyfilelocation)
        httpd.socket = sslctx.wrap_socket(httpd.socket, server_side=True)
        print("HTTPS is enabled! :)") #les goo https!!
    else:
        print("Running in HTTP mode. :/") #meh its ok but you have to manually type it in nowadays
    if server_address[0] == '': printserver = '127.0.0.1 or localhost'
    else: printserver = server_address[0]
    print(f"SebbyWebServer\nServing on {printserver}:{server_address[1]}\nPress Ctrl+C to stop") #gotta tell chat how it works bro
    try:
        httpd.serve_forever()
    except KeyboardInterrupt: #stop server when Ctrl+C pressed
        pass
    print("Stopping server...")
    httpd.server_close() #close it properly man
    print("Stopped.") #It's now safe to turn off your computer (ain't nobody gonna get this reference)