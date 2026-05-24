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

## Functions

SebbyWebServer allows you to add custom functions written in Python,
meaning custom paths or features that can be useful for both frontend and backend.

You can add a function by putting it in `publicf/`.
These functions will act as normal HTML paths, etc. to the end user.
All functions are navigable to their path and name, excluding the `.py` extension.
They must return a tuple of a str or bytes object, status (int), output type (str).
Like `tuple["Example", 200, 'text/plain']`.

Anything else in `/public` will just be treated as normal files.
They are navigable via their direct paths (in public).
