import os
import socket
import pickle
import sqlite3
import datetime
import traceback
import convert_to_bytes
from PIL import Image as PilImage 


def get_image_names(user_id):
    os.chdir(f"account_user{user_id}/feed_user{user_id}")
    ls = os.listdir()
    ls = [image for image in ls if image.endswith(".txt") is False]
    ls = sorted(ls,key = lambda x: datetime.datetime.strptime(x.replace('$',':').split('_')[0],'%Y-%m-%d %H:%M:%S.%f'))    
    ls = [f'account_user{user_id}/feed_user{user_id}/{image}' for image in ls]
    os.chdir('../..')
    return ls

def get_image_time(images_name):
    images_time = [image.split('/')[-1] for image in images_name]
    images_time = [datetime.datetime.strptime(image.replace('$',':').split('_')[0],'%Y-%m-%d %H:%M:%S.%f') for image in images_time]
    return images_time

def get_user_details(user_id,ls):
    
    ls = [image.split('/')[-1] for image in ls]
    conn_feed = sqlite3.connect("copro.db")
    cursor_feed = conn_feed.cursor()
    ids = [image.split("-")[-1].split(".jpg")[0] for image in ls]
    full_name = []
    image_txt = []
    image_people_liked = []
    likes = []
    people = []
    
    for poster_id in ids:
        with conn_feed:
            cursor_feed.execute("""SELECT first,last FROM accounts
                                    WHERE id = (:id)""",{
                                    "id":poster_id,
                                })
        result = cursor_feed.fetchone()
        full_name.append(result[0]+" "+result[1])
    
    
    for image in ls:
        image_txt.append(image.replace(".jpg",".txt")) 
        image_people_liked.append(image.replace(".jpg","_people_liked.txt"))
    
    for images,poster_id in zip(image_txt,ids):
        with open(f"account_user{poster_id}/{images}","r") as f:
            likes.append(f.read())
    
    for people_liked,poster_id in zip(image_people_liked,ids):
        with open(f"account_user{poster_id}/{people_liked}","r") as f:
            people__ = [lines.strip() for lines in f.readlines()]
            people.append(people__)
    
    return (full_name,likes,ids,people)

def get_feed_thumbnails(ids):

    conn_feed = sqlite3.connect("copro.db")
    cursor_feed = conn_feed.cursor()
    thumbnails = []
    for poster_id in ids:
        with conn_feed:
            cursor_feed.execute("""SELECT feed_thumbnail FROM accounts
                        WHERE id = (:id)""",{
                        "id":poster_id,
                        })
        thumbnails.append(cursor_feed.fetchone()[0]) 
    return thumbnails


def main():
    port = 3500

    print("creating socket feed")
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print("socket created feed")

    print("binding socket feed")
    s.bind(('',port))
    print("socket binded feed")

    s.listen(4)
    print("server started listening feed")

    while True:
        try:
            c,add = s.accept()
            print("client connected")

            print("receiving user id")
            user_id = c.recv(4096).decode('utf-8')
            print("id received")

            print("processing request")
            image_names = get_image_names(user_id)
            images_time = get_image_time(image_names)
            images = [convert_to_bytes.convert_image(PilImage.open(image)) for image in image_names]
            details = list(get_user_details(user_id,image_names))
            thumbnails = get_feed_thumbnails(details[2])
            thumbnails = [convert_to_bytes.convert_image(PilImage.open(thumbnail)) for thumbnail in thumbnails]
            details.insert(0,thumbnails)
            details.insert(0,image_names)
            details.append(images_time)
            details.append(images)
            print("done processing")

        
            print("sending details")
            with open(f'feed_user{add}.pickle','wb') as f:
                pickle.dump(details,f)
            with open(f"feed_user{add}.pickle",'rb') as f:
                data = f.read(4096)
                while data:
                    c.send(data)
                    data = f.read(4096)
                c.send("no more data".encode())
            os.remove(f'feed_user{add}.pickle')
            print("sent")

        
        except Exception as e:
            print('server_feed raised exception :',end = ' ')
            print(e)
            print('traceback for above feed error')
            traceback.print_exc()
            break
        c.close()
    
    s.close()

if __name__ == '__main__':
    main()