import socket
import sqlite3
import pickle
import os
from PIL import Image as PilImage

def account_settings(flag, new_detail,user_detail):
    
    conn_settings = sqlite3.connect("copro.db")
    cursor_settings  = conn_settings.cursor()

    with conn_settings:
        if flag == 0:
            new_detail = new_detail.upper()
            cursor_settings.execute("""UPDATE accounts
                         SET first = (:new_first)
                         WHERE email = (:email)""",{
                         "new_first": new_detail, 
                         "email": user_detail['email']
                         })
            user_detail['first'] = new_detail
        elif flag == 1:
            new_detail = new_detail.upper()
            cursor_settings.execute("""UPDATE accounts
                         SET last = (:new_last)
                         WHERE email = (:email)""",{
                         "new_last": new_detail,  
                         "email": user_detail['email']
                         })
            user_detail['last'] = new_detail
        elif flag == 2:
            cursor_settings.execute("""SELECT * FROM accounts
                     WHERE email = (:email)""",{
                     "email":new_detail})
            if cursor_settings.fetchone() is not None:
                return 0
            else:
                os.rename(f"account_user{ user_detail['email'] }" , f"account_user{new_detail}")
                path = os.getcwd()
                path =  os.path.join(path,f"account_user{new_detail}")
                os.chdir(path)
                os.rename(f"feed_user{user_detail['email']}" , f"feed_user{new_detail}")
                os.rename(f"profile_pic_user{user_detail['email']}" , f"profile_pic_user{new_detail}")
                os.rename(f"thumbnail_user{user_detail['email']}" , f"thumbnail_user{new_detail}")
                os.chdir("..")
                cursor_settings.execute("""UPDATE accounts
                             SET email = (:new_email),
                             propic = (:new_propic),
                             thumbnail = (:new_thumbnail),
                             feed_thumbnail=(:new_feed_thumbnail)
                             WHERE email = (:email)""",{
                             "email": user_detail['email'],
                              "new_email": new_detail,
                              "new_propic":f"account_user{new_detail}/profile_pic_user{new_detail}/propic.jpg",
                              "new_thumbnail":f"account_user{new_detail}/thumbnail_user{new_detail}/thumbnail.jpg",
                              "new_feed_thumbnail":f"account_user{new_detail}/thumbnail_user{new_detail}/feed_thumbnail.jpg"
                         })
                user_detail['email'] = new_detail
                user_detail['propic'] = f"account_user{new_detail}/profile_pic_user{new_detail}/propic.jpg"

        elif flag == 3:
            cursor_settings.execute("""UPDATE accounts
                         SET password = (:new_pass)
                         WHERE email = (:email)""",{
                         "email": user_detail['email'],
                          "new_pass": new_detail  
                         })
            user_detail['password'] = new_detail
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
        c,add = s.accept()

        print("receiving flag")
        flag = c.recv(4096).decode('utf-8')
        c.sendall('received by server'.encode())
        print("received")
        
        if flag == 'settings':
            print("receiving details")
            details = pickle.loads(c.recv(4096))
            print("received")
            print(details[0])
            print("making changs")
            return_value = account_settings(details[0],details[1],details[2])
            print("done")

            print("sending return values")
            if return_value == 0:
                c.sendall("error".encode())
                c.sendall(str(return_value).encode())
            else:
                c.sendall("no error".encode())
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
                propic,email = pickle.load(f)

            os.remove(f'image_propic.pickle_user{add}')
        
            propic.thumbnail((150,150))
            propic.save(f"account_user{email}/profile_pic_user{email}/propic.jpg")
            propic.thumbnail((60,60))
            propic.save(f"account_user{email}/thumbnail_user{email}/thumbnail.jpg")
            propic.thumbnail((20,20))
            propic.save(f"account_user{email}/thumbnail_user{email}/feed_thumbnail.jpg")
        
        c.close()
        

    s.close()
if __name__ == '__main__':
    main()