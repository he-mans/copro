import socket
import pickle
import os
from PIL import Image as PilImage
import shutil
import time
import datetime
from io import BytesIO

ip = '127.0.0.1'

def get_byte_array(images):
    images_byte_array_dict = {}
    images_byte_array = []
    for i,image in enumerate(images):
        images_byte_array_dict.update({f'array{i}':BytesIO()})
        image.save(images_byte_array_dict[f'array{i}'],"JPEG")
        images_byte_array.append(images_byte_array_dict[f'array{i}'].getvalue() )
    return images_byte_array

def create(first,last,email,password):
    port = 2000
    global ip
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print('socket made')
    
    print("making connection")
    
    s.connect((ip,port))
    print("connection sucessful")
    
    account_details=[first,last,email,password]
    account_details = pickle.dumps(account_details)

    print("sending details to server")
    s.sendall(account_details)
    print("details sent")

    print("receiving return status")
    return_status = pickle.loads(s.recv(4096))
    print("received")
    
    print("closing socket")
    s.close()
    print("scoket closed")
    return return_status

def login(email,password):
    port = 2500
    global ip
    
    print("creating socket")
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print("socket created")
    
    print("conencting to server")
    s.connect((ip,port))
    print("connection scuessful")

    login_details = [email,password]
    login_details = pickle.dumps(login_details)

    print("sending details to server")
    s.sendall(login_details)
    print("sent")

    print("receiving reutrn status")
    return_status = pickle.loads(s.recv(4096))
    print("received")
    if return_status!=1 and return_status!=0:
        user_id = return_status["id"]
    
        print("sending request to send profile pic and thumbnail")
        s.sendall("send".encode())

        print("receiving images file")
        with open("images.pickle",'wb') as f:
            data = s.recv(4096000)
            while data:
                f.write(data)
                data = s.recv(4096000)
            
        with open("images.pickle",'rb') as f:
            profile,thumbnail = pickle.load(f)
            
        propic = BytesIO()
        profile.save(propic,"JPEG")
        propic = propic.getvalue()
            
    else:
        s.sendall("don't send".encode())
    
    try:
        os.remove('images.pickle')
    except Exception as e:
        print(e)
    finally:
        s.close()
        print("socket closed")
        return [return_status,propic]

def account_settings(flag,new_detail,user_detail):
    port = 3000
    global ip

    print("creating socket")
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print("socket created")

    print("connection socket")
    s.connect((ip,port))
    print("connection sucessful")

    print("sending flag")
    s.sendall("settings".encode())
    print(s.recv(4096).decode('utf-8'))

    details = [flag,new_detail,user_detail]
    details = pickle.dumps(details)

    print("sending details")
    s.sendall(details)
    print("sent")

    print("receiving return_data")
    return_data = pickle.loads(s.recv(4096))
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


    details = [propic,user_id]
    print('sending details')
    with open("image.pickle",'wb') as f:
            pickle.dump(details,f)

    with open("image.pickle",'rb') as f:
        data = f.read(4096)
        while data:
            s.send(data)
            data = f.read(4096)
        s.send(b'no more data')
    
    print(s.recv(4096).decode('utf-8'))
    s.close()
    propic.thumbnail((150,150))
    propic_byte_array = BytesIO()
    propic.save(propic_byte_array,"JPEG")
    propic_byte_array = propic_byte_array.getvalue()
    return propic_byte_array

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

    print("receiving feed image names")
    images_name = pickle.loads(s.recv(4096))
    s.sendall("received".encode())

    print("requesting images")
    with open('images.pickle','wb') as f:
        data = s.recv(4096)
        while data:
            if data.endswith(b'no more data'):
                data = data.split(b'no more data')[0]
                f.write(data)
                break
            f.write(data)
            data = s.recv(4096)
        print("no more data")
    s.send("images received by client".encode())
    print('received')

    with open('images.pickle','rb') as f:
        images_list = pickle.load(f)
    
    images_byte_array = get_byte_array(images_list)
    
    print("requesting user details")
    details = pickle.loads(s.recv(4096))
    print("details received")
    s.send("user_detail received by client".encode())

    print("receiving thumbnails")
    with open("thumbnail_image.pickle",'wb') as f:
        data = s.recv(4096)
        while data:
            f.write(data)
            data = s.recv(4096)

    with open("thumbnail_image.pickle",'rb') as f:
        thumbnails = pickle.load(f)
    print("thumbnail received")

    thumbnails_byte_array = get_byte_array(thumbnails)
    
    images_time = [datetime.datetime.strptime(image.replace('$',':').split('_')[0],'%Y-%m-%d %H:%M:%S.%f') for image in images_name]

    details = list(details)
    details.insert(0,thumbnails_byte_array)
    details.insert(0,images_name)
    details.append(images_time)
    details.append(images_byte_array)
    os.remove('thumbnail_image.pickle')
    os.remove('images.pickle')
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

    s.connect((ip,port))
    print("connected to server")

    print("sending user id")
    s.sendall(str(user_id).encode())
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
    s.close()
    time.sleep(.5)
    return

