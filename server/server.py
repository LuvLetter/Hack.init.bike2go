
#!/usr/bin/env python
from http.server import BaseHTTPRequestHandler, HTTPServer
# import MySQLdb
# import os
from bikeObj import bike
import sqlite3 as lite
bikeNo = 1
NAME = "bikedb.sqlite"
con = lite.connect(NAME)
c = con.cursor()
c.execute(
"SELECT * FROM Bikes WHERE Bid = %d"%bikeNo
)
rows = c.fetchall()
thisBike = bike(*rows[0])

# ssl_cert = "/home/jhl/client-cert.pem"
# ssl_key = "/home/jhl/client-key.pem"
# ssl_ca = "/home/jhl/server-ca.pem"
# print()
# cnx = MySQLdb.connector.connect(user='scott', password='tiger',
#                               host='127.0.0.1',
#                               database='employees')
# cnx = MySQLdb.connect(user='joe', database='test')
# cnx = MySQLConnection(user='joe', database='test')
# db = MySQLdb.connect(
#           host='35.190.234.86',
          # ssl_ca = "/home/jhl/Desktop/client/server-ca.pem",
          # ssl_cert = "/home/jhl/Desktop/client/client-cert.pem",
          # ssl_key = "/home/jhl/Desktop/client/client-key.pem",
          # user='jhl', passwd='13757121426')
# cnx = mysql.connector.connect(user='jhl', database='bikes')
# cnx = MySQLConnection(user='jhl', database='bikes')

# https://docs.python.org/3/library/csv.html
#sample data
# with open('bikeList.csv', 'w') as csvfile:
#     fieldnames = ['bikeId','n', 'e','d','status','location']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()
#     writer.writerow({'bikeId': '1','n':'123','e': '123','d':'123','status':"1",'location':'1'})
    # writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
    # writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})

def decrypt(bike):
  return 1

def isLegalRequest(bike):
  if(decrypt(bike)!=bike.bikeId):                                       
    return False
  return True

def updateLocation(bike,lng,lat):
  if(isLegalRequest(bike)):
    bike.lng = lng
    bike.lat = lat
  return

def updateStatus(bike, status):
  if(isLegalRequest(bike)):
    bike.status = status
  return

def update(bike, bikeStatus):
  updateLocation(bike,lng,lat)
  updateStatus(bike, bikeStatus)
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



