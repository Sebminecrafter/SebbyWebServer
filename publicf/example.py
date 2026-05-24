def main(request):
    output = f"<h1>Example test on {request.path}</h1>"
    status = 200
    outputtype = 'text/html'
    return output, status, outputtype