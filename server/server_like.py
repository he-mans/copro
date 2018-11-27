import socket
import os
import pickle
import traceback
def add_like(image,p_id,user_id):
    image_txt = image.replace(".jpg",".txt")
    
    with open(f"account_user{p_id}/{image_txt}","r") as f:
        likes = int(f.read())
    with open(f"account_user{p_id}/{image_txt}","w") as f:
        f.write(str(likes+1))
    image_txt = image.replace(".jpg","_people_liked.txt")
    with open(f"account_user{p_id}/{image_txt}","a") as f:
        f.write(f"{user_id}\n")
    return likes+1

def remove_like(image,p_id,user_id):
    image_txt = image.replace(".jpg",".txt")
    with open(f"account_user{p_id}/{image_txt}","r") as f:
        likes = int(f.read())
    with open(f"account_user{p_id}/{image_txt}","w") as f:
        f.write(str(likes-1))
    image_txt = image.replace(".jpg","_people_liked.txt")
    with open(f"account_user{p_id}/{image_txt}","r") as f:
        liked_people = [ids.strip() for ids in f.readlines()]
    liked_people.remove(str(user_id))
    with open(f"account_user{p_id}/{image_txt}","w") as f:
        f.truncate(0)
        for people in liked_people:
            f.write(people+"\n")


def main():
    port = 4500

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("socket made")

    print("binding socket")
    s.bind(('',port))
    print('socket binded')

    s.listen(4)
    print('socket started to listen')

    while True:
        try:
            c,add = s.accept()
            print('connected to client')

            print("receiving details")
            details = pickle.loads(c.recv(4096))
            c.sendall('received by server'.encode())

            if details[-1] == "like":
                add_like(details[0],details[1],details[2])

            elif details[-1] == "unlike":
                remove_like(details[0],details[1],details[2])
        
        except Exception as e:
            print('server_like raised exception :',end = ' ')
            print(e)
            print('traceback for above like error')
            traceback.print_exc()
            break
        c.close()

    s.close()

if __name__ == '__main__':
    main()