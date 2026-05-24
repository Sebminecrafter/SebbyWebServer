# SebbyWebServer by Sebminecrafter

import http.server, os, ssl, mimetypes, yaml, importlib.util
from pathlib import Path

ver = 2.0
strver = str(ver)
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

def loadFunction(path, req) -> tuple[bytes, int, str]:
    module_path = Path(path)
    try:
        spec = importlib.util.spec_from_file_location(module_path.stem, module_path)
        if spec is None or spec.loader is None:
            raise ImportError("Cannot load module")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        fresult = module.main(req)
        if isinstance(fresult, tuple) and len(fresult) == 3:
            output, status, outputtype = fresult
        else:
            output = str(fresult)
            status = 200
            outputtype = 'text/html'
    except Exception:
        output = "<h1>500 internal server error</h1><h2>An error occured processing that request</h2>"
        status = 500
        outputtype = 'text/html'

    if isinstance(output, str):
        output = output.encode('utf-8')
    elif not isinstance(output, (bytes, bytearray)):
        output = str(output).encode('utf-8')

    return output, status, outputtype

def evalRequest(req, config) -> tuple[bytes, int, str]:
    path = req.path
    path = path.split("?", 1)[0]
    path = path.lstrip("/")
    path = os.path.normpath(path)
    if path.startswith(".."):
        path = ""

    public = Path(os.getcwd()) / "public"
    publicf = Path(os.getcwd()) / "publicf"
    ppath = public / path
    fpath = f"{publicf / path}.py"

    # Check for function file
    if os.path.isfile(fpath):
        output, status, outputtype = loadFunction(str(fpath), req)

    # Check for normal file path
    elif ppath.is_file():
        status = 200
        if mimetypes.guess_type(str(ppath))[0] == 'text/html':
            with open(ppath, 'r', encoding='utf-8') as f:
                output = f.read()
                output = f"{output}{config.append}".encode('UTF-8')
            outputtype = 'text/html'
        else:
            with open(ppath, 'rb') as f:
                output = f.read()
            outputtype = mimetypes.guess_type(str(ppath))[0] or 'application/octet-stream'

    elif (ppath / "index.html").is_file():
        with open(ppath / "index.html", 'r', encoding='utf-8') as f:
            output = f.read()
            output = f"{output}{config.append}".encode('UTF-8')
        status = 200
        outputtype = 'text/html'

    else:
        output = f"{config.notfoundpage.replace('PATH', path)}{config.append}".encode('UTF-8')
        status = 404
        outputtype = 'text/html'
    
    if type(output) == str:
        output = output.encode('UTF-8')
    
    return output, status, outputtype

class SebbyServer(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        response = evalRequest(self, config)
        self.send_response(response[1])
        self.send_header("Content-type", response[2])
        self.end_headers()
        self.wfile.write(response[0])
    def do_POST(self):
        self.do_GET()

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