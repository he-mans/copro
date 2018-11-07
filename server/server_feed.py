import socket
import os
import pickle
from PIL import Image as PilImage 
import sqlite3
import datetime


def get_image_names(email):
    os.chdir(f"account_user{email}/feed_user{email}")
    ls = os.listdir()
    ls = [image for image in ls if image.endswith(".txt") is False]
    ls = sorted(ls,key = lambda x: datetime.datetime.strptime(x.split('_')[0],'%Y-%m-%d %H:%M:%S.%f'))    
    os.chdir('..')
    os.chdir('..')
    return ls

    
def get_user_details(u_email,ls):
    
    conn = sqlite3.connect("copro.db")
    c = conn.cursor()
    os.chdir(f"account_user{u_email}/feed_user{u_email}")

    ids = [image.split("-")[-1].split(".jpg")[0] for image in ls]
    emails = []
    full_name = []
    image_txt = []
    image_people_liked = []
    likes = []
    people = []
    
    for poster_id in ids:
        with conn:
            c.execute("""SELECT email,first,last FROM accounts
                        WHERE id = (:id)""",{
                        "id":poster_id,
                        })
        result = c.fetchone()
        
        emails.append(result[0]) 
        full_name.append(result[1]+" "+result[2])
    for i in range(2):
        os.chdir("..")
    for image in ls:
        image_txt.append(image.replace(".jpg",".txt")) 
        image_people_liked.append(image.replace(".jpg","_people_liked.txt"))
    
    for images,email in zip(image_txt,emails):
        with open(f"account_user{email}/{images}","r") as f:
            likes.append(f.read())
    
    for people_liked,email in zip(image_people_liked,emails):
        with open(f"account_user{email}/{people_liked}","r") as f:
            people__ = [lines.strip() for lines in f.readlines()]
            people.append(people__)
    
    return (full_name,likes,ids,people,emails)

def get_feed_thumbnails(ids):

    conn = sqlite3.connect("copro.db")
    c = conn.cursor()
    thumbnails = []
    for poster_id in ids:
        with conn:
            c.execute("""SELECT feed_thumbnail FROM accounts
                        WHERE id = (:id)""",{
                                           "id":poster_id,
                        })
        thumbnails.append(c.fetchone()[0]) 
    return thumbnails


port = 3500

print("creating socket")
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("socket created")

print("binding socket")
s.bind(('',port))
print("socket binded")

s.listen(4)
print("server started listening")

while True:
    c,add = s.accept()
    print("client connected")

    print("receiving user email")
    email = c.recv(4096).decode('utf-8')
    print("email received")

    image_names = get_image_names(email)

    print("sending image names")
    c.sendall(pickle.dumps(image_names))
    if c.recv(4096).decode("utf-8") == "received":

        print("received by client")
        os.chdir(f'account_user{email}/feed_user{email}')

        images = [PilImage.open(image) for image in image_names]

        with open('images.pickle','wb') as f:
            pickle.dump(images,f)

        print("sending images")
        with open("images.pickle",'rb') as f:
            data = f.read(4096)
            while data:
                c.send(data)
                data = f.read(4096)
            c.send("no more data".encode())
        print(c.recv(4096).decode("utf-8"))

        os.remove('images.pickle')
        os.chdir('..')
        os.chdir('..')
        
        details = get_user_details(email,image_names)
        print("sending details")
        c.sendall(pickle.dumps(details))
        print("sent")
        print(c.recv(4096).decode("utf-8"))
    
        thumbnails = get_feed_thumbnails(details[2])
        print("sending thumbnails")
        thumbnail_image = [PilImage.open(thumbnail) for thumbnail in thumbnails]

        with open('thumbnail_image.pickle','wb') as f:
            pickle.dump(thumbnail_image,f)

        with open('thumbnail_image.pickle','rb') as f:
            data = f.read(4096)
            while data:
                c.sendall(data)
                data = f.read(4096)
        print("all thumbnails sent")
        os.remove("thumbnail_image.pickle")

    c.close()
    
s.close()






