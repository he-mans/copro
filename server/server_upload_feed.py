import socket
import os 
import pickle
from PIL import Image as PilImage
import sqlite3
import datetime
import traceback

def get_friend_list(user_id):
    conn_upload_feed = sqlite3.connect('copro.db')
    cursor_upload = conn_upload_feed.cursor()

    with conn_upload_feed:
        cursor_upload.execute("""SELECT friend_list 
                    FROM accounts WHERE id = (:id)""",{
                    "id":int(user_id)
                    })
        friend_list = cursor_upload.fetchone()[0]
    return friend_list


def upload(image,user_id,friend_list,upload_time):
    for friend in friend_list:
        if(friend==""):
            continue
        image.save(f"account_user{friend}/feed_user{friend}/{upload_time}_image_account-{user_id}.jpg")


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
        try:
            c,add = s.accept()
            print("client accepted")

            add_str = str(add)
            add_str = add_str.replace("(","")
            add_str = add_str.replace(")","")

            print('receiving user id')
            user_id = c.recv(4096).decode('utf-8')
            c.sendall("id received by server".encode())
            print("id received")

            print('receiving image')
            with open(f'image_upload_feed_user.pickle_user_{add_str}','wb') as f:
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
        
            with open(f'image_upload_feed_user.pickle_user_{add_str}','rb') as f:
                image = pickle.load(f)

            friend_list = get_friend_list(user_id)
                
            friend_list = friend_list.split(" ")
            image.thumbnail((460,460))
            upload_time = str(datetime.datetime.now())
            upload_time=upload_time.replace(":","$")
            image.save(f"account_user{user_id}/{upload_time}_image_account-{user_id}.jpg")
            image.save(f"account_user{user_id}/feed_user{user_id}/{upload_time}_image_account-{user_id}.jpg")
            f=open(f"account_user{user_id}/{upload_time}_image_account-{user_id}.txt","w")
            f.write("0")
            f.close()
            f=open(f"account_user{user_id}/{upload_time}_image_account-{user_id}_people_liked.txt","a").close()
            
            upload(image,user_id,friend_list,upload_time)
            
            os.remove(f'image_upload_feed_user.pickle_user_{add_str}')
        except Exception as e:
            print(e)
            traceback.print_exc()
            break
        c.close()
    s.close()

if __name__ == '__main__':
    main()