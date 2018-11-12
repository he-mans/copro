import socket
import os
from PIL import Image as PilImage
import pickle
import sqlite3

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
            cursor_login.execute("""SELECT first,last,email,id,password,
                         propic,friend_req FROM accounts
                         WHERE email = (:email)""",{"email":entered_email})
            details = cursor_login.fetchone()
            email,password = details[2],details[4]
            if entered_password != password:
                return 1
            else:
                lables = ["first","last","email","id","password",
                         "propic","friend_req"]
                user_detail = {lable:value for lable,value in zip(lables,details)}
                return user_detail

def main():
	port = 2500

	print("creating scoket")
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	print("socket login created")

	print("binding socket login")
	s.bind(('',port))
	print("socket login binded")

	s.listen(4)
	print("server started listening")

	while True:
		c,add = s.accept()
		print("client accepted")

		print("receiving login details")
		login_details=pickle.loads(c.recv(4096))
		print("received")

		email = login_details[0]
		return_status = login(login_details[0],login_details[1])

		print("sending return_status")
		c.sendall(pickle.dumps(return_status))
		print('sent')

		if c.recv(4096).decode('utf-8') == "send":
			print('sending propic and thumbnail sizes')
			propic = PilImage.open(f"account_user{email}/profile_pic_user{email}/propic.jpg")
			thumbnail = PilImage.open(f"account_user{email}/thumbnail_user{email}/thumbnail.jpg")

			print('sending images to client')
			with open("images_login.pickle",'wb') as f:
				images_list = [propic,thumbnail] 
				pickle.dump(images_list,f)

			with open("images_login.pickle",'rb') as f:
				data = f.read(4096000)
				while data:
					c.sendall(data)
					data = f.read(4096000)
			print("sent")
			
			c.close()
			os.remove('images_login.pickle')

		else:	
			c.close()
	s.close()
