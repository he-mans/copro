creating account:
-
as soon as you fill the credentials and click signup button, the data is sent to server which checks whethere there is already existing email or not as there cannot be ambiguity in emails. if not then your account is created, data is saved in database and a folder of your name in created in the server computer where all the post you made are saved. moreover other folders are made inside the main folder which contains your feed, profile pic, thumbnail etc.

logging in:
-
as soon as you click the login button server checks if the password entered is correct or not. if correct, it sends some data to your gui like profile pic, fullname, email etc. which is needed for different tasks. also all your feed is sent to gui/client which is then displayed as soon as you enter your account. the feed is sorted in chronological order and the person who posted is identifind, his thumbnail and fullname is also retrived and displayed.

uploading image or profile pic:
-
uploading a image for post/feed or for new profile pic are basically same. image is sent to the server and then it is saved to respective forlde feed or profile_pic. in case feed the image is saved in with a unique naming scheme which inclide the date and time it was added and the user id it was added by. two txt files are made which keep track of no. of likes and the people that have liked the post. the feed image is saved to all the friend's feed folder the user has.

searching and freind request:
-
while seraching the the database is returns all the user whose either first name or lastname or fullname resembles to the text entered by user. also his id and thumbnail is returned. thumbnail so that user can identify different results and id in case you want to send the person a friend request. when you send a person a friend request, your id is saved in his request list and his id is saved into your sent list in order to prevent possiblity of sending the request to him again.

accepting or rejecting request:
- 
request list is stored in database in form of a string. if of different users are seperated by a space which can be easily converted into a list and then parese into int. when viewing frined request this method is used to retreive the id of the requesters and if request is accepted the id is removed form the list, added to friend list which is also stored in the same way and then the updated list converted into a string and is stored in database and you are removed from his sent list.

for reject it is same process but he/she is not added into your friend list.

liking and unliking posts:
-
while loading image in gui, it is checked if you have already liked the post or not(list of people that liked the image is provided by server). if you already liked the image the the respective icon is applied to the like button and button is mapped to the unlike function and vice verca for if you didn't already liked the image. as soon as you like or unlike the image, the icon of the like button is changed, previous connection of the button to function is deleted and new connection is made to the opposit function i.e. like to unlike/unlike to like. and changes are made respectively to the files.

scouting:
-
by clicking the person name in feed or search or friend request page you can enter their profile(scout mode) and see all the post they have made. this works exactly similar to the feed but insted of getting the person feed it gets all the image posted by him.
