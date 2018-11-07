import socket
import os
from PIL import Image as PilImage
import pickle
import sqlite3



class account:
    
    def __init__(self, first, last , email, password):
        self.first = first
        self.last = last
        self.email = email
        self.password = password
        self.profile_pic = f"account_user{self.email}/profile_pic_user{self.email}/propic.jpg"
        self.thumbnail = f"account_user{self.email}/thumbnail_user{self.email}/thumbnail.jpg"
        self.feed_thumbnail = f"account_user{self.email}/thumbnail_user{self.email}/feed_thumbnail.jpg"
        self.friend_req = ""
        self.friend_list = ""
        self.sent = ""

def create_account(first,last,email,password):
    
    conn = sqlite3.connect("copro.db")
    c  = conn.cursor()

    first,last,email,password = first.strip(),last.strip(),email.strip(),password.strip()
    with conn:  
        c.execute("""SELECT * FROM accounts
                     WHERE email = (:email)""",{"email":email})
        if c.fetchone() is not None:
            return 0
        else:
            member = account(first,last,email,password)
            with open("user count.txt","r") as f:
                current_users = int(f.read())
            with open("user count.txt","w") as f:    
                f.truncate(0)
                f.write(str(current_users+1))
            if not os.path.exists(f"account_user{email}"):
                os.makedirs(f"account_user{email}/feed_user{email}")
                os.chdir(f"account_user{email}")
                os.mkdir(f"profile_pic_user{email}")
                os.mkdir(f"thumbnail_user{email}")
                os.chdir("..")
            image = PilImage.open("default_icons/default_propic.jpg")
            image.save(f"account_user{email}/profile_pic_user{email}/propic.jpg")
            image = PilImage.open("default_icons/default_thumbnail.jpg")
            image.save(f"account_user{email}/thumbnail_user{email}/thumbnail.jpg")
            image = PilImage.open("default_icons/default_feed_thumbnail.jpg")
            image.save(f"account_user{email}/thumbnail_user{email}/feed_thumbnail.jpg")
            
            c.execute("""INSERT INTO accounts
                        VALUES(:id,:first, :last, :email,:password,:propic,
                                :thumbnail,:feed_thumbnail,:friend_req,:friend_list,:sent)""",{
                         "id":current_users,
                         "first":member.first,
                         "last":member.last,
                         "email":member.email,
                         "password":member.password,
                         "propic":member.profile_pic,
                         "thumbnail":member.thumbnail,
                         "feed_thumbnail":member.feed_thumbnail,
                         "friend_req":member.friend_req,
                         "friend_list":member.friend_list,
                         "sent":member.sent
                         })
            
            return 1


port = 2000
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("server socket created")

s.bind(('',port))
print("server binded to port 1000")

s.listen(4)
print("server started listening")

while True:
    c,add = s.accept()
    print("client accepted")
    
    print("receving account details")
    account_details = pickle.loads(c.recv(4096))
    print("details received")

    print("creating account")
    return_status = create_account(account_details[0],account_details[1],account_details[2],account_details[3])

    print("sending return status of server")
    c.sendall(pickle.dumps(return_status))
    print("sent")
    c.close()

s.close()



