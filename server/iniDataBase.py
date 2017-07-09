#initialize database
import sqlite3 as lite
def initialize():
    NAME = "bikedb.sqlite"
    con = lite.connect(NAME)
    c = con.cursor()
    c.execute(
       """CREATE TABLE Bikes(
       Bid INT NOT NULL,
       Blng INT,
       Blat INT,
       PRIMARY KEY (Bid)
     )""")
#hard code data
    c.execute("""
        INSERT INTO Bikes VALUES(10017202,3118069,12159400);

    """)
    c.execute("""
        INSERT INTO Bikes VALUES(10029583,3123929,-1213023);
    """)
    c.execute("""
        INSERT INTO Bikes VALUES(10100962,3118069,12159400);
    """)
    c.execute("""
        INSERT INTO Bikes VALUES(10130335,3118069,12159400);
    """)
    c.execute("""
        INSERT INTO Bikes VALUES(10302884,3118069,12159400);
    """)
    con.commit()
    con.close
initialize()