import os
import time
import socket
import pickle
import shutil
import datetime
from PIL import Image as PilImage

ip = '127.0.0.1'

def create(first,last,email,password):
    port = 2000
    global ip
    
    print("creating socket")
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print('socket created')
    
    print("making connection")
    s.connect((ip,port))
    print("connection sucessful")
    

    print("sending details to server")
    account_details=[first,last,email,password]
    account_details = pickle.dumps(account_details)
    s.sendall(account_details)
    print("details sent")

    print("receiving return status")
    return_status = pickle.loads(s.recv(4096))
    print("received")
    
    s.close()
    return return_status

def login(email,password):
    port = 2500
    global ip
    
    print("creating socket")
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        print("socket created")
        
        print("conencting to server")
        s.connect((ip,port))
        print("connection scuessful")


        print("sending details to server")
        login_details = [email,password]
        login_details = pickle.dumps(login_details)
        s.sendall(login_details)
        print("sent")

        print("receiving user data")
        with open("data_login.pickle",'wb') as f:
                data = s.recv(4096000)
                while data:
                    f.write(data)
                    data = s.recv(4096000)
        with open("data_login.pickle",'rb') as f:
            user_data = pickle.load(f)
        print("received")

        try:
            os.remove('data_login.pickle')
        except Exception as e:
            print(e)

    return user_data
        
def account_settings(flag,new_detail,user_detail):
    port = 3000
    global ip

    print("creating socket")
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print("socket created")

    print("connecting socket")
    s.connect((ip,port))
    print("connection sucessful")

    print("sending flag")
    s.sendall("settings".encode())
    print(s.recv(4096).decode('utf-8'))


    print("sending details")
    details = [flag,new_detail,user_detail]
    details = pickle.dumps(details)
    s.sendall(details)
    print("sent")

    print("receiving return_data")
    return_data = pickle.loads(s.recv(4096))
    print("received")

    s.close()
    print("socket closed")
    return return_data

def change_propic(propic,user_id):
    port = 3000
    global ip
    
    try:
        propic_var = propic
        propic = PilImage.open(propic)
        if ".jpg" not in propic_var and ".jpeg" not in propic_var:
            return 0
    except:
        return None

    print("creating socket")
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print('socket created')

    print("connection socket")
    s.connect((ip,port))
    print("connected")

    print('sending flag')
    s.sendall('propic'.encode())
    print(s.recv(4096).decode('utf-8'))

    
    print('sending details')
    details = [propic,user_id]
    with open("image.pickle",'wb') as f:
            pickle.dump(details,f)
    with open("image.pickle",'rb') as f:
        data = f.read(4096)
        while data:
            s.send(data)
            data = f.read(4096)
        s.send(b'no more data')
    os.remove('image.pickle')
    print("sent")

    
    print("receiving new propic")
    with open("image.pickle",'wb') as f:
        data = s.recv(4096)
        while True:
            if data.endswith(b'no more data'):
                data = data.split(b'no more data')[0]
                f.write(data)
                break
            f.write(data)
            data = s.recv(4096)
    with open("image.pickle",'rb') as f:
        propic_bytes = pickle.load(f)
    os.remove('image.pickle')
    print("received")


    s.close()
    return propic_bytes

def fetch_feed(user_id):
    port = 3500
    global ip

    print("creating feed socket")
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print("socket created")

    print("connection socket")
    s.connect((ip,port))
    print("connection sucessful")


    print("sending user_id to server")
    s.sendall(str(user_id).encode())
    print("sent")

    print("receiving feed")
    with open("feed.pickle","wb") as f:
        data = s.recv(4096)
        while True:
            if data.endswith(b'no more data'):
                data = data.split(b'no more data')[0]
                f.write(data)
                break
            f.write(data)
            data = s.recv(4096)
    with open("feed.pickle",'rb') as f:
        details = pickle.load(f)
    os.remove('feed.pickle')
    print("received")

    s.close()
    return details

def upload_feed(image,user_id):
    try:
        image_var = image
        image = PilImage.open(image)
        if ".jpg" not in image_var and ".jpeg" not in image_var:
            return 0
    except:
        return None

    port = 4000
    global ip

    print("creating socket")
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print("socket created")

    print("connecting")
    s.connect((ip,port))
    print("connected to server")

    print("sending user id")
    s.sendall(str(user_id).encode())
    print("sent")
    print(s.recv(4096).decode('utf-8'))

    
    print('sending image')
    with open('image.pickle','wb') as f:
        pickle.dump(image,f)
    with open('image.pickle','rb') as f:
        data = f.read(4096)
        while data:
            s.sendall(data)
            data=f.read(4096)
        s.sendall(b'no more data')
    os.remove('image.pickle')
    print("sent")
    

    s.close()
    time.sleep(.5)
    return

