components:
-
  - sockets for networking
  - sqlite for storing data
  - PIL for image handeling
  - os module for managing file system
  - datetime module for chronological order and keeping track of time
  - pyqt4 for creating gui

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
  since not all data can be stored into databases or not recommended like images, storing user posts and profile pic needs different solution. That's where file system comes in handy. every user has a folder of his/her name in the server, which has all the post made by the user and has different folders like 'feed' containing all the images in her current existing feed posted by him/her or friends, 'profile pic' which contains profile picture of the user .
  
datetime module:
-
in order to keep all the posts in chronological order datetime module is being used. all the image posted have the date and time it was posted on associated with its name. while fetching data images are sorted by this datetime criteria. this also gives the functionality of tracking how much time has passed since the post was made just by finding time delta with current datetime while displaying the image.

PIL:
-
since user is going to post images a image processing module in needed. PIL or pillow is the most widely used and image processing module in python thus used here.

PyQT4:
-
keeping in mind that no user wants to work in ternimal a user interface or a gui is a must in a project like this. PyQT is not certainly the most popular module and also not the most easy to learn or get into but in by far the most updated one according to the current standards compared to Tkinter or any other. thus to provide a solid user interface pyqt4 in implementd. also qtcreated which is gui application to create gui using pyqt makes it much easier to create complex and more interwoven gui compared to others