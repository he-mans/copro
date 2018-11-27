import socket
import pickle
import os
from PIL import Image as PilImage
import shutil
import time
import datetime

ip = '127.0.0.1'

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
        if not os.path.exists(f"account_user{user_id}"):
            print("creating temp folders")
            os.makedirs(f"account_user{user_id}/feed_user{user_id}")
            os.chdir(f"account_user{user_id}")
            os.mkdir(f"profile_pic_user{user_id}")
            os.mkdir(f"thumbnail_user{user_id}")
            os.mkdir(f"thumbnail_people_feed")
            os.mkdir(f"thumbnail_people_search")
            os.mkdir(f"thumbnail_people_friend_request")
            os.mkdir(f"scout")
            os.chdir("..")
            print('folders created')
        
        
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
            
        print("saving images")
        profile.save(f'account_user{user_id}/profile_pic_user{user_id}/propic.jpg')
        thumbnail.save(f'account_user{user_id}/thumbnail_user{user_id}/thumbnail.jpg')
        print('image saved')
            
    else:
        s.sendall("don't send".encode())
    
    try:
        os.remove('images.pickle')
    except Exception as e:
        print(e)
    finally:
        s.close()
        print("socket closed")
        return return_status

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
    propic.thumbnail((150,150))
    propic.save(f"account_user{user_id}/profile_pic_user{user_id}/propic.jpg")
    propic.thumbnail((60,60))
    propic.save(f"account_user{user_id}/thumbnail_user{user_id}/thumbnail.jpg")
    return 1
    
        

def fetch_feed(user_id):
    port = 3500
    global ip

    try:
        shutil.rmtree(f'account_user{user_id}/feed_user{user_id}')
        shutil.rmtree(f'account_user{user_id}/thumbnail_people_feed')
    except Exception as e:
        print(e)
    finally:
        os.makedirs(f'account_user{user_id}/feed_user{user_id}')
        os.makedirs(f'account_user{user_id}/thumbnail_people_feed')

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
    images = pickle.loads(s.recv(4096))
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

    os.chdir(f"account_user{user_id}/feed_user{user_id}")

    for image,image_name_ in zip(images_list,images):
        image.save(image_name_)
    print("images saved")
    
    
    os.chdir("..")
    
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

    thumbnail_counter = 0
    os.chdir("thumbnail_people_feed")
    
    for thumbnail in thumbnails:
        thumbnail.save(f"thumbnail_{thumbnail_counter}.jpg")
        print("image saved")
        thumbnail_counter+=1
    
    images_time = [datetime.datetime.strptime(image.replace('$',':').split('_')[0],'%Y-%m-%d %H:%M:%S.%f') for image in images]
    images = [f"account_user{user_id}/feed_user{user_id}/{image}" for image in images]
    thumbnails = [f"account_user{user_id}/thumbnail_people_feed/{thumbnail}" for thumbnail in os.listdir()]
    thumbnails = sorted(thumbnails)

    details = list(details)
    details.insert(0,thumbnails)
    details.insert(0,images)
    details.append(images_time)
    
    os.chdir("..")
    os.remove('thumbnail_image.pickle')
    os.chdir("..")
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
    
    try:
        shutil.rmtree(f'account_user{user_id}/thumbnail_people_search')
    except Exception as e:
        print(e)
    finally:
        os.makedirs(f'account_user{user_id}/thumbnail_people_search')

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

    os.chdir(f'account_user{user_id}/thumbnail_people_search')
    for i,thumbnail in enumerate(thumbnails):
        thumbnail.save(f'thumbnail_{i}.jpg')


    print('recieving details')
    details_search = pickle.loads(s.recv(4096))
    print('received')

    search_result,friend_list,sent = details_search
    search_result = [list(elements) for elements in search_result]
    thumbnails = os.listdir()
    thumbnails = sorted(thumbnails,key = lambda x: int(x.split('.')[0].split('_')[1]))
    for thumbnail,elements in zip(thumbnails,search_result):
        elements[3] = f'account_user{user_id}/thumbnail_people_search/{thumbnail}'

    search_result = tuple(search_result)
    os.chdir('..')
    os.chdir('..')
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
    
    try:
        shutil.rmtree(f'account_user{user_id}/thumbnail_people_friend_request')
    except Exception as e:
        print(e)
    finally:
        os.makedirs(f'account_user{user_id}/thumbnail_people_friend_request')

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
    for i,thumbnail in enumerate(thumbnails):
        thumbnail.save(f'account_user{user_id}/thumbnail_people_friend_request/thumbnail_{i}.jpg')

    thumbnails = [f'account_user{user_id}/thumbnail_people_friend_request/{thumbnail}' for thumbnail in os.listdir(f'account_user{user_id}/thumbnail_people_friend_request')]
    thumbnails = sorted(thumbnails,key = lambda x: int(x.split("/")[-1].split('.')[0].split('_')[1]))

    print("receiving req details")
    req_list = pickle.loads(s.recv(4096))
    print('received')

    req_list.remove('')
    new_req_list = []
    for req,thumbnail in zip(req_list,thumbnails):
        req = req.split(' ')
        req[3] = thumbnail
        new_req_list.append((' ').join(req))

    return new_req_list

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
    print(s.recv(4096).decode('utf-8'))

    print('receiving images names')
    names = pickle.loads(s.recv(4096))
    names = [name.split('.jpg')[0] for name in names]
    images_time = [datetime.datetime.strptime(name.replace('$',':').split('_')[0] , '%Y-%m-%d %H:%M:%S.%f') for name in names]
    s.sendall(b'names received by client')
    print('received')

    try:
        shutil.rmtree(f'account_user{user_id}/scout')
    except Exception as e:
        print(e)
    finally:
        os.makedirs(f'account_user{user_id}/scout')

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

    os.remove('images.pickle')

    for image,name in zip(images,names):
        image.save(f'account_user{user_id}/scout/{name}.jpg')

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

    pro_and_thu[0].save(f'account_user{user_id}/scout/propic.jpg')
    pro_and_thu[1].save(f'account_user{user_id}/scout/thumbnail.jpg')

    images = os.listdir(f'account_user{user_id}/scout')
    images.remove('propic.jpg')
    images.remove('thumbnail.jpg')
    images = sorted(images,key = lambda x:datetime.datetime.strptime(x.replace('$',':').split('_')[0],'%Y-%m-%d %H:%M:%S.%f'))
    images = [f'account_user{user_id}/scout/{image}' for image in images]
    propic = f'account_user{user_id}/scout/propic.jpg'
    thumbnail = f'account_user{user_id}/scout/thumbnail.jpg'
    
    return (images,likes,people_liked,propic,thumbnail,images_time)

def logout(user_id):
    shutil.rmtree(f'account_user{user_id}')