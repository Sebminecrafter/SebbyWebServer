# SebbyWebServer

A simple Python webserver.
Provided in this repo are example files and the code.

## Features

- Custom Python functions
- Only requires one external module, `pyyaml`
- Compatible with Python 3.13 or 3.14
- Single Python file and config
- Simple and open!

## Config

You can configure various features of SebbyWebServer via the `config.yml` file

- `port`: The TCP port to run the server on (default: `80`), HTTP uses `80`, and HTTPS uses `443`, but you can use any valid port number.
- `host`: The hostname (default: `""`). This isn't required but should be set outside of testing environments.
- `ssl`: SSL section of the configuration.
  - `enabled`: Whether or not to enable SSL (default: `false`). Can be `true` or `false`
  - `keyfile`: `"cert/private.key"`
  - `certfile`: `"cert/cert.pem"`
- `append`: The text/html appended at end of any HTML page, you may use VER for version. (default: `"\n<br><p>Running SebbyWebServer Version VER</p>"`)
- `notfoundpage`: The file not found (404) page, you may use PATH for the path. (default: `"<h1>404 Not found: PATH</h1>"`)

## Functions

SebbyWebServer allows you to add custom functions written in Python,
meaning custom paths or features that can be useful for both frontend and backend.

You can add a function by putting it in `publicf/`.
These functions will act as normal HTML paths, etc. to the end user.
All functions are navigable to their path and name, excluding the `.py` extension.
The functions must have a `main(request)` function that returns a tuple of:
a str or bytes object, status (int), output type (str),
like `tuple["Example", 200, 'text/plain']`.

Anything else in `/public` will just be treated as normal files.
They are navigable via their direct paths (in public).
