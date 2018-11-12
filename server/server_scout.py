import socket
from PIL import Image as PilImage
import os
import pickle
import sqlite3
import datetime


def main():

    port = 6000

    conn_scout = sqlite3.connect('copro.db')
    cursor_scout = conn_scout.cursor()

    print("creating socket")
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print('socket created')

    print('binding socket')
    s.bind(('',port))
    print('socket binded')

    s.listen(4)
    print('scoket started listening')

    while True:
        c,add = s.accept()
        print('client accepted')

        print('receiving details')
        person_email,person_id = pickle.loads(c.recv(4096))
        c.sendall('details received by server'.encode())
        print('received')
        
        os.chdir(f"account_user{person_email}")
        posts = os.listdir()
        images_name = [image for image in posts if image.endswith(".txt") is False and os.path.isdir(image) is False]
        images_name = sorted(images_name,key=lambda x: datetime.datetime.strptime(x.split("_")[0],'%Y-%m-%d %H:%M:%S.%f'))
        
        print('sending images names')
        c.sendall(pickle.dumps(images_name))
        print(c.recv(4096))
        
        images = [PilImage.open(image) for image in images_name]
        
        with open('images_scout.pickle','wb') as f:
            pickle.dump(images,f)

        print('sending images')
        with open('images_scout.pickle','rb') as f:
            data = f.read(4096)
            while data:
                c.sendall(data)
                data = f.read(4096)
            c.sendall(b'no more data')
        print(c.recv(4096))
        os.remove('images_scout.pickle')

        likes_file = [image.replace(".jpg",".txt") for image in images_name]
        people_liked_files = [file.replace(".txt","_people_liked.txt") for file in likes_file]
        people_liked=[]
        likes = []
        
        for file in likes_file:
            with open(file,"r") as f:
                likes.append(f.read())
        
        for file in people_liked_files:
            with open(file,"r") as f:
                people__ = [lines.strip() for lines in f.readlines()]
                people_liked.append(people__)

        print('sending likes and people liked')
        c.sendall(pickle.dumps([likes,people_liked]))
        print(c.recv(4096))
        
        os.chdir('..')
        
        with conn_scout:
            cursor_scout.execute("""SELECT propic,feed_thumbnail FROM accounts
                        WHERE id = (:person_id)""",{
                        "person_id":person_id
                        })
            person_propic,thumbnail = cursor_scout.fetchone()
        print(os.getcwd())
        pro_and_thu = [PilImage.open(person_propic),PilImage.open(thumbnail)]

        print("sending propic and thumbanil")
        with open('pro_and_thu_scout.pickle','wb') as f:
            pickle.dump(pro_and_thu,f)
        with open('pro_and_thu_scout.pickle','rb') as f:
            data = f.read(4096)
            while data:
                c.sendall(data)
                data = f.read(4096)
            c.sendall(b'no more data')

        print(c.recv(4096))

        os.remove('pro_and_thu_scout.pickle') 