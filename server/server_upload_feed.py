import socket
import os 
import pickle
from PIL import Image as PilImage
import sqlite3
import datetime


def main():

    port = 4000

    print("creating socket")
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print("socket created")

    print("binding socket")
    s.bind(('',port))
    print("socket binded")

    s.listen(4)
    print("started listening")

    while True:
        c,add = s.accept()
        print("client accepted")

        print('receiving email')
        user_email = c.recv(4096).decode('utf-8')
        c.sendall("email received by server".encode())
        print("email received")

        print('receiving image')
        with open("image_upload_feed.pickle",'wb') as f:
            data = c.recv(4096)
            while data:
                if data.endswith(b'no more data'):
                    data = data.split(b'no more data')[0]
                    f.write(data)
                    break
                f.write(data)
                data = c.recv(4096)
        print("image_received")

        c.close()
        
        with open('image_upload_feed.pickle','rb') as f:
            image = pickle.load(f)

        os.remove('image_upload_feed.pickle')

        conn_upload_feed = sqlite3.connect('copro.db')
        cursor_upload = conn_upload_feed.cursor()

        with conn_upload_feed:
            cursor_upload.execute("""SELECT id,friend_list 
                        FROM accounts WHERE email = (:email)""",{
                        "email":user_email
                        })
            user_id,friend_list = cursor_upload.fetchone()
            friend_list = friend_list.split(" ")
            image.thumbnail((480,480))
            upload_time = str(datetime.datetime.now())
            image.save(f"account_user{user_email}/{upload_time}_image_account-{user_id}.jpg")
            image.save(f"account_user{user_email}/feed_user{user_email}/{upload_time}_image_account-{user_id}.jpg")
            f=open(f"account_user{user_email}/{upload_time}_image_account-{user_id}.txt","w")
            f.write("0")
            f.close()
            f=open(f"account_user{user_email}/{upload_time}_image_account-{user_id}_people_liked.txt","a").close()
        
            for friend in friend_list:
                if(friend==""):
                    continue
                cursor_upload.execute("""SELECT email FROM accounts
                            WHERE id = (:id)""",{
                            "id":int(friend)
                            })
                friend = cursor_upload.fetchone()[0]
                image.save(f"account_user{friend}/feed_user{friend}/{upload_time}_image_account-{user_id}.jpg")

    s.close()