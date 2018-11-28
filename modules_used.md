components:
-
  - sockets for networking
  - sqlite for storing data
  - PIL for image handeling
  - os module for managing file system
  - datetime module for chronological order and keeping track of time
  - pyqt4 for creating gui
  - pickle for converting object to byte strings
  - partial form functools for mapping buttons to functions
  - threading for threading
  - BytesIO for convresion of image into byte

sockets:
-
  the gui that you will be using only serves as a medium to display data. no actual data is stored in the gui or the
  client side of the app. All the data is stored and managed by the server side. your client sends request to fetch data
  from the client which is needed at the given point in time and server fetches it from database or filesystem and provides
  it to the client. The client and server are connected via internet using sockets which are basiclly lower level networking     api.
  
sqlite:
-
  In order to store data permanently databases are used. The database used in this project is sqlite which is a LITE version of
  MySQL and provides easier usability. using same code as a fully fleged MySQL allows for easier protability into an actual       database. the database holds information like fullname, email, password, user id and friend request if any.
  
file system:
-
  since not all data can be stored into databases or not recommended like images, storing user posts and profile pic needs different solution. That's where file system comes in handy. every user has a folder of his/her name in the server, which has all the post made by the user and has different folders like 'feed' containing all the feed images by him/her or friends, 'profile pic' which contains profile picture of the user .
  
datetime module:
-
in order to keep all the posts in chronological order datetime module is being used. all the image posted have the date and time it was posted on associated with its name. while fetching data images are sorted by this datetime criteria. this also gives the functionality of tracking how much time has passed since the post was made just by finding time delta with current datetime while displaying the image.

PIL:
-
since user is going to post images an image handeling module in needed. PIL or pillow is the most widely used and image processing module in python thus used here.

PyQT4:
-
keeping in mind that no user wants to work in ternimal a user interface or a gui is a must in a project like this. PyQT is not certainly the most popular module and also not the most easy to learn or get into but in by far the most updated one according to the current standards compared to Tkinter or any other. thus to provide a solid user interface pyqt4 in implementd. also qt creater which is gui application to create gui using pyqt makes it much easier to create complex and more interwoven gui compared to others

pickel:
-
for converting image objects or string or lists into byte strings to send them through sockets.

partial:
-
in order to like an image or to send friend request to a person or any other such task the respective button should be mapped to their respective function with image or person sepecific information sent as arguments. mapping button with function usual/primitive way only maps the last button to the function and rest are ignored. to solve this problen partial method from functools module is used. tuple are used to send the required information as partial accepts only one argument to a function

threading:
-
there are total 9 server files performing different tasks. running them seperately on differently on different command lines may prove hard to managa and moniter. file 'main.py' in server takes care of this as it automatically runs all the server files and in order for these server files to run independently, threading is used. this may not be a good idea given the situation but it is done for ease of use for demo purposes.

BytesIO
-
to map image directly onto a lable rather than storing it into harddrive and then using its location to map it, the image needs to be converted to bytes first. to achive this we have used BytesIO. saving image to its object and then performing getvalue on it performs the task we need.
