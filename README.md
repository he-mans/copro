# copro
  a small model of a social networking app.

requirments:
  -
  - python 3.6 or above
  - PIL (to install type `pip install pillow` on terminal or cmd)
  - pyqt4 (download pyqt4 for windows for your version of python from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4))
  
    (to download on ubuntu type `apt-cache search pyqt` hit enter and then type `sudo apt-get install python-qt4` on terminal)
  - every other packege is built into python
  - to know more about modules used and why read [modeuls_used.md](https://github.com/planetred-cc/copro/blob/master/modules_used.md#components)
  
how does it works:
  -
  the interface that you are using acts as a client which sends request or data to the server using sockets. The server           gives client the data or store the data in the database and/or the implimented file system. you can see the file 
  system in work yourself by looking in the serve folder. to know more read [how_does_it_works.md](https://github.com/planetred-cc/copro/blob/master/how_does_it_works.md#creating-account)

how to use:
  -
  - download server and client folders and save them on your pc
  - open the server folder and run functions.py to create database file and user count file
  - run main.py in server folder and leave it running
  - open the client folder and run gui.py file
  - (in linux) to close a server terminal use ctrl+c to first force stop the ongoing operation in order to free port    currently being used
  
note:
  -
  currently the app in configured to run if server and client are on the same computer. if you want client to
  run independently on different computer like an actual social networking app then
  - save server folder on a different device
  - go to client folder and open client.py file 
  - change line (line no. 9) ` ip = '127.0.0.1' ` to the ip of the device that your server folder is on (IP must be a string).
  - to find ip on a linux device open terminal and type `ifconfig`  
  - to find ip on a windows device open cmd and type `ipconfig /all` (use ipv4 address) 

- **to know how it works or which modules are used and why read respective .md files**
- **if programm gives ERROR `TabError: inconsistent use of tabs and spaces in indentation` change indentation to spaces in both client.py and gui.py**
