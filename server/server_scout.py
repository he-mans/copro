import os
import socket
import pickle
import sqlite3
import datetime
import traceback
import convert_to_bytes
from PIL import Image as PilImage


def get_images_name(user_id):
    os.chdir(f"account_user{user_id}")
    images_name = [image for image in os.listdir() if image.endswith(".txt") is False and os.path.isdir(image) is False]
    images_name = sorted(images_name,key = lambda x:datetime.datetime.strptime(x.split('_')[0].replace('$',':'),'%Y-%m-%d %H:%M:%S.%f'))
    os.chdir('..')
    return images_name

def get_image_time(images_name):
    images_time = [datetime.datetime.strptime(name.split('_')[0].replace('$',':') , '%Y-%m-%d %H:%M:%S.%f') for name in images_name]
    return images_time

def get_images(images_name,user_id):
    os.chdir(f"account_user{user_id}")
    images = [convert_to_bytes.convert_image(PilImage.open(image_name)) for image_name in images_name]
    os.chdir("..")
    return images

def get_details(images_name,user_id):
    os.chdir(f"account_user{user_id}")
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
    os.chdir("..")
    return (people_liked,likes)

def get_propic_and_thumbnail(person_id):
    conn_scout = sqlite3.connect('copro.db')
    cursor_scout = conn_scout.cursor()

    with conn_scout:
        cursor_scout.execute("""SELECT propic,feed_thumbnail FROM accounts
                    WHERE id = (:person_id)""",{
                    "person_id":person_id
                    })
        propic,thumbnail = cursor_scout.fetchone()
        propic,thumbnail = PilImage.open(propic),PilImage.open(thumbnail)
    
    return convert_to_bytes.convert_image([propic,thumbnail])


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
        try:
            c,add = s.accept()
            print('client accepted')

            print('receiving details')
            person_id = pickle.loads(c.recv(4096))
            print('received')
            
            
            print("processing request")
            images_name = get_images_name(person_id)
            images = get_images(images_name,person_id)
            images_time = get_image_time(images_name)
            people_liked,likes = get_details(images_name,person_id)
            propic,thumbnail = get_propic_and_thumbnail(person_id)
            details = (images_name,likes,people_liked,propic,thumbnail,images_time,images)
            print("done")
            

            print("sending details")
            with open(f'details_scout_user{add}.pickle','wb') as f:
                pickle.dump(details,f)
            with open(f'details_scout_user{add}.pickle','rb') as f:
                data = f.read(4096)
                while data:
                    c.sendall(data)
                    data = f.read(4096)
                c.sendall(b'no more data')
            os.remove(f'details_scout_user{add}.pickle')
            print("sent")


        except Exception as e:
            print('server_scout raised exception :',end = ' ')
            print(e)
            print('traceback for above scout error')
            traceback.print_exc()
            break
        c.close()
    s.close()

if __name__ == '__main__':
    main()