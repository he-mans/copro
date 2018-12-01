import socket
import os
from PIL import Image as PilImage
import pickle
import sqlite3
import traceback


class account:
    
    def __init__(self, first, last , email, password,user_id):
        self.first = first
        self.last = last
        self.email = email
        self.password = password
        self.id = user_id
        self.profile_pic = f"account_user{self.id}/profile_pic_user{self.id}/propic.jpg"
        self.thumbnail = f"account_user{self.id}/thumbnail_user{self.id}/thumbnail.jpg"
        self.feed_thumbnail = f"account_user{self.id}/thumbnail_user{self.id}/feed_thumbnail.jpg"
        self.friend_req = ""
        self.friend_list = ""
        self.sent = ""

def create_account(first,last,email,password):
    
    conn_create = sqlite3.connect("copro.db")
    cursor_create  = conn_create.cursor()

    first,last,email,password = first.strip().upper(),last.strip().upper(),email.strip(),password.strip()
    with conn_create:  
        cursor_create.execute("""SELECT * FROM accounts
                     WHERE email = (:email)""",{"email":email})
        if cursor_create.fetchone() is not None:
            return 0
        else:
            with open("user count.txt","r") as f:
                current_users = int(f.read())
            member = account(first,last,email,password,current_users)
            with open("user count.txt","w") as f:    
                f.truncate(0)
                f.write(str(current_users+1))
            if not os.path.exists(f"account_user{current_users}"):
                os.makedirs(f"account_user{current_users}/feed_user{current_users}")
                os.chdir(f"account_user{current_users}")
                os.mkdir(f"profile_pic_user{current_users}")
                os.mkdir(f"thumbnail_user{current_users}")
                os.chdir("..")
            image = PilImage.open("default_icons/default_propic.jpg")
            image.save(f"account_user{current_users}/profile_pic_user{current_users}/propic.jpg")
            image = PilImage.open("default_icons/default_thumbnail.jpg")
            image.save(f"account_user{current_users}/thumbnail_user{current_users}/thumbnail.jpg")
            image = PilImage.open("default_icons/default_feed_thumbnail.jpg")
            image.save(f"account_user{current_users}/thumbnail_user{current_users}/feed_thumbnail.jpg")
            
            cursor_create.execute("""INSERT INTO accounts
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


def main():
    
    port = 2000
    
    print("creating socket")
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print("server socket created")

    print("binding socket")
    s.bind(('',port))
    print("server binded to port")

    s.listen(4)
    print("server started listening")

    while True:
        try:
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
        except Exception as e:
            print('server_create_account raised exception :',end = ' ')
            print(e)
            print('traceback for above create_account error')
            traceback.print_exc()
            break
        c.close()
    
    s.close()

if __name__ == '__main__':
    main()