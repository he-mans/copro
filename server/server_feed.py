import socket
import os
import pickle
from PIL import Image as PilImage 
import sqlite3
import datetime
import traceback

def get_image_names(user_id):
    os.chdir(f"account_user{user_id}/feed_user{user_id}")
    ls = os.listdir()
    ls = [image for image in ls if image.endswith(".txt") is False]
    ls = sorted(ls,key = lambda x: datetime.datetime.strptime(x.replace('$',':').split('_')[0],'%Y-%m-%d %H:%M:%S.%f'))    
    os.chdir('..')
    os.chdir('..')
    return ls

    
def get_user_details(user_id,ls):
    
    conn_feed = sqlite3.connect("copro.db")
    cursor_feed = conn_feed.cursor()
    os.chdir(f"account_user{user_id}/feed_user{user_id}")

    ids = [image.split("-")[-1].split(".jpg")[0] for image in ls]
    #emails = []
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
    for i in range(2):
        os.chdir("..")
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

            image_names = get_image_names(user_id)

            print("sending image names")
            c.sendall(pickle.dumps(image_names))
            
            if c.recv(4096).decode("utf-8") == "received":

                print("received by client")
                os.chdir(f'account_user{user_id}/feed_user{user_id}')

                images = [PilImage.open(image) for image in image_names]

                with open(f'images_feed_user{add}.pickle','wb') as f:
                    pickle.dump(images,f)

                print("sending images")
                with open(f"images_feed_user{add}.pickle",'rb') as f:
                    data = f.read(4096)
                    while data:
                        c.send(data)
                        data = f.read(4096)
                    c.send("no more data".encode())
                print(c.recv(4096).decode("utf-8"))

                os.remove(f'images_feed_user{add}.pickle')
                os.chdir('..')
                os.chdir('..')
                
                details = get_user_details(user_id,image_names)
                print("sending details")
                c.sendall(pickle.dumps(details))
                print("sent")
                print(c.recv(4096).decode("utf-8"))
            
                thumbnails = get_feed_thumbnails(details[2])
                print("sending thumbnails")
                thumbnail_image = [PilImage.open(thumbnail) for thumbnail in thumbnails]

                with open(f'thumbnail_image_feed_user{add}.pickle','wb') as f:
                    pickle.dump(thumbnail_image,f)

                with open(f'thumbnail_image_feed_user{add}.pickle','rb') as f:
                    data = f.read(4096)
                    while data:
                        c.sendall(data)
                        data = f.read(4096)
                print("all thumbnails sent")
                os.remove(f"thumbnail_image_feed_user{add}.pickle")

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