import socket
import os
import pickle
def add_like(image,p_id,user_email,email):
    image_txt = image.replace(".jpg",".txt")
    
    with open(f"account_user{email}/{image_txt}","r") as f:
        likes = int(f.read())
    with open(f"account_user{email}/{image_txt}","w") as f:
        f.write(str(likes+1))
    image_txt = image.replace(".jpg","_people_liked.txt")
    with open(f"account_user{email}/{image_txt}","a") as f:
        f.write(f"{p_id}\n")
    return likes+1

def remove_like(image,p_id,user_email,email):
    image_txt = image.replace(".jpg",".txt")
    with open(f"account_user{email}/{image_txt}","r") as f:
        likes = int(f.read())
    with open(f"account_user{email}/{image_txt}","w") as f:
        f.write(str(likes-1))
    image_txt = image.replace(".jpg","_people_liked.txt")
    with open(f"account_user{email}/{image_txt}","r") as f:
        liked_people = [ids.strip() for ids in f.readlines()]
    liked_people.remove(str(p_id))
    with open(f"account_user{email}/{image_txt}","w") as f:
        f.truncate(0)
        for people in liked_people:
            f.write(people+"\n")
    return likes-1    


port = 4500

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("socket made")

print("binding socket")
s.bind(('',port))
print('socket binded')

s.listen(4)
print('socket started to listen')

while True:
	c,add = s.accept()
	print('connected to client')

	print("receiving details")
	details = pickle.loads(c.recv(4096))
	c.sendall('received by server'.encode())

	if details[-1] == "like":
		like_count = add_like(details[0],details[1],details[2],details[3])

	elif details[-1] == "unlike":
		like_count = remove_like(details[0],details[1],details[2],details[3])

	print("sending like count")
	c.sendall(pickle.dumps(like_count))

	c.close()

s.close()