def like_unlike(image,p_id,user_id,flag):

    port = 4500
    global ip

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print("socket made")
    
    s.connect((ip,port))
    print('connected to server')

    details = [image,p_id,user_id,flag]

    print('sending required details')
    s.sendall(pickle.dumps(details))
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
    print(s.recv(4096).decode('utf-8'))

    print('sending details')
    details = [searched_person,user_id]
    s.sendall(pickle.dumps(details))
    print(s.recv(4096).decode('utf-8'))

    print('receiving thumbnails')
    with open('images.pickle','wb') as f:
        data = s.recv(4096)
        while True:
            if data.endswith(b'no more data'):
                data = data.split(b'no more data')[0]
                f.write(data)
                break
            f.write(data)
            data = s.recv(4096)
        s.sendall('thumbnails received by client'.encode())
        print('thumbnails received')

    with open('images.pickle','rb') as f:
        thumbnails = pickle.load(f)

    os.remove('images.pickle')

    thumbnails_byte_array = {}
    for i,thumbnail in enumerate(thumbnails):
        thumbnails_byte_array.update({'array'+str(i):BytesIO()})
        thumbnail.save(thumbnails_byte_array[f'array{i}'],"JPEG")
        thumbnails_byte_array['array'+str(i)] = thumbnails_byte_array[f'array{i}'].getvalue()

    print('recieving details')
    details_search = pickle.loads(s.recv(4096))
    print('received')

    search_result,friend_list,sent = details_search
    search_result = [list(elements) for elements in search_result]

    for thumbnail,elements in zip(thumbnails_byte_array,search_result):
       elements[3] = thumbnails_byte_array[thumbnail]

    search_result = tuple(search_result)
    return (search_result,friend_list,sent)

    s.close() 

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
    print(s.recv(4096).decode('utf-8'))

    print('sending details')
    s.send(pickle.dumps([sender_id,receiver_id]))
    print(s.recv(4096))

    s.close()

def fetch_req(user_id):
    
    port = 5500
    global ip

    print('creating socket')
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print('socket created')

    s.connect((ip,port))
    print("connected to server")

    s.send('fetch'.encode())
    print(s.recv(4096).decode('utf-8'))

    print('sending email')
    s.send(str(user_id).encode())
    print(s.recv(4096).decode('utf-8'))

    print('receiving thumbnails')
    with open('images.pickle','wb') as f:
        data = s.recv(4096)
        while True:
            if data.endswith(b'no more data'):
                data = data.split(b'no more data')[0]
                f.write(data)
                break
            f.write(data)
            data = s.recv(4096)

    s.sendall('received by client'.encode())

    with open('images.pickle','rb') as f:
        thumbnails = pickle.load(f)

    os.remove('images.pickle')
    
    thumbnails = get_byte_array(thumbnails)
    
    print("receiving req details")
    req_list = pickle.loads(s.recv(4096))
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

    s.connect((ip,port))
    print("connected to server")

    s.send('reject'.encode())
    print(s.recv(4096).decode('utf-8'))
    
    print('sending details')
    print(requester_id)
    s.send(pickle.dumps([user_id,new_req_list,requester_id]))
    print('sent')

def accept_req(requester_id,new_req_list,user_id):
    port = 5500
    global ip
    print('creating socket')
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print('socket created')

    s.connect((ip,port))
    print("connected to server")

    s.send('accept'.encode())
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

    s.connect((ip,port))
    print('connnected to server')

    print('sending details to server')
    s.sendall(pickle.dumps(person_id))
    print(s.recv(4096))

    print('receiving images names')
    names = pickle.loads(s.recv(4096))
    images_time = [datetime.datetime.strptime(name.split('.jpg')[0].replace('$',':').split('_')[0] , '%Y-%m-%d %H:%M:%S.%f') for name in names]
    s.sendall(b'names received by client')
    print('received')

    print('receiving images')
    with open('images.pickle','wb') as f:
        while True:
            data = s.recv(4096)
            if data.endswith(b'no more data'):
                data = data.split(b'no more data')[0]
                f.write(data)
                break
            f.write(data)
    s.sendall(b'images received by client')
    print('received')

    with open('images.pickle','rb') as f:
        images = pickle.load(f)

    images = get_byte_array(images)
    os.remove('images.pickle')

    print('recieving likes and people liked')
    likes,people_liked = pickle.loads(s.recv(4096))
    s.sendall(b'received by client')
    print('received')

    print('receiving profile and thumbnail')
    with open('images.pickle','wb') as f:
        while True:
            data = s.recv(4096)
            if data.endswith(b'no more data'):
                data = data.split(b'no more data')[0]
                f.write(data)
                break
            f.write(data)
    s.sendall(b'received by client')
    print('received')

    with open('images.pickle','rb') as f:
        pro_and_thu = pickle.load(f)

    os.remove('images.pickle')

    propic,thumbnail = get_byte_array(pro_and_thu)
    
    return (names,likes,people_liked,propic,thumbnail,images_time,images)