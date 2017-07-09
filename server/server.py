#!/usr/bin/env python
from http.server import BaseHTTPRequestHandler, HTTPServer
# import MySQLdb
# import os
from bikeObj import bike
import sqlite3 as lite
# import aes
import urllib

def enc():
  bikeno = 1001
  result = 0
  while(bikeno>0):
    result = result*31 + bikeno%10
    bikeno = bikeno//10
  return result

# def check(bike):
#   bikeno = bike.bikeId
#   length = len(s)
#   result = 0
#   while(bikeno>0):
#     result = result*31 + bikeno%10
#     bikeno = bikeno//10
#   return (result%10000) == bike.encrypted

 
NAME = "bikedb.sqlite"
con = lite.connect(NAME)
c = con.cursor()

# did not use cloud SQL due to the complexity of making the server
# ssl_cert = "/home/jhl/client-cert.pem"
# ssl_key = "/home/jhl/client-key.pem"
# ssl_ca = "/home/jhl/server-ca.pem"
# print()
# db = MySQLdb.connect(
#           host='35.190.234.86',
          # ssl_ca = "/home/jhl/Desktop/client/server-ca.pem",
          # ssl_cert = "/home/jhl/Desktop/client/client-cert.pem",
          # ssl_key = "/home/jhl/Desktop/client/client-key.pem",
          # user='jhl', passwd='')
# cnx = mysql.connector.connect(user='jhl', database='bikes')
# cnx = MySQLConnection(user='jhl', database='bikes')

def check(ssid):
  result = 0
  firstFour = int(ssid[1:])//10000
  print(firstFour)
  while(firstFour>0):
    result = result*31 + firstFour%10
    firstFour = firstFour//10
  print(result)
  return (result%10000) == int(ssid[1:])%10000


# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
  # GET
  def do_GET(self):

        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()
        got = self.path
        L = got.split("/")
        print(L)
        if not (L[1]== "unlock")or(L[1]=="noAction"):
          return
        SSID = L[2]
        print(check(SSID))
        if not(check(SSID)):
            self.wfile.write(bytes("wrong", "utf8"))
            return "error"
        if(L[1]=="unlock"):
          if(check(SSID)):
            password = (104729-(int(SSID[1:])%10000))%10000
            self.wfile.write(bytes(str(password), "utf8"))
            return str(password)
        lng = L[4]
        lat = L[5]
        if(L[3]=="update"):
            lng = str(int(L[4])*10000)
            lat = str(int(L[5])*10000)
            bk = bike(int(L[2][1:]),lng,lat)
            c.cursor("""
              UPDATE Bikes SET Blng = %s WHERE name = %s 
              """%(lng, name)
            )
            c.cursor("""
              UPDATE Bikes SET Blat = %s WHERE name = %s 
              """%(lat,name)
            )
            con.commit()
            con.close

        # parsed_path = urlparse(self.path)
        # Send message back to client
        message = "Hello world!"
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return

def run():
  print('starting server...')

  # Server settings
  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  server_address = ('0.0.0.0', 23000)
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('running server...')
  httpd.serve_forever()


run()
