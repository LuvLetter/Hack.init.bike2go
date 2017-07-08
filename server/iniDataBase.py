#initialize database
import sqlite3 as lite
def initialize():
    NAME = "bikedb.sqlite"
    con = lite.connect(NAME)
    c = con.cursor()
    c.execute(
       """CREATE TABLE Bikes(
       Bid INT NOT NULL,
       N INT NOT NULL,
       E INT NOT NULL,
       D INT NOT NULL,
       Bsta INT NOT NULL,
       Blng INT,
       Blat INT,
       PRIMARY KEY (Bid)
     )""")
#hard code data
    c.execute("""
        INSERT INTO Bikes VALUES(0001,20891,7709,5,22,3118069,12159400);
    """)
    con.commit()
    con.close
initialize()