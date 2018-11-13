import socket
import pickle
import sqlite3
from PIL import Image as PilImage
import os



def fetch_req(user_email):
    conn_freind = sqlite3.connect('copro.db')
    cursor_friend = conn_freind.cursor()

    with conn_freind:
        cursor_friend.execute("""SELECT friend_req FROM accounts
                        WHERE email = (:email)""",{
                        "email" : user_email
                        })
        req_list = cursor_friend.fetchone()[0]
        req_list = req_list.split(repr(" "))
        return req_list 

def reject(user_id,new_req_list,requester_id):
    conn_freind = sqlite3.connect('copro.db')
    cursor_friend = conn_freind.cursor()

    with conn_freind:
        cursor_friend.execute("""UPDATE accounts
                    SET friend_req = (:new_list)
                    WHERE id=(:id)""",{
                    "new_list":new_req_list,
                    "id":user_id
                    })

        cursor_friend.execute("""SELECT sent FROM accounts
                    WHERE id=(:id)""",{
                    "id":requester_id
                    })
        sent = cursor_friend.fetchone()[0]
        sent = sent.split(" ")
        sent.remove(str(user_id))
        sent = (" ").join(sent)
        print(sent)
        cursor_friend.execute("""UPDATE accounts 
                    SET sent = (:new_sent)
                    WHERE id = (:id)""",{
                    "id":requester_id,
                    "new_sent":sent
                    })

def accept(requester_id,new_req_list,user_id):
    conn_freind = sqlite3.connect('copro.db')
    cursor_friend = conn_freind.cursor()

    new_req_list = (repr(" ")).join(new_req_list)
    with conn_freind:
        cursor_friend.execute("""SELECT friend_list FROM accounts
                    WHERE id=(:id)""",{
                    "id":user_id
                    })
        friend_list = cursor_friend.fetchone()[0]
        friend_list = friend_list +" "+str(requester_id)
        
        cursor_friend.execute("""UPDATE accounts 
                    SET friend_req = (:new_req_list),
                    friend_list = (:new_friend_list)
                    WHERE id = (:id)""",{
                    "new_req_list":new_req_list,
                    "new_friend_list":friend_list,
                    "id":user_id
                    })
        
        cursor_friend.execute("""SELECT friend_list,sent FROM accounts
                    WHERE id=(:id)""",{
                    "id":requester_id
                    })
        friend_list,sent = cursor_friend.fetchone()
        friend_list = friend_list +" "+str(user_id)
        sent = sent.split(" ")
        sent.remove(str(user_id))
        sent = (" ").join(sent)
        cursor_friend.execute("""UPDATE accounts 
                    SET friend_list = (:new_friend_list),
                        sent = (:new_sent)
                    WHERE id = (:id)""",{
                    "new_req_list":new_req_list,
                    "new_friend_list":friend_list,
                    "id":requester_id,
                    "new_sent":sent
                    })

def main():

    port = 5500

    print('creating socket friend')
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print('socket friend created')

    print("binding socket friend")
    s.bind(('',port))
    print('socket friend binded')

    s.listen(4)
    print('socket started listening')

    while True:
        c,add = s.accept()  
        print('connected to client')

        flag = c.recv(4096).decode('utf-8')
        
        if flag == "fetch":
            c.send(b'flag received by server')
            print('received')

            print('receiving user email')
            user_email = c.recv(4096).decode('utf-8')
            c.send('email received by server'.encode())
            print('received')

            req_list = fetch_req(user_email)


            thumbnails = [PilImage.open(requests.split(' ')[3]) for requests in req_list if requests!='']
            with open('images_friend.pickle','wb') as f:
                pickle.dump(thumbnails,f)

            print('sending thumbnails')
            with open('images_friend.pickle','rb') as f:
                data = f.read(4096)
                while data:
                    c.sendall(data)
                    data = f.read(4096)
                c.sendall(b'no more data')
            print(c.recv(4096).decode('utf-8'))

            os.remove('images_friend.pickle')
            print("sending req details")
            c.sendall(pickle.dumps(req_list))
            print('sent')

        elif flag == 'reject':
            c.send(b'flag received by server')
            print('received')

            print('receiving details')
            user_id,new_req_list,requester_id = pickle.loads(c.recv(4096))
            print(requester_id)
            reject(user_id,new_req_list,requester_id)

        elif flag == 'accept':
            c.send(b'flag received by server')
            print('received')

            print('receiving details')
            requester_id,new_req_list,user_id = pickle.loads(c.recv(4096))

            accept(requester_id,new_req_list,user_id)


        c.close()
    s.close()

if __name__ == '__main__':
    main()