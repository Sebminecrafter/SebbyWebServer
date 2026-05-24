# SebbyWebServer by Sebminecrafter

import http.server, os, ssl, mimetypes, yaml
from pathlib import Path

ver = 1.3
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
        self.ssl_keyfile = ""
        self.ssl_certfile = ""

        self.append = ""
        self.notfoundpage = ""

        # Load if file exists
        if self.path.exists():
            self._load()

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

def evalRequest(path, config):
    output = None
    if path in codePaths:
        output = eval(f"{codePathFuncs[codePaths.index(path)]}()")
        status = 200
        type = 'text/html'
    else:
        path2 = f"{os.getcwd()}{path}"
        if os.path.isfile(path2):
            status = 200
            if str(mimetypes.guess_file_type(path2)[0]) == 'text/html':
                with open(path2, 'r') as f:
                    output = f.read()
                    output = f"{output}{config.append}".encode('UTF-8')
                type = 'text/html'
            else:
                with open(path2, 'rb') as f:
                    output = f.read()
                type = str(mimetypes.guess_file_type(path2)[0])
        elif os.path.isfile(f"{path2}index.html"):
            with open(f"{path2}index.html") as f:
                output = f.read()
                status = 200
                output = f"{output}{config.append}".encode('UTF-8')
                type = 'text/html'
        elif os.path.isfile(f"{path2}/index.html"):
            with open(f"{path2}/index.html") as f:
                output = f.read()
                status = 200
                output = f"{output}{config.append}".encode('UTF-8')
                type = 'text/html'
        else:
            status = 404
            output = f"{config.notfoundpage.replace("PATH",path)}{config.append}".encode('UTF-8')
            type = 'text/html'
    
    return output, status, type

class SebbyServer(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        response = evalRequest(self.path, config)
        self.send_response(response[1])
        self.send_header("Content-type", response[2])
        self.end_headers()
        self.wfile.write(response[0])

if __name__ == '__main__':
    config = Config("config.yml")
    server_address = (config.host, config.port)
    httpd = http.server.ThreadingHTTPServer(server_address, SebbyServer)
    if config.ssl_enabled:
        sslctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        sslctx.check_hostname = False
        sslctx.load_cert_chain(config.ssl_certfile, config.ssl_keyfile)
        httpd.socket = sslctx.wrap_socket(httpd.socket, server_side=True)
        print("HTTPS is enabled")
    else:
        print("HTTPS is disabled")
    if server_address[0] == '': printserver = '127.0.0.1 or localhost'
    else: printserver = server_address[0]
    print("SebbyWebServer")
    print("Serving on", printserver, ":", server_address[1])
    print("Press Ctrl+C to stop")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt: # Stop the server if Ctrl+C pressed
        print("Stopping server...")
        httpd.server_close() # Close the server
        pass
    print("Stopped.")