
#!/usr/bin/env python
 
from http.server import BaseHTTPRequestHandler, HTTPServer
import MySQLdb
import mysql
import os


ssl_cert = "/home/jhl/client-cert.pem"
ssl_key = "/home/jhl/client-key.pem"
ssl_ca = "/home/jhl/server-ca.pem"

# cnx = MySQLdb.connector.connect(user='scott', password='tiger',
#                               host='127.0.0.1',
#                               database='employees')
cnx = mysql.connector.connect(user='joe', database='test')
cnx = MySQLConnection(user='joe', database='test')
db = mysql.connect(
          host='35.190.234.86',
          # ssl_ca = "/home/jhl/Desktop/client/server-ca.pem",
          # ssl_cert = "/home/jhl/Desktop/client/client-cert.pem",
          # ssl_key = "/home/jhl/Desktop/client/client-key.pem",
          user='root', passwd='13757121426')

# cnx = mysql.connector.connect(user='jhl', database='bikes')
# cnx = MySQLConnection(user='jhl', database='bikes')

def isLegalRequest(bikeId, bikeStatus):
  if(0==1):                                       
    return False
  return True

def updateLocation(bikeId,bikeStatus):
  return

def updateStatus(bikeId, bikeStatus):
  return

def update(bikeId, bikeStatus):
  updateLocation(bikeId,bikeStatus)
  updateStatus(bikeId, bikeStatus)
  return 


def getPassword(bikeId,bikeStatus):
  if isLegalRequest(bikeId, bikeStatus):
    return "123"
  return

# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
 
  # GET
  def do_GET(self):
        # Send response status code
        self.send_response(200)
 
        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()
 
        # Send message back to client
        message = "Hello world!"
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return
 
def run():
  print('starting server...')
 
  # Server settings
  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  server_address = ('127.0.0.1', 3306)
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('running server...')
  httpd.serve_forever()
 
 
run()



