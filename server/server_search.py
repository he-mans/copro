import pickle
import socket
import os
import sqlite3
from PIL import Image as PilImage
import traceback
import convert_to_bytes

def search(detail,user_id):
    conn_search = sqlite3.connect("copro.db")
    cursor_search = conn_search.cursor()

    detail = detail.strip().upper()
    with conn_search:
        try:
            first,last = detail.split(" ")
            first,last = first.strip(),last.strip()
            cursor_search.execute("""SELECT first,last,
                         id,thumbnail FROM accounts
                         WHERE first = (:first) AND
                         last = (:last)""",{
                         "first":first,
                         "last":last
                             })
        except:
            first = detail
            cursor_search.execute("""SELECT first,last,
                             id,thumbnail FROM accounts
                             WHERE first = (:first) OR  
                             last = (:first)""",{
                             "first":first
                             })
        search_result = cursor_search.fetchall()

        cursor_search.execute("""SELECT friend_list,sent FROM accounts
                        WHERE id=(:id)""",{
                        "id":user_id
                        })
        friend_list,sent = cursor_search.fetchone()
        friend_list = friend_list.split(" ")
        sent = sent.split(" ")
        return (search_result,friend_list,sent)

def send_req(sender_id,receiver_id):
    conn_search = sqlite3.connect("copro.db")
    cursor_search = conn_search.cursor()

    with conn_search:
        cursor_search.execute("""SELECT first,last,id,thumbnail,sent FROM accounts
                    WHERE id = (:id)""",{
                    "id": sender_id
                    })
        result = list(cursor_search.fetchone())
        sender_detail,sent = result[0:-1],result[-1]
        sender_detail[2] = str(sender_detail[2])
        sender_detail = (" ").join(sender_detail)
        
        sent+=f" {receiver_id}"
        cursor_search.execute("""SELECT friend_req FROM accounts
                    WHERE id = (:id)""",{
                     "id":receiver_id
                     })
        req_list = cursor_search.fetchone()[0]
        req_list = req_list+repr(" ")+sender_detail
        cursor_search.execute("""UPDATE accounts
                     SET friend_req = (:friend_req)
                     WHERE id = (:id)""",{
                     "friend_req":req_list,
                     "id":receiver_id
                     })
        cursor_search.execute("""UPDATE accounts
                    SET sent = (:sent)
                    WHERE id = (:id)""",{
                    "sent":sent,
                    "id":sender_id
                    })

def main():
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

        try:
            c,add = s.accept()
            print("client connected")

            print("receiving flag")
            flag = c.recv(4096)
            if flag =='search'.encode():
                c.sendall("flag received by client".encode())
                print('flag recieved')

                print('receiving details')
                details= pickle.loads(c.recv(4096))
                print('details received')

                
                print("processing request")
                detail,user_id = details
                search_result,friend_list,sent = search(detail,user_id)
                thumbnails = [PilImage.open(result[3]) for result in search_result]
                thumbnails = convert_to_bytes.convert_image(thumbnails)
                search_result = [list(result) for result in search_result]
                for thumbnail,result in zip(thumbnails,search_result):
                    result[3] = thumbnail
                info = [search_result,friend_list,sent]
                print("done")

                
                print("sending information")
                with open(f'result_search{add}.pickle','wb') as f:
                    pickle.dump(info,f)
                with open(f'result_search{add}.pickle','rb') as f:
                    data = f.read(4096)
                    while data:
                        c.sendall(data)
                        data = f.read(4096)
                    c.sendall(b'no more data')
                os.remove(f'result_search{add}.pickle')
                print("sent")

            
            elif flag == 'send req'.encode():
                c.sendall("flag received by client".encode())
                print('flag recieved')

                print('receiving details')
                sender_id,receiver_id = pickle.loads(c.recv(4096))
                c.send('received by server'.encode())
                print('received')

                send_req(sender_id,receiver_id)
                print('req sent')

        except Exception as e:
            print('server_search raised exception :',end = ' ')
            print(e)
            print('traceback for above search error')
            traceback.print_exc()
            break
        c.close()
    s.close()

if __name__ == '__main__':
    main()
