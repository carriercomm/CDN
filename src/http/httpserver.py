from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urllib2



class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        request = "http://" + self.origin + ":8080" + self.path

        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        try:
            response = self.cache[self.path]
            # cache hit
            self.wfile.write(response.read())
        except KeyError as e:
            # cache miss
            response = urllib2.urlopen(request)
            self.cache[self.path] = response
            self.wfile.write(response.read())
        return

def run(port, origin):
    try:
        handler = HttpHandler
        handler.origin = origin

        handler.cache = {}

        server = HTTPServer(("",port),handler)
        print "Started server at ", server.socket.getsockname()
        server.serve_forever()
    except KeyboardInterrupt:
        print "Keyboard Interrupt"
        server.socket.close()
