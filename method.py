#! /usr/bin/env python

# Our tutorial's WSGI server
from wsgiref.simple_server import make_server

# This is our application object. It could have any name,
# except when using mod_wsgi where it must be "application"
def application( # It accepts two arguments:
      # environ points to a dictionary containing CGI like environment variables
      # which is filled by the server for each received request from the client
      environ,
      # start_response is a callback function supplied by the server
      # which will be used to send the HTTP status and headers to the server
      start_response):

   # build the response body possibly using the environ dictionary
   response_body = 'The request method was %s' % environ['REQUEST_METHOD']

   # HTTP response code and message
   status = '200 OK'

   # These are HTTP headers expected by the client.
   # They must be wrapped as a list of tupled pairs:
   # [(Header name, Header value)].
   response_headers = [('Content-Type', 'text/plain'),
                       ('Content-Length', str(len(response_body)))]

   # Send them to the server using the supplied function
   start_response(status, response_headers)

   # Return the response body.
   # Notice it is wrapped in a list although it could be any iterable.
   return [response_body]

# Instantiate the WSGI server.
# It will receive the request, pass it to the application
# and send the application's response to the client
httpd = make_server(
   'localhost', # The host name.
   8051, # A port number where to wait for the request.
   application # Our application object name, in this case a function.
   )

# Wait for a single request, serve it and quit.
httpd.handle_request()