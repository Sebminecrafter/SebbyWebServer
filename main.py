# Sebby Web Server
# Code by Sebminecrafter
# Warning: Not fully tested for security
# Not for production use (yet)
from http.server import *
from pathlib import Path
import os, ssl, mimetypes
try:
    import yaml
except ImportError:
    print("SebbyWebServer requires PyYAML")
    print("It can be installed with 'pip install pyyaml'")
    if input("Type Y to install it now").lower()=='y':
        os.system("pip install pyyaml")
    else:
        from sys import exit
        exit(1)
    import yaml
ver = 1.2
strver = str(ver)
codePaths = []
codePathFuncs = []
mimetypes.init()

class Config:
    def __init__(self, path: str = "config.yml"):
        self.path = Path(path)

        # Defaults
        self.port = 80
        self.host = ""

        self.ssl_enabled = False
        self.ssl_keyfile = None
        self.ssl_certfile = None

        self.append = ""
        self.notfoundpage = ""

        # Load if file exists
        if self.path.exists():
            self._load(self)

    def _load(self):
        with self.path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        self.port = data.get("port", self.port)
        self.host = data.get("host", self.host)

        ssl = data.get("ssl", {})
        self.ssl_enabled = ssl.get("enabled", self.ssl_enabled)
        self.ssl_keyfile = ssl.get("keyfile", self.ssl_keyfile)
        self.ssl_certfile = ssl.get("certfile", self.ssl_certfile)

        self.append = data.get("append", self.append)
        self.append = self.append.replace("VER", str(ver))
        self.notfoundpage = data.get("notfoundpage", self.notfoundpage)
    def save(self):
        data = {
            "port": self.port,
            "host": self.host,
            "ssl": {
                "enabled": self.ssl_enabled,
                "keyfile": self.ssl_keyfile,
                "certfile": self.ssl_certfile,
            },
            "append": self.append,
            "notfoundpage": self.notfoundpage,
        }

        with self.path.open("w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, sort_keys=False)
    def __repr__(self):
        return (
            f"Config(port={self.port}, host={self.host!r}, "
            f"ssl_enabled={self.ssl_enabled}, "
            f"ssl_keyfile={self.ssl_keyfile!r}, "
            f"ssl_certfile={self.ssl_certfile!r}, "
            f"append={self.append!r}, "
            f"notfoundpage={self.notfoundpage!r})"
        )

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
                    output = f"{output}{Config.append}".encode('UTF-8')
                type = 'text/html'
            else:
                with open(path2, 'rb') as f:
                    output = f.read()
                type = str(mimetypes.guess_file_type(path2)[0])
        elif os.path.isfile(f"{path2}index.html"):
            with open(f"{path2}index.html") as f:
                output = f.read()
                status = 200
                output = f"{output}{Config.append}".encode('UTF-8')
                type = 'text/html'
        elif os.path.isfile(f"{path2}/index.html"):
            with open(f"{path2}/index.html") as f:
                output = f.read()
                status = 200
                output = f"{output}{Config.append}".encode('UTF-8')
                type = 'text/html'
        else:
            cr404page = Config.notfoundpage.replace("PATH",path)
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

if __name__ == '__main__':
    Config.__init__(Config, "config.yml")
    server_address = (Config.host, Config.port)
    httpd = ThreadingHTTPServer(server_address, SebbyServer)
    if Config.ssl_enabled:
        sslctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        sslctx.check_hostname = False
        sslctx.load_cert_chain(certfile=Config.ssl_certfile, keyfile=Config.ssl_keyfile)
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