def like_unlike(image,p_id,user_id,flag):

    port = 4500
    global ip

    print("creating socket")
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print("socket created")
    
    print("connecting socket")
    s.connect((ip,port))
    print('connected to server')

    print('sending required details')
    details = [image,p_id,user_id,flag]
    s.sendall(pickle.dumps(details))
    print("sent")
    print(s.recv(4096).decode('utf-8'))

    s.close()

def search(searched_person,user_id):

    port = 5000
    global ip

    print("creating socket")
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print("socket created")

    print("connecting socket")
    s.connect((ip,port))
    print("connected")

    print('sending flag')
    s.sendall('search'.encode())
    print("sent")
    print(s.recv(4096))

    print('sending details')
    details = [searched_person,user_id]
    s.sendall(pickle.dumps(details))
    print("sent")

    
    print('receiving details')
    with open('details.pickle','wb') as f:
        data = s.recv(4096)
        while True:
            if data.endswith(b'no more data'):
                data = data.split(b'no more data')[0]
                f.write(data)
                break
            f.write(data)
            data = s.recv(4096)
    with open('details.pickle','rb') as f:
        search_result,friend_list,sent = pickle.load(f)
    os.remove('details.pickle')
    print("details received")


    s.close() 
    return (search_result,friend_list,sent)


def send_frnd_req(sender_id,receiver_id):

    port = 5000
    global ip
    
    print("creating socket")
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print("socket created")

    print("connecting socket")
    s.connect((ip,port))
    print("connected")

    print('sending flag')
    s.sendall('send req'.encode())
    print("sent")
    print(s.recv(4096).decode('utf-8'))

    print('sending details')
    s.send(pickle.dumps([sender_id,receiver_id]))
    print("sent")
    print(s.recv(4096))

    s.close()

def fetch_req(user_id):
    
    port = 5500
    global ip

    print('creating socket')
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print('socket created')

    print("conencting")
    s.connect((ip,port))
    print("connected to server")

    print('sending flag')
    s.send('fetch'.encode())
    print(s.recv(4096).decode('utf-8'))
    print('sent')

    print('sending user id')
    s.send(str(user_id).encode())
    print(s.recv(4096).decode('utf-8'))
    print("sent")

    print('receiving requests')
    with open('request.pickle','wb') as f:
        data = s.recv(4096)
        while True:
            if data.endswith(b'no more data'):
                data = data.split(b'no more data')[0]
                f.write(data)
                break
            f.write(data)
            data = s.recv(4096)
    with open('request.pickle','rb') as f:
        req_list,thumbnails = pickle.load(f)
    os.remove('request.pickle')
    print('received')

    
    req_list.remove('')
    new_req_list = []
    for req in req_list:
        req = req.split(' ')
        new_req_list.append((' ').join(req))

    return [new_req_list,thumbnails]

def reject_request(user_id,new_req_list,requester_id):
    port = 5500
    global ip
    
    print('creating socket')
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print('socket created')

    print("connecting to server")
    s.connect((ip,port))
    print("connected to server")

    print("sending flag")
    s.send('reject'.encode())
    print("sent")
    print(s.recv(4096).decode('utf-8'))
    
    print('sending details')
    s.send(pickle.dumps([user_id,new_req_list,requester_id]))
    print('sent')

def accept_req(requester_id,new_req_list,user_id):
    port = 5500
    global ip
    
    print('creating socket')
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print('socket created')

    print("connection to server")
    s.connect((ip,port))
    print("connected to server")

    print("sending flag")
    s.send('accept'.encode())
    print("sent")
    print(s.recv(4096).decode('utf-8'))

    print('sending details')
    s.send(pickle.dumps([requester_id,new_req_list,user_id]))
    print('sent')

def fetch_scout_view(user_id,person_id):
    global ip
    port = 6000

    print('creating socket')
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print('socket created')

    print("connecting")
    s.connect((ip,port))
    print('connnected to server')

    print('sending details to server')
    s.sendall(pickle.dumps(person_id))
    print("sent")

    
    print('receiving details')
    with open('details.pickle','wb') as f:
        while True:
            data = s.recv(4096)
            if data.endswith(b'no more data'):
                data = data.split(b'no more data')[0]
                f.write(data)
                break
            f.write(data)
    with open('details.pickle','rb') as f:
        details = pickle.load(f)
    os.remove('details.pickle')
    print('received')

    return details
