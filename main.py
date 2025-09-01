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
                    output = f.read()
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
            cr404page = notfoundpage.replace("PATH",path)
            output = cr404page.encode('UTF-8')
            status = 404
            type = 'text/html'
    return output,status,type

class SebbyServer(BaseHTTPRequestHandler): #just runs another function -_-
    def do_GET(self):
        response = evalRequest(self.path)
        self.send_response(response[1])
        self.send_header("Content-type", response[2]); self.end_headers()
        self.wfile.write(response[0])


port = 80; host = ''; keyfilelocation = ''; certfilelocation = ''; sebby_using_ssl = False; handler_class=SebbyServer; append = f"\n<br><center><p>Running SebbyWebServer Version {strver}</p></center>"; notfoundpage = "<h1>404 File/Function not found: PATH</h1>"
#Load config file
try:
    with open('config.txt', 'r') as config:
        for i in config.readlines():
            exec(i)
        config.close() #close file cuz yes
except Exception:
    print("Failed to load config file, making you a new one")
    #make a new config if one does not exist
    with open('config.txt', 'w') as config:
        config.write("""#NOTICE: THIS WILL BE INTERPRETED AS CODE, BE CAREFUL AND READ ANYTHING BEFORE YOU PUT IT IN HERE
#                                                                                 --------------------------------Config--------------------------------
port = 443                                                                        #Which port to serve on (default for http is 80, https is 443)
host = ''                                                                         #Hostname/ip change if you aren't just devtesting
keyfilelocation = 'cert/private.key'                                              #Only required for ssl, location of your key file (private.key)
certfilelocation = 'cert/cert.pem'                                                #Only required for ssl, location of your certificate (cert.pem)
sebby_using_ssl = True                                                            #Whether you are using SSL (HTTPS) or not (HTTP)
handler_class=SebbyServer                                                         #Only change if you are testing/editing/etc.
append = f"\\n<br><center><p>Running SebbyWebServer Version {strver}</p></center>"#Appended at end of page
notfoundpage = "<h1>404 File/Function not found: PATH</h1>"                       #File not found (404) page you can use PATH for the path""")
        config.close() #close file

if __name__ == '__main__':
    server_address = (host, port)
    httpd = ThreadingHTTPServer(server_address, handler_class)
    if sebby_using_ssl:
        sslctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        sslctx.check_hostname = False
        sslctx.load_cert_chain(certfile=certfilelocation, keyfile=keyfilelocation)
        httpd.socket = sslctx.wrap_socket(httpd.socket, server_side=True)
        print("HTTPS is enabled")
    else:
        print("HTTPS is disabled")
    if server_address[0] == '': printserver = '127.0.0.1 or localhost'
    else: printserver = server_address[0]
    print(f"SebbyWebServer\nServing on {printserver}:{server_address[1]}\nPress Ctrl+C to stop") #gotta tell chat how it works bro
    try:
        httpd.serve_forever()
    except KeyboardInterrupt: #stop server when Ctrl+C pressed
        pass
    print("Stopping server...")
    httpd.server_close() #close the server
    print("Stopped.")