import socket
import os
from PIL import Image as PilImage
import pickle
import sqlite3
import traceback
import convert_to_bytes

def login(entered_email,entered_password):
    
    conn_login = sqlite3.connect("copro.db")
    cursor_login=conn_login.cursor()

    entered_password,entered_email = entered_password.strip(),entered_email.strip()
    print(entered_password,entered_email)
    with conn_login:
        cursor_login.execute("""SELECT * FROM accounts
                     WHERE email = (:email)""",{'email':entered_email})
        if cursor_login.fetchone() is None: 
            return 0
        else:
            cursor_login.execute("""SELECT first,last,email,id,password
                                    FROM accounts
                                    WHERE email = (:email)""",{"email":entered_email}
                                )
            details = cursor_login.fetchone()
            email,password = details[2],details[4]
            if entered_password != password:
                return 1
            else:
                lables = ["first","last","email","id","password"]
                user_detail = {lable:value for lable,value in zip(lables,details) if lable!="password"}
                return user_detail

def main():
    port = 2500

    print("creating scoket")
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s: 
        print("socket login created")
        
        print("binding socket login")
        s.bind(('',port))
        print("socket login binded")
        
        s.listen(4)
        print("server started listening")

        while True:
            try:
                c,add = s.accept()
                print("client accepted")

                print("receiving login details")
                login_details=pickle.loads(c.recv(4096))
                print("received")

                return_status = login(login_details[0],login_details[1])

                print("sending return status")
                if return_status == 0 or return_status == 1:
                    c.sendall(pickle.dumps(return_status))

                else:
                    user_id = return_status["id"]

                    propic = PilImage.open(f"account_user{user_id}/profile_pic_user{user_id}/propic.jpg")
                    thumbnail = PilImage.open(f"account_user{user_id}/thumbnail_user{user_id}/thumbnail.jpg")

                    propic_bytes = convert_to_bytes.convert_image(propic)
                    thumbnail_bytes = convert_to_bytes.convert_image(thumbnail)

                    return_status.update({"propic":propic_bytes})
                    return_status.update({"thumbnail":thumbnail_bytes})

                    with open("data_login.pickle",'wb') as f:
                        pickle.dump(return_status,f)

                    with open("data_login.pickle",'rb') as f:
                        data = f.read(4096000)
                        while data:
                            c.sendall(data)
                            data = f.read(4096000)
                    os.remove('data_login.pickle')
                print("sent")
                    
            except Exception as e:
                print('server_login raised exception :',end = ' ')
                print(e)
                print('traceback for above login error')
                traceback.print_exc()
                break
            
            c.close()

if __name__ == '__main__':
    main()