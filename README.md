# copro
this is a small model of a social networking app like instagram.

requirments:
  -
  - python 3.6 or above
  - PIL (to install type `pip install pillow` on termanil or cmd)
  - pyqt4 (download pyqt4 for your version from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4))
  - every other packege is built into python
  
how does it works:
  -
  the interface that you are using acts as a client which sends request or data to the server using sockets. The server           gives client the data or store the data from/in the database and/or the implimented file system. you can see the file 
  system in work yourself by looking in the serve folder.

how to use:
  -
  - download server.zip and client.zip and unzip them
  - save both server and client folder on your pc
  - open the server folder and run functions.py to create database file and user count file
  - run all the server .py files in server folder and leave them running
  - open the client folder and run gui.py file
  - (in linux) to close a server terminal use ctrl+c to first force stop the current going operation in order to free port    currently used
  
note:
  -
  currently the app in configured to run if server and client are on the same computer. if you want client to
  run independently on different computer like an actual social networking app then
  - save server folder on a different device
  - go to client folder and open client.py file 
  - change line (line no. 9) ` ip = '127.0.0.1' ` to the ip of the device that your server folder is on (IP must a string).
  - to find ip on a linux device open terminal and type `ifconfig`  
  - to find ip on a windows device open terminal and type `ifconfig /all` (use ipv4 address) 
