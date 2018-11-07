import pickle
import socket
import os
import sqlite3
from PIL import Image as PilImage

conn = sqlite3.connect("copro.db")
cursor = conn.cursor()
def search(detail,user_email):
    global conn,cursor

    detail = detail.strip()
    with conn:
        try:
            first,last = detail.split(" ")
            first,last = first.strip(),last.strip()
            cursor.execute("""SELECT first,last,
                         id,thumbnail,email FROM accounts
                         WHERE first = (:first) AND
                         last = (:last)""",{
                         "first":first,
                         "last":last
                             })
        except:
            first = detail
            cursor.execute("""SELECT first,last,
                             id,thumbnail,email FROM accounts
                             WHERE first = (:first) OR  
                             last = (:first)""",{
                             "first":first
                             })
        search_result = cursor.fetchall()

        cursor.execute("""SELECT friend_list,sent FROM accounts
                        WHERE email=(:email)""",{
                        "email":user_email
                        })
        friend_list,sent = cursor.fetchone()
        friend_list = friend_list.split(" ")
        sent = sent.split(" ")
        return (search_result,friend_list,sent)

def send_req(sender_email,requester_id):
    global conn,cursor

    with conn:
        cursor.execute("""SELECT first,last,id,thumbnail,email FROM accounts
                    WHERE email = (:email)""",{
                    "email": sender_email
                    })
        sender_detail = list(cursor.fetchone())
        sender_detail[2] = str(sender_detail[2])
        sender_detail = (" ").join(sender_detail)
        
        cursor.execute("""SELECT sent FROM accounts
                    WHERE email = (:email)""",{
                    "email":sender_email
                    })
        sent = cursor.fetchone()[0]
        sent+=f" {receiver_id}"
        cursor.execute("""SELECT friend_req FROM accounts
                    WHERE id = (:id)""",{
                     "id":receiver_id
                     })
        req_list = cursor.fetchone()[0]
        req_list = req_list+repr(" ")+sender_detail
        cursor.execute("""UPDATE accounts
                     SET friend_req = (:friend_req)
                     WHERE id = (:id)""",{
                     "friend_req":req_list,
                     "id":receiver_id
                     })
        cursor.execute("""UPDATE accounts
                    SET sent = (:sent)
                    WHERE email = (:email)""",{
                    "sent":sent,
                    "email":sender_email
                    })

port = 5000

print('creating socket')
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('socket created')

print('binding socket')
s.bind(('',port))
print('socket binded')

s.listen(4)
print("listening")

while True:

    c,add = s.accept()
    print("client connected")

    flag = c.recv(4096)
    if flag =='search'.encode():
        
        c.sendall("flag received by client".encode())
        print('flag recieved')

        print('receiving details')
        details= pickle.loads(c.recv(4096))
        c.sendall('details received by server'.encode())
        print('details received')

        detail,email = details

        search_result,friend_list,sent = search(detail,email)
        thumbnails = [result[3] for result in search_result]

        thumbnails = [PilImage.open(thumbnail) for thumbnail in thumbnails]

        with open('image.pickle','wb') as f:
            pickle.dump(thumbnails,f)

        print("sending thumbnails")
        with open('image.pickle','rb') as f:
            data = f.read(4096)
            while data:
                c.sendall(data)
                data = f.read(4096)
            c.sendall(b'no more data')
        print(c.recv(4096).decode('utf-8'))

        os.remove('image.pickle')

        print('sending search details')
        search_details = [search_result,friend_list,sent]
        c.sendall(pickle.dumps(search_details))
        print('sent')

    elif flag == 'send req'.encode():
        c.sendall("flag received by client".encode())
        print('flag recieved')

        print('receiving details')
        sender_email,receiver_id = pickle.loads(c.recv(4096))
        c.send('received by server'.encode())
        print('received')

        send_req(sender_email,receiver_id)
        print('req sent')

    c.close()
s.close()





