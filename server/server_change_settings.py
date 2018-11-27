import socket
import sqlite3
import pickle
import os
from PIL import Image as PilImage
import traceback

def account_settings(flag, new_detail,user_detail):
    
    conn_settings = sqlite3.connect("copro.db")
    cursor_settings  = conn_settings.cursor()

    with conn_settings:
        if flag == 0:
            new_detail = new_detail.upper()
            cursor_settings.execute("""UPDATE accounts
                         SET first = (:new_first)
                         WHERE id = (:id)""",{
                         "new_first": new_detail, 
                         "id": user_detail['id']
                         })
            user_detail['first'] = new_detail
        elif flag == 1:
            new_detail = new_detail.upper()
            cursor_settings.execute("""UPDATE accounts
                         SET last = (:new_last)
                         WHERE id = (:id)""",{
                         "new_last": new_detail,  
                         "id": user_detail['id']
                         })
            user_detail['last'] = new_detail
        elif flag == 2:
            cursor_settings.execute("""SELECT * FROM accounts
                     WHERE email = (:email)""",{
                     "email":new_detail})
            if cursor_settings.fetchone() is not None:
                return 0
            else:
                cursor_settings.execute("""UPDATE accounts
                             SET email = (:new_email)
                             WHERE id = (:id)""",{
                              "new_email": new_detail,
                              "id": user_detail['id']
                              })
                user_detail['email'] = new_detail

        elif flag == 3:
            cursor_settings.execute("""UPDATE accounts
                         SET password = (:new_pass)
                         WHERE id = (:id)""",{
                         "id": user_detail['id'],
                          "new_pass": new_detail  
                         })
    return user_detail

def main():
    port = 3000

    print("creating socket")
    s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print("socket created")

    print("binding socket")
    s.bind(('',port))
    print("binding complete")

    s.listen(4)
    print("started listening")

    while True:
        try:
            c,add = s.accept()

            print("receiving flag")
            flag = c.recv(4096).decode('utf-8')
            c.sendall('received by server'.encode())
            print("received")
            
            if flag == 'settings':
                print("receiving details")
                details = pickle.loads(c.recv(4096))
                print("received")
                print("making changs")
                return_value = account_settings(details[0],details[1],details[2])
                print("done")

                print("sending return values")
                c.sendall(pickle.dumps(return_value))

            elif flag == 'propic':

                print('receiving propic')
                with open(f'image_propic.pickle_user{add}','wb') as f:
                    data = c.recv(4096)
                    while True:
                        if data.endswith(b'no more data'):
                            data = data.split(b'no more data')[0]
                            f.write(data)
                            break
                        f.write(data)
                        data = c.recv(4096)
                c.sendall('propic received by client'.encode())
                print('propic received')

                with open(f'image_propic.pickle_user{add}','rb') as f:
                    propic,user_id = pickle.load(f)

                os.remove(f'image_propic.pickle_user{add}')
            
                propic.thumbnail((150,150))
                propic.save(f"account_user{user_id}/profile_pic_user{user_id}/propic.jpg")
                propic.thumbnail((60,60))
                propic.save(f"account_user{user_id}/thumbnail_user{user_id}/thumbnail.jpg")
                propic.thumbnail((20,20))
                propic.save(f"account_user{user_id}/thumbnail_user{user_id}/feed_thumbnail.jpg")
            
        except Exception as e:
            print('server_change_settings raised exception :',end = ' ')
            print(e)
            print('traceback for above change_settings error')
            traceback.print_exc()
        c.close()
        

    s.close()
if __name__ == '__main__':
    main()