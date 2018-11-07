import sqlite3

conn = sqlite3.connect("copro.db")
c  = conn.cursor()

with conn:
   c.execute("""CREATE TABLE accounts(
                   id INT,
                   first TEXT,
                   last TEXT,
                   email TEXT,
                   password TEXT,
                   propic TEXT,
                   thumbnail TEXT,
                   feed_thumbnail TEXT,
                   friend_req TEXT,
                   friend_list TEXT,
                   sent TEXT)""")

f=open("user count.txt","w")
f.write("0")
f.close()

print("database created")
print("user count file created")