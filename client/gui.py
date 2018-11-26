from PyQt4 import QtCore, QtGui
from functools import partial
import sys
import client
from datetime import datetime 
import time
import threading
        
QtGui.QApplication.setStyle("Plastique")
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class create_account_thread(QtCore.QThread):
    signal = QtCore.pyqtSignal(int)
    def __init__(self,first,last,email,password):
        QtCore.QThread.__init__(self)
        self.first = first
        self.last = last
        self.email = email
        self.password = password

    def run(self):
        try:
            status = client.create(self.first,self.last,self.email,self.password)
            self.signal.emit(status)
        except ConnectionRefusedError:
            self.signal.emit(-1)

class login_thread(QtCore.QThread):
    signal = QtCore.pyqtSignal(dict)
    signal_error = QtCore.pyqtSignal(int)
    def __init__(self,email,password):
        QtCore.QThread.__init__(self)
        self.email = email
        self.password = password

    def run(self):
        try:
            status = client.login(self.email,self.password)
            if status == 1 or status == 0:
                self.signal_error.emit(status)
            else:
                self.signal.emit(status)
        except ConnectionRefusedError:
            self.signal_error.emit(-1)


class feed_thread(QtCore.QThread):
    signal = QtCore.pyqtSignal(list)
    signal_error = QtCore.pyqtSignal(str)
    def __init__(self,email,parent = None):
        QtCore.QThread.__init__(self,parent)
        self.email = email

    def run(self):
        self.running = True
        try:
            images,thumbnails,full_names,likes,ids,people_liked,emails,times= client.fetch_feed(self.email)
            feed = [(image,full_name,thumbnail,like,p_id,peoples,email,time) for image,full_name,thumbnail,like,p_id,peoples,email,time in zip(
                            images,full_names,thumbnails,likes,ids,people_liked,emails,times)]
            self.signal.emit(feed)
        except ConnectionRefusedError:
            self.signal_error.emit("Connection refused by server")

class search_thread(QtCore.QThread):
    signal = QtCore.pyqtSignal(list)
    signal_error = QtCore.pyqtSignal(str)
    def __init__(self,searched,email,parent=None):
        QtCore.QThread.__init__(self,parent)
        self.email = email
        self.searched = searched
    
    def run(self):
        try:
            self.running = True
            search_result,friend_list,sent = client.search(self.searched,self.email)
            self.signal.emit([search_result,friend_list,sent])
        except ConnectionRefusedError:
            self.signal_error.emit("Connection refused by server")

class friend_thread(QtCore.QThread):
    signal = QtCore.pyqtSignal(list)
    signal_error = QtCore.pyqtSignal(str)
    def __init__(self,email,parent=None):
        QtCore.QThread.__init__(self,parent)
        self.email = email

    def run(self):
        try:
            self.running = True
            req_list = client.fetch_req(self.email)
            self.signal.emit(req_list)
        except ConnectionRefusedError as e:
            self.signal_error.emit("Connection refused by server")

class scout_thread(QtCore.QThread):
    signal = QtCore.pyqtSignal(tuple)
    signal_error = QtCore.pyqtSignal(str)
    def __init__(self,email,person_email,person_id,fullname,parent = None):
        QtCore.QThread.__init__(self,parent)
        self.user_email = email
        self.person_id = person_id
        self.person_email = person_email
        self.fullname = fullname

    def run(self):
        try:
            self.running = True
            details = client.fetch_scout_view(self.user_email,self.person_email,self.person_id)
            details+=(self.person_email,self.person_id,self.fullname)
            self.signal.emit(details)
        except ConnectionRefusedError:
            self.signal_error.emit("Connection refused by server")

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(400, 600)
        MainWindow.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.copro = QtGui.QWidget(MainWindow)
        self.copro.setObjectName(_fromUtf8("copro"))
        self.gridLayout_2 = QtGui.QGridLayout(self.copro)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.stackedWidget = QtGui.QStackedWidget(self.copro)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        font.setPointSize(8)
        self.stackedWidget.setFont(font)
        self.stackedWidget.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);\n"
"\n"
""))
        self.stackedWidget.setObjectName(_fromUtf8("stackedWidget"))
        self.login_page = QtGui.QWidget()
        self.login_page.setObjectName(_fromUtf8("login_page"))
        self.gridLayout = QtGui.QGridLayout(self.login_page)
        self.gridLayout.setContentsMargins(0,0,0,0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        
        self.horizontalLayout = QtGui.QHBoxLayout()
        spacerItem_login2 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        self.horizontalLayout.addItem(spacerItem_login2)

        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem_0 = QtGui.QSpacerItem(300,40,QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem_0)
        self.le_email = QtGui.QLineEdit(self.login_page)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_email.sizePolicy().hasHeightForWidth())
        self.le_email.setSizePolicy(sizePolicy)
        font = self.generate_font(family = "Comic Sans MS", point_size = 10)
        self.le_email.setFont(font)
        self.le_email.setStyleSheet(_fromUtf8("background-color: rgb(222, 209, 193);"))
        self.le_email.setObjectName(_fromUtf8("le_email"))
        self.verticalLayout.addWidget(self.le_email)
        self.le_password = QtGui.QLineEdit(self.login_page)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_password.sizePolicy().hasHeightForWidth())
        self.le_password.setSizePolicy(sizePolicy)
        self.le_password.setFont(font)
        self.le_password.setStyleSheet(_fromUtf8("background-color: rgb(222, 209, 193);"))
        self.le_password.setEchoMode(QtGui.QLineEdit.Password)
        self.le_password.setObjectName(_fromUtf8("le_password"))
        self.verticalLayout.addWidget(self.le_password)
        self.btn_login = QtGui.QPushButton(self.login_page)
        font = self.generate_font(family = "Ubuntu Condensed", point_size = 10, set_bold = True)
        self.btn_login.setFont(font)
        self.btn_login.setStyleSheet(_fromUtf8("background-color: rgb(69, 142, 255);"))
        self.btn_login.setAutoRepeat(False)
        self.btn_login.setObjectName(_fromUtf8("btn_login"))
        self.verticalLayout.addWidget(self.btn_login)
        
        self.horizontalLayout_2_login = QtGui.QHBoxLayout()
        #self.horizontalLayout_2_login.setContentsMargins(0, 10, -1, -1)
        self.label = QtGui.QLabel(self.login_page)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = self.generate_font(family = "Ubuntu", point_size = 9)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        
        self.horizontalLayout_2_login.addWidget(self.label)
        self.btn_sign_up = QtGui.QPushButton(self.login_page)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_sign_up.sizePolicy().hasHeightForWidth())
        self.btn_sign_up.setSizePolicy(sizePolicy)
        self.btn_sign_up.setFont(font)
        self.btn_sign_up.setFlat(True)
        self.btn_sign_up.setObjectName(_fromUtf8("btn_sign_up"))
        self.horizontalLayout_2_login.addWidget(self.btn_sign_up)
        spacerItem_login1 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2_login.addItem(spacerItem_login1)

        self.verticalLayout.addLayout(self.horizontalLayout_2_login)
        spacerItem_4 = QtGui.QSpacerItem(300,40,QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem_4)

        
        self.horizontalLayout.addLayout(self.verticalLayout)
        
        spacerItem_login3 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        self.horizontalLayout.addItem(spacerItem_login3)
        self.gridLayout.addLayout(self.horizontalLayout,9,1,1,1)
        
        self.stackedWidget.addWidget(self.login_page)
#---------------------------------------------------------------------------------------------------------------------------#        
#---------------------------------------------------------------------------------------------------------------------------#
        self.sign_up_page = QtGui.QWidget()
        self.sign_up_page.setObjectName(_fromUtf8("sign_up_page"))
        self.gridLayout_3 = QtGui.QGridLayout(self.sign_up_page)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.gridLayout_3.setContentsMargins(0,0,0,0)
        spacerItem11 = QtGui.QSpacerItem(385, 77, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem11, 0, 0, 1, 5)
        self.line = QtGui.QFrame(self.sign_up_page)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout_3.addWidget(self.line, 1, 0, 1, 5)
        spacerItem12 = QtGui.QSpacerItem(385, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem12, 2, 0, 1, 5)
        spacerItem13 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem13, 3, 0, 1, 1)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.le_first_su = QtGui.QLineEdit(self.sign_up_page)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_first_su.sizePolicy().hasHeightForWidth())
        self.le_first_su.setSizePolicy(sizePolicy)
        font = self.generate_font(family = "Comic sans MS", point_size = 10)
        self.le_first_su.setFont(font)
        self.le_first_su.setStyleSheet(_fromUtf8("background-color: rgb(222, 209, 193);"))
        self.le_first_su.setText(_fromUtf8(""))
        self.le_first_su.setObjectName(_fromUtf8("le_first_su"))
        self.verticalLayout_2.addWidget(self.le_first_su)
        self.le_last_su = QtGui.QLineEdit(self.sign_up_page)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_last_su.sizePolicy().hasHeightForWidth())
        self.le_last_su.setSizePolicy(sizePolicy)
        self.le_last_su.setFont(font)
        self.le_last_su.setStyleSheet(_fromUtf8("background-color: rgb(222, 209, 193);"))
        self.le_last_su.setObjectName(_fromUtf8("le_last_su"))
        self.verticalLayout_2.addWidget(self.le_last_su)
        self.le_email_su = QtGui.QLineEdit(self.sign_up_page)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_email_su.sizePolicy().hasHeightForWidth())
        self.le_email_su.setSizePolicy(sizePolicy)
        self.le_email_su.setFont(font)
        self.le_email_su.setStyleSheet(_fromUtf8("background-color: rgb(222, 209, 193);"))
        self.le_email_su.setObjectName(_fromUtf8("le_email_su"))
        self.verticalLayout_2.addWidget(self.le_email_su)
        self.le_pass_su = QtGui.QLineEdit(self.sign_up_page)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_pass_su.sizePolicy().hasHeightForWidth())
        self.le_pass_su.setSizePolicy(sizePolicy)
        self.gridLayout_3.addWidget(self.line, 1, 0, 1, 5)
        self.le_pass_su.setFont(font)
        self.le_pass_su.setStyleSheet(_fromUtf8("background-color: rgb(222, 209, 193);"))
        self.le_pass_su.setEchoMode(QtGui.QLineEdit.Password)
        self.le_pass_su.setObjectName(_fromUtf8("le_pass_su"))
        self.verticalLayout_2.addWidget(self.le_pass_su)
        self.btn_sign_up_su = QtGui.QPushButton(self.sign_up_page)
        font = self.generate_font(family="Ubuntu Condensed",point_size = 10, set_bold = True)
        self.btn_sign_up_su.setFont(font)
        self.btn_sign_up_su.setStyleSheet(_fromUtf8("background-color: rgb(69, 142, 255);"))
        self.btn_sign_up_su.setAutoRepeat(False)
        self.btn_sign_up_su.setObjectName(_fromUtf8("btn_sign_up_su"))
        self.verticalLayout_2.addWidget(self.btn_sign_up_su)
        self.gridLayout_3.addLayout(self.verticalLayout_2, 3, 1, 5, 3)
        spacerItem14 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem14, 3, 4, 1, 1)
        spacerItem15 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem15, 4, 0, 1, 1)
        spacerItem16 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem16, 4, 4, 1, 1)
        spacerItem17 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem17, 5, 0, 1, 1)
        spacerItem18 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem18, 5, 4, 1, 1)
        spacerItem19 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem19, 6, 0, 1, 1)
        spacerItem20 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem20, 6, 4, 1, 1)
        spacerItem21 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem21, 7, 0, 1, 1)
        spacerItem22 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem22, 7, 4, 1, 1)
        spacerItem23 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem23, 8, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.sign_up_page)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = self.generate_font(family = "Ubuntu",point_size=10)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_3.addWidget(self.label_2, 8, 1, 1, 1)
        self.btn_back_su = QtGui.QPushButton(self.sign_up_page)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_back_su.sizePolicy().hasHeightForWidth())
        self.btn_back_su.setSizePolicy(sizePolicy)
        font = self.generate_font(family = "Ubuntu",point_size = 10)
        #font.setWeight(50)
        self.btn_back_su.setFont(font)
        self.btn_back_su.setFlat(True)
        self.btn_back_su.setObjectName(_fromUtf8("btn_back_su"))
        self.gridLayout_3.addWidget(self.btn_back_su, 8, 2, 1, 1)
        spacerItem24 = QtGui.QSpacerItem(135, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem24, 8, 3, 1, 2)
        spacerItem25 = QtGui.QSpacerItem(385, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem25, 9, 0, 1, 5)
        self.line_3 = QtGui.QFrame(self.sign_up_page)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.gridLayout_3.addWidget(self.line_3, 10, 0, 1, 5)
        spacerItem26 = QtGui.QSpacerItem(385, 76, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem26, 11, 0, 1, 5)
        self.stackedWidget.addWidget(self.sign_up_page)
#------------------------------------------------------------------------------------------------------------------------------------------#        
#------------------------------------------------------------------------------------------------------------------------------------------#
        self.home_page = QtGui.QWidget()
        self.home_page.setObjectName(_fromUtf8("home_page"))
        self.gridLayout_4 = QtGui.QGridLayout(self.home_page)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.gridLayout_4.setContentsMargins(0,0,0,0)
        self.btn_feed = QtGui.QPushButton(self.home_page)
        self.btn_feed.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/feed/feed.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.btn_feed.setIcon(icon)
        self.btn_feed.setIconSize(QtCore.QSize(35, 35))
        self.btn_feed.setFlat(True)
        self.btn_feed.setObjectName(_fromUtf8("btn_feed"))
        self.gridLayout_4.addWidget(self.btn_feed, 2, 1, 1, 1)
        spacerItem27 = QtGui.QSpacerItem(28, 28, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem27, 1, 0, 2, 1)
        self.line_2 = QtGui.QFrame(self.home_page)
        self.line_2.setFrameShadow(QtGui.QFrame.Raised)
        self.line_2.setLineWidth(2)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout_4.addWidget(self.line_2, 1, 1, 1, 5)
        self.btn_frnd_req = QtGui.QPushButton(self.home_page)
        self.btn_frnd_req.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/req/friend_request.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/newPrefix/feed.png")), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.btn_frnd_req.setIcon(icon1)
        self.btn_frnd_req.setIconSize(QtCore.QSize(32, 32))
        self.btn_frnd_req.setFlat(True)
        self.btn_frnd_req.setObjectName(_fromUtf8("btn_frnd_req"))
        self.gridLayout_4.addWidget(self.btn_frnd_req, 2, 4, 1, 1)
        self.btn_account = QtGui.QPushButton(self.home_page)
        self.btn_account.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/account/propic.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.btn_account.setIcon(icon2)
        self.btn_account.setIconSize(QtCore.QSize(25, 25))
        self.btn_account.setFlat(True)
        self.btn_account.setObjectName(_fromUtf8("btn_account"))
        self.gridLayout_4.addWidget(self.btn_account, 2, 5, 1, 1)
        self.btn_post = QtGui.QPushButton(self.home_page)
        self.btn_post.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/post/post.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.btn_post.setIcon(icon3)
        self.btn_post.setIconSize(QtCore.QSize(50, 50))
        self.btn_post.setFlat(True)
        self.btn_post.setObjectName(_fromUtf8("btn_post"))
        self.gridLayout_4.addWidget(self.btn_post, 2, 3, 1, 1)
        self.btn_find_people = QtGui.QPushButton(self.home_page)
        self.btn_find_people.setText(_fromUtf8(""))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/search/search.jpg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.btn_find_people.setIcon(icon4)
        self.btn_find_people.setIconSize(QtCore.QSize(30, 30))
        self.btn_find_people.setFlat(True)
        self.btn_find_people.setObjectName(_fromUtf8("btn_find_people"))
        self.gridLayout_4.addWidget(self.btn_find_people, 2, 2, 1, 1)
        spacerItem28 = QtGui.QSpacerItem(28, 28, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem28, 1, 6, 2, 1)
        self.stackedWidget_2 = QtGui.QStackedWidget(self.home_page)
        self.stackedWidget_2.setFont(font)
        self.stackedWidget_2.setObjectName(_fromUtf8("stackedWidget_2"))
        self.stackedWidget_2.setContentsMargins(0,0,0,0)
#------------------------------------------------------------------------------------------------------------------------------------------------------#        
#------------------------------------------------------------------------------------------------------------------------------------------------------#
        self.feed = QtGui.QWidget()
        self.feed.setObjectName(_fromUtf8("feed"))
        self.gridLayout_9 = QtGui.QGridLayout(self.feed)
        self.gridLayout_9.setObjectName(_fromUtf8("gridLayout_9"))
        self.gridLayout_9.setContentsMargins(0,0,0,0)
        self.scrollArea_3 = QtGui.QScrollArea(self.feed)
        self.scrollArea_3.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea_3.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollArea_3.setObjectName(_fromUtf8("scrollArea_3"))
        self.scrollArea_3.setFrameShape(QtGui.QFrame.NoFrame)
        self.scrollAreaWidgetContents_3 = QtGui.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 498, 355))
        self.scrollAreaWidgetContents_3.setObjectName(_fromUtf8("scrollAreaWidgetContents_3"))
        self.verticalLayout_22 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents_3)
        self.verticalLayout_22.setObjectName(_fromUtf8("verticalLayout_22"))
        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_3)
        self.gridLayout_9.addWidget(self.scrollArea_3, 0, 0, 1, 1)
        self.stackedWidget_2.addWidget(self.feed)
        
#-----------------------------------------------------------------------------------------------------------------------------#        
#-----------------------------------------------------------------------------------------------------------------------------#
        self.find_people = QtGui.QWidget()
        self.find_people.setObjectName(_fromUtf8("find_people"))
        self.gridLayout_7 = QtGui.QGridLayout(self.find_people)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.gridLayout_7.setContentsMargins(0,0,0,0)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.le_search = QtGui.QLineEdit(self.find_people)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_search.sizePolicy().hasHeightForWidth())
        self.le_search.setSizePolicy(sizePolicy)
        font = self.generate_font(family = "Comic Sans MS", point_size = 12)
        self.le_search.setFont(font)
        self.le_search.setStyleSheet(_fromUtf8("background-color: rgb(222, 209, 193);"))
        self.le_search.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout_7.addWidget(self.le_search)
        self.btn_clear = QtGui.QPushButton(self.find_people)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_clear.sizePolicy().hasHeightForWidth())
        self.btn_clear.setSizePolicy(sizePolicy)
        font = self.generate_font(family = "Comic Sans MS", point_size = 10, set_bold = True)
        #font.setWeight(75)
        self.btn_clear.setFont(font)
        self.btn_clear.setStyleSheet(_fromUtf8(""))
        self.btn_clear.setAutoDefault(True)
        self.btn_clear.setDefault(False)
        self.btn_clear.setFlat(True)
        self.btn_clear.setObjectName(_fromUtf8("btn_clear"))
        self.horizontalLayout_7.addWidget(self.btn_clear)
        self.btn_search = QtGui.QPushButton(self.find_people)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_search.sizePolicy().hasHeightForWidth())
        self.btn_search.setSizePolicy(sizePolicy)
        #font.setWeight(75)
        self.btn_search.setFont(font)
        self.btn_search.setStyleSheet(_fromUtf8(""))
        self.btn_search.setAutoDefault(True)
        self.btn_search.setDefault(False)
        self.btn_search.setFlat(True)
        self.btn_search.setObjectName(_fromUtf8("btn_search"))
        self.horizontalLayout_7.addWidget(self.btn_search)
        self.gridLayout_7.addLayout(self.horizontalLayout_7, 0, 0, 1, 1)
        self.scrollArea = QtGui.QScrollArea(self.find_people)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.scrollArea.setFont(font)
        self.scrollArea.setLineWidth(1)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollArea.setFrameShape(QtGui.QFrame.NoFrame)
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 500, 320))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalLayout_11 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_11.setObjectName(_fromUtf8("verticalLayout_11"))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_7.addWidget(self.scrollArea, 2, 0, 1, 1)
        self.stackedWidget_2.addWidget(self.find_people)
#---------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------#        
        self.frnd_req = QtGui.QWidget()
        self.frnd_req.setObjectName(_fromUtf8("frnd_req"))
        self.gridLayout_8 = QtGui.QGridLayout(self.frnd_req)
        self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
        self.gridLayout_8.setContentsMargins(0,0,0,0)
        font = self.generate_font(family = "Ubuntu Condensed", point_size=10,set_bold = True)
        self.scrollArea_2 = QtGui.QScrollArea(self.frnd_req)
        self.scrollArea_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName(_fromUtf8("scrollArea_2"))
        self.scrollAreaWidgetContents_2 = QtGui.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 500, 357))
        self.scrollAreaWidgetContents_2.setObjectName(_fromUtf8("scrollAreaWidgetContents_2"))
        self.verticalLayout_12 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_12.setObjectName(_fromUtf8("verticalLayout_12"))
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.gridLayout_8.addWidget(self.scrollArea_2)
        self.stackedWidget_2.addWidget(self.frnd_req)
#-------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------------#        
        self.account = QtGui.QWidget()
        self.account.setObjectName(_fromUtf8("account"))
        self.gridLayout_5 = QtGui.QGridLayout(self.account)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.gridLayout_5.setContentsMargins(0,0,0,0)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        spacerItem37 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_6.addItem(spacerItem37)
        spacerItem38 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_6.addItem(spacerItem38)
        spacerItem39 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_6.addItem(spacerItem39)
        spacerItem40 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_6.addItem(spacerItem40)
        spacerItem41 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_6.addItem(spacerItem41)
        spacerItem42 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_6.addItem(spacerItem42)
        self.horizontalLayout_2.addLayout(self.verticalLayout_6)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        spacerItem43 = QtGui.QSpacerItem(258, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_3.addItem(spacerItem43)
        spacerItem44 = QtGui.QSpacerItem(258, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_3.addItem(spacerItem44)
        spacerItem45 = QtGui.QSpacerItem(258, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_3.addItem(spacerItem45)
        spacerItem46 = QtGui.QSpacerItem(258, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_3.addItem(spacerItem46)
        spacerItem47 = QtGui.QSpacerItem(258, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_3.addItem(spacerItem47)
        spacerItem48 = QtGui.QSpacerItem(258, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_3.addItem(spacerItem48)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.gridLayout_5.addLayout(self.horizontalLayout_2, 2, 2, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        spacerItem49 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_4.addItem(spacerItem49)
        spacerItem50 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_4.addItem(spacerItem50)
        spacerItem51 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_4.addItem(spacerItem51)
        spacerItem52 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_4.addItem(spacerItem52)
        spacerItem53 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_4.addItem(spacerItem53)
        spacerItem54 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_4.addItem(spacerItem54)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        spacerItem55 = QtGui.QSpacerItem(18, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_5.addItem(spacerItem55)
        spacerItem56 = QtGui.QSpacerItem(18, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_5.addItem(spacerItem56)
        spacerItem57 = QtGui.QSpacerItem(18, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_5.addItem(spacerItem57)
        spacerItem58 = QtGui.QSpacerItem(18, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_5.addItem(spacerItem58)
        spacerItem59 = QtGui.QSpacerItem(18, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_5.addItem(spacerItem59)
        spacerItem60 = QtGui.QSpacerItem(18, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_5.addItem(spacerItem60)
        self.horizontalLayout.addLayout(self.verticalLayout_5)
        self.gridLayout_5.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        self.verticalLayout_8 = QtGui.QVBoxLayout()
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.label_4 = QtGui.QLabel(self.account)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = self.generate_font(family = "Ubuntu Condensed",point_size=15,set_bold=True)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_8.addWidget(self.label_4)
        self.btn_first_as = QtGui.QPushButton(self.account)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_first_as.sizePolicy().hasHeightForWidth())
        self.btn_first_as.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu Condensed"))
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.btn_first_as.setFont(font)
        self.btn_first_as.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btn_first_as.setStyleSheet(_fromUtf8("Text-align:left"))
        self.btn_first_as.setFlat(True)
        self.btn_first_as.setObjectName(_fromUtf8("btn_first_as"))
        self.verticalLayout_8.addWidget(self.btn_first_as)
        self.btn_last_as = QtGui.QPushButton(self.account)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_last_as.sizePolicy().hasHeightForWidth())
        self.btn_last_as.setSizePolicy(sizePolicy)
        #font.setWeight(50)
        self.btn_last_as.setFont(font)
        self.btn_last_as.setStyleSheet(_fromUtf8("Text-align:left"))
        self.btn_last_as.setFlat(True)
        self.btn_last_as.setObjectName(_fromUtf8("btn_last_as"))
        self.verticalLayout_8.addWidget(self.btn_last_as)
        self.btn_email_as = QtGui.QPushButton(self.account)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_email_as.sizePolicy().hasHeightForWidth())
        self.btn_email_as.setSizePolicy(sizePolicy)
        self.btn_email_as.setFont(font)
        self.btn_email_as.setStyleSheet(_fromUtf8("Text-align:left"))
        self.btn_email_as.setFlat(True)
        self.btn_email_as.setObjectName(_fromUtf8("btn_email_as"))
        self.verticalLayout_8.addWidget(self.btn_email_as)
        self.btn_pass_as = QtGui.QPushButton(self.account)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_pass_as.sizePolicy().hasHeightForWidth())
        self.btn_pass_as.setSizePolicy(sizePolicy)
        self.btn_pass_as.setFont(font)
        self.btn_pass_as.setStyleSheet(_fromUtf8("Text-align:left"))
        self.btn_pass_as.setFlat(True)
        self.btn_pass_as.setObjectName(_fromUtf8("btn_pass_as"))
        self.verticalLayout_8.addWidget(self.btn_pass_as)
        self.btn_propic_as = QtGui.QPushButton(self.account)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_propic_as.sizePolicy().hasHeightForWidth())
        self.btn_propic_as.setSizePolicy(sizePolicy)
        self.btn_propic_as.setFont(font)
        self.btn_propic_as.setStyleSheet(_fromUtf8("Text-align:left"))
        self.btn_propic_as.setFlat(True)
        self.btn_propic_as.setObjectName(_fromUtf8("btn_propic_as"))
        self.verticalLayout_8.addWidget(self.btn_propic_as)
        self.btn_logout_as = QtGui.QPushButton(self.account)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_pass_as.sizePolicy().hasHeightForWidth())
        self.btn_logout_as.setSizePolicy(sizePolicy)
        self.btn_logout_as.setFont(font)
        self.btn_logout_as.setStyleSheet(_fromUtf8("Text-align:left"))
        self.btn_logout_as.setFlat(True)
        self.btn_logout_as.setObjectName(_fromUtf8("btn_logout_as"))
        self.verticalLayout_8.addWidget(self.btn_logout_as)
        self.gridLayout_5.addLayout(self.verticalLayout_8, 2, 1, 1, 1)
        self.verticalLayout_7 = QtGui.QVBoxLayout()
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem61 = QtGui.QSpacerItem(68, 130, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem61)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.l_propic_as = QtGui.QLabel(self.account)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.l_propic_as.sizePolicy().hasHeightForWidth())
        self.l_propic_as.setSizePolicy(sizePolicy)
        self.l_propic_as.setStyleSheet(_fromUtf8(""))
        self.l_propic_as.setFrameShape(QtGui.QFrame.NoFrame)
        self.l_propic_as.setFrameShadow(QtGui.QFrame.Raised)
        self.l_propic_as.setLineWidth(2)
        self.l_propic_as.setTextFormat(QtCore.Qt.RichText)
        self.l_propic_as.setObjectName(_fromUtf8("l_propic_as"))
        self.horizontalLayout_4.addWidget(self.l_propic_as)
        spacerItem62 = QtGui.QSpacerItem(138, 118, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem62)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)
        self.verticalLayout_7.addLayout(self.horizontalLayout_5)
        spacerItem63 = QtGui.QSpacerItem(418, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_7.addItem(spacerItem63)
        self.gridLayout_5.addLayout(self.verticalLayout_7, 1, 0, 1, 3)
        spacerItem64 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem64, 0, 0, 1, 1)
        self.stackedWidget_2.addWidget(self.account)
#--------------------------------------------------------------------------------------------------------------------------#        
#--------------------------------------------------------------------------------------------------------------------------#
        self.change_settings = QtGui.QWidget()
        self.change_settings.setObjectName(_fromUtf8("change_settings"))
        self.gridLayout_6 = QtGui.QGridLayout(self.change_settings)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.gridLayout_6.setContentsMargins(0,0,0,0)
        self.verticalLayout_10 = QtGui.QVBoxLayout()
        self.verticalLayout_10.setObjectName(_fromUtf8("verticalLayout_10"))
        spacerItem65 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_10.addItem(spacerItem65)
        spacerItem66 = QtGui.QSpacerItem(498, 228, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_10.addItem(spacerItem66)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        spacerItem67 = QtGui.QSpacerItem(28, 88, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem67)
        self.verticalLayout_9 = QtGui.QVBoxLayout()
        self.verticalLayout_9.setObjectName(_fromUtf8("verticalLayout_9"))
        self.label_3 = QtGui.QLabel(self.change_settings)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_9.addWidget(self.label_3)
        self.le_new_name = QtGui.QLineEdit(self.change_settings)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_new_name.sizePolicy().hasHeightForWidth())
        self.le_new_name.setSizePolicy(sizePolicy)
        font.setFamily(_fromUtf8("Comic Sans MS"))
        font.setPointSize(10)
        self.le_new_name.setFont(font)
        self.le_new_name.setStyleSheet(_fromUtf8("background-color: rgb(222, 209, 193);"))
        self.le_new_name.setObjectName(_fromUtf8("le_new_name"))
        self.verticalLayout_9.addWidget(self.le_new_name)
        self.btn_done_as = QtGui.QPushButton(self.change_settings)
        self.btn_cancle_as = QtGui.QPushButton(self.change_settings)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_done_as.sizePolicy().hasHeightForWidth())
        self.btn_done_as.setSizePolicy(sizePolicy)
        self.btn_cancle_as.setSizePolicy(sizePolicy)
        font = self.generate_font(family = "Ubuntu Condensed",point_size = 11)
        #font.setWeight(50)
        self.btn_done_as.setFont(font)
        self.btn_cancle_as.setFont(font)
        self.btn_done_as.setStyleSheet(_fromUtf8("background-color: rgb(69, 142, 255);"))
        self.btn_done_as.setAutoRepeat(False)
        self.btn_cancle_as.setStyleSheet(_fromUtf8("background-color: rgb(69, 142, 255);"))
        self.btn_cancle_as.setAutoRepeat(False)
        self.btn_done_as.setObjectName(_fromUtf8("btn_done_as"))
        self.btn_cancle_as.setObjectName(_fromUtf8("btn_cancle_as"))
        self.verticalLayout_9.addWidget(self.btn_done_as)
        self.verticalLayout_9.addWidget(self.btn_cancle_as)
        self.horizontalLayout_6.addLayout(self.verticalLayout_9)
        spacerItem68 = QtGui.QSpacerItem(198, 88, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem68)
        self.verticalLayout_10.addLayout(self.horizontalLayout_6)
        self.gridLayout_6.addLayout(self.verticalLayout_10, 0, 0, 1, 1)
        self.stackedWidget_2.addWidget(self.change_settings)
#----------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------#        
        self.scout = QtGui.QWidget()
        self.scout.setObjectName(_fromUtf8("scout"))
        self.gridLayout_10 = QtGui.QGridLayout(self.scout)
        self.gridLayout_10.setObjectName(_fromUtf8("gridLayout_10"))
        self.gridLayout_10.setContentsMargins(0,0,0,0)
        self.scrollArea_4 = QtGui.QScrollArea(self.scout)
        self.scrollArea_4.setWidgetResizable(True)
        self.scrollArea_4.setObjectName(_fromUtf8("scrollArea_4"))
        self.scrollArea_4.setFrameShape(QtGui.QFrame.NoFrame)
        self.scrollArea_4.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea_4.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollAreaWidgetContents_4 = QtGui.QWidget()
        self.scrollAreaWidgetContents_4.setGeometry(QtCore.QRect(0, 0, 498, 355))
        self.scrollAreaWidgetContents_4.setObjectName(_fromUtf8("scrollAreaWidgetContents_4"))
        self.verticalLayout_23 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents_4)
        self.verticalLayout_23.setObjectName(_fromUtf8("verticalLayout_25"))
        self.scrollArea_4.setWidget(self.scrollAreaWidgetContents_4)
        self.gridLayout_10.addLayout(self.verticalLayout_23, 0, 0, 1, 1)
        self.stackedWidget_2.addWidget(self.scout)      
        
        self.gridLayout_10.addWidget(self.scrollArea_4)
        
#----------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------------#
        self.page = QtGui.QWidget()
        self.page.setObjectName(_fromUtf8("page"))
        self.stackedWidget_2.addWidget(self.page)
        self.gridLayout_4.addWidget(self.stackedWidget_2, 0, 0, 1, 7)
        self.stackedWidget_2.raise_()
        self.btn_feed.raise_()
        self.line_2.raise_()
        self.btn_find_people.raise_()
        self.btn_post.raise_()
        self.btn_frnd_req.raise_()
        self.btn_account.raise_()
        self.stackedWidget.addWidget(self.home_page)
        self.gridLayout_2.addWidget(self.stackedWidget, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.copro)

        self.variable_assets()
        
        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget_2.setCurrentIndex(0)
        self.clicked()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
#---------------------------------------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------------------------------------#

    def variable_assets(self):
        self.feed = []
        self.page_elements = {}
        self.search_result = []
        self.page_elements_fr = {}
        self.req_list = []

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.le_email.setPlaceholderText(_translate("MainWindow", "email", None))
        self.le_password.setPlaceholderText(_translate("MainWindow", "password", None))
        self.btn_login.setText(_translate("MainWindow", "LOGIN", None))
        self.label.setText(_translate("MainWindow", "Don\'t have an account? ", None))
        self.btn_sign_up.setText(_translate("MainWindow", "Sign Up", None))
        self.le_first_su.setPlaceholderText(_translate("MainWindow", "first name", None))
        self.le_last_su.setPlaceholderText(_translate("MainWindow", "last name", None))
        self.le_email_su.setPlaceholderText(_translate("MainWindow", "email", None))
        self.le_pass_su.setPlaceholderText(_translate("MainWindow", "password", None))
        self.btn_sign_up_su.setText(_translate("MainWindow", "Sign Up", None))
        self.label_2.setText(_translate("MainWindow", "Changed your mind?", None))
        self.btn_back_su.setText(_translate("MainWindow", "Back", None))
        self.le_search.setPlaceholderText(_translate("MainWindow", "find people", None))
        self.btn_find_people.setIcon(QtGui.QIcon("default_icons/search.png"))
        self.btn_find_people.setIconSize(QtCore.QSize(33,33))
        self.btn_frnd_req.setIcon(QtGui.QIcon("default_icons/friend_req.png"))
        self.btn_frnd_req.setIconSize(QtCore.QSize(42,42))
        self.btn_search.setIcon(QtGui.QIcon("default_icons/confirm.png"))
        self.btn_search.setIconSize(QtCore.QSize(24,24))
        self.btn_account.setIcon(QtGui.QIcon("default_icons/acc.png"))
        self.btn_account.setIconSize(QtCore.QSize(41,41))
        self.btn_feed.setIcon(QtGui.QIcon("default_icons/feed.png"))
        self.btn_feed.setIconSize(QtCore.QSize(35,35))
        self.btn_post.setIcon(QtGui.QIcon("default_icons/post.png"))
        self.btn_post.setIconSize(QtCore.QSize(45,45))
        self.btn_clear.setIcon(QtGui.QIcon("default_icons/clear.png"))
        self.btn_clear.setIconSize(QtCore.QSize(26,26))
        self.label_4.setText(_translate("MainWindow", "Account", None))
        self.btn_first_as.setText(_translate("MainWindow", "Change Frist name", None))
        self.btn_last_as.setText(_translate("MainWindow", "Change Last name", None))
        self.btn_email_as.setText(_translate("MainWindow", "Change Email", None))
        self.btn_pass_as.setText(_translate("MainWindow", "Change Password", None))
        self.btn_propic_as.setText(_translate("MainWindow", "Change Profile picture", None))
        self.btn_logout_as.setText(_translate("MainWindow", "Logout", None))
        self.label_3.setText(_translate("MainWindow", "TextLabel", None))
        self.le_new_name.setPlaceholderText(_translate("MainWindow", "enter new name", None))
        self.btn_done_as.setText(_translate("MainWindow", "Done", None))
        self.btn_cancle_as.setText("Cancle")

    def clicked(self):
        self.btn_sign_up.clicked.connect(lambda:self.change_page(first = 1))
        self.btn_back_su.clicked.connect(lambda:self.change_page(first = 0))
        self.btn_sign_up_su.clicked.connect(lambda:self.create_account())
        self.btn_login.clicked.connect(lambda:self.login())
        self.btn_feed.clicked.connect(lambda:self.feed_page())
        self.btn_find_people.clicked.connect(lambda:self.change_to_search_page())
        self.btn_frnd_req.clicked.connect(lambda:self.fetch_req())
        self.btn_account.clicked.connect(lambda:self.change_page(second = 3))
        self.btn_first_as.clicked.connect(lambda:self.account_settings(flag = 0))
        self.btn_last_as.clicked.connect(lambda:self.account_settings(flag = 1))
        self.btn_email_as.clicked.connect(lambda:self.account_settings(flag = 2))
        self.btn_pass_as.clicked.connect(lambda:self.account_settings(flag = 3))
        self.btn_propic_as.clicked.connect(lambda:self.change_propic())
        self.btn_done_as.clicked.connect(lambda:self.change_settings_page())  
        self.btn_cancle_as.clicked.connect(lambda:self.cancle())
        self.btn_logout_as.clicked.connect(lambda:self.logout())
        self.btn_search.clicked.connect(lambda:self.search())
        self.btn_clear.clicked.connect(lambda:self.clear(self.verticalLayout_11,flag="search"))
        self.btn_post.clicked.connect(lambda:self.post_image())      

    def logout(self):
        client.logout(self.user_detail["email"])
        self.user_detail = {}
        self.search_result = []
        self.sent = []
        self.req_list = []
        self.feed = []
        self.le_search.clear()
        self.clear(self.verticalLayout_22)
        self.clear(self.verticalLayout_11)
        self.change_page(first = 0 , second = 0)
        

    def change_page(self,first = None,second = None):
        if first is not None:
            self.stackedWidget.setCurrentIndex(first)
        if second is not None:
            self.stackedWidget_2.setCurrentIndex(second)
    
    def cancle(self):
        self.le_new_name.clear()
        self.change_page(second = 3)

    def create_account(self):
        self.loading_icon_su = self.generate_loading_icon("default_icons/loading_small.gif")
        self.verticalLayout_2.addLayout(self.loading_icon_su)

        self.btn_back_su.setEnabled(False)
        self.btn_sign_up_su.setEnabled(False)

        self.thread_create_account = create_account_thread(self.le_first_su.text(),
                                                            self.le_last_su.text(),
                                                            self.le_email_su.text(),
                                                            self.le_pass_su.text())
        self.thread_create_account.start()
        self.thread_create_account.signal.connect(self.create_account_message)

    def create_account_message(self,status):
        
        self.btn_back_su.setEnabled(True)
        self.btn_sign_up_su.setEnabled(True)
        if status == -1:
            self.message_box("sign up","connection refused by server")
        elif status == 0:
            self.message_box("Sign up","Email already exist")    
        elif status ==1 :
            self.message_box("Sign up","Sign up sucessful")
            self.le_first_su.clear()
            self.le_last_su.clear()
            self.le_email_su.clear()
            self.le_pass_su.clear()
            self.change_page(first = 0)
        self.clear(self.loading_icon_su)

    def login(self):
        
        self.btn_sign_up.setEnabled(False)
        self.btn_login.setEnabled(False)
        
        self.loading_icon_login = self.generate_loading_icon("default_icons/loading_small.gif")
        self.verticalLayout.insertLayout(4,self.loading_icon_login)

        self.thread_login = login_thread(self.le_email.text(),self.le_password.text())
        self.thread_login.start()
        self.thread_login.signal.connect(self.login_message)
        self.thread_login.signal_error.connect(self.login_message)

    def login_message(self,user_detail):
        self.user_detail = user_detail
        self.btn_sign_up.setEnabled(True)
        self.btn_login.setEnabled(True)
        
        if self.user_detail == 0:
            self.message_box("Login" , "Wrong email")
        elif self.user_detail == 1:
            self.message_box("Login","Wrong email or password")
        elif self.user_detail == -1:
            self.message_box("Login","Connection refused by server")
        else:
            self.le_email.clear()
            self.le_password.clear()
            self.l_propic_as.setPixmap(QtGui.QPixmap(self.user_detail["propic"]))
            self.feed_page()
        self.clear(self.loading_icon_login)

    def post_image(self):
        image = QtGui.QFileDialog.getOpenFileName()
        return_value = client.upload_feed(image,self.user_detail["email"])
        if return_value == 0:
            self.message_box("upload feed","only jpg file format is supported")
        self.feed_page()
        

    def account_settings(self,flag = None):
        if flag ==0:
            self.le_new_name.setPlaceholderText("enter new first name")
            self.label_3.setText(self.user_detail["first"])
            self.flag = 0
        elif flag ==1:    
            self.le_new_name.setPlaceholderText("enter new last name")
            self.label_3.setText(self.user_detail["last"])
            self.flag = 1
        elif flag ==2:    
            self.le_new_name.setPlaceholderText("enter new email")
            self.label_3.setText(self.user_detail["email"])
            self.flag = 2
        elif flag ==3:    
            self.le_new_name.setPlaceholderText("enter new password")
            self.label_3.setText(self.user_detail["password"])
            self.flag = 3
        self.change_page(second = 4)
    
    def change_settings_page(self):
        return_signal = client.account_settings(self.flag,self.le_new_name.text(),self.user_detail)
        if return_signal == 0:
            self.message_box("accountsettings","email alredy exist")
            return None
        self.user_detail = return_signal
        self.le_new_name.clear()
        self.change_page(second = 3)

    def change_propic(self):
        propic = QtGui.QFileDialog.getOpenFileName()
        rescaled_propic = client.change_propic(propic,self.user_detail["email"])
        if rescaled_propic == 0:
            self.message_box("account settings","image format not supported")
        elif rescaled_propic is 1:
            self.l_propic_as.setPixmap(QtGui.QPixmap(self.user_detail["propic"]))

    def clear(self,layout,flag=None):  
        while layout.count():
            item = layout.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()
            elif item.layout() is not None:
                self.clear(item.layout())
        if flag=='search':
            self.change_to_search_page()

    def change_to_search_page(self):
        self.change_page(second=1)
        if self.verticalLayout_11.count() == 0:
            flag_location = "default_icons/search_flag.png"
            flag = self.generate_flag(flag_location = flag_location)
            self.verticalLayout_11.addLayout(flag)

    def search(self):
        self.thread_search = search_thread(self.le_search.text(),self.user_detail["email"])
        self.thread_search.start()
        self.thread_search.signal.connect(self.search_page)
        self.thread_search.signal_error.connect(self.search_page)

        self.clear(self.verticalLayout_11)
        loading = self.generate_loading_icon("default_icons/loading.gif")
        self.verticalLayout_11.addLayout(loading)

    def search_page(self,details):
        self.clear(self.verticalLayout_11)
        if details == "Connection refused by server":
            flag_location = "default_icons/connection_refused.png"
            flag = self.generate_flag(flag_location)
            self.verticalLayout_11.addLayout(flag)
            return

        self.search_result = details[0]
        self.friend_list = details[1]
        self.sent = details[2]
        self.page_elements = {}

        if self.search_result == ():
            flag = self.generate_flag(flag_text = 'no result found')
            self.verticalLayout_11.addLayout(flag)
        
        for i,result in enumerate(self.search_result):
            self.page_elements["li_fp"+str(i)] = QtGui.QLabel(self.scrollAreaWidgetContents)
            self.page_elements["ln_fp"+str(i)] = QtGui.QPushButton(self.scrollAreaWidgetContents)
            self.page_elements["btn_fr_fp"+str(i)] = QtGui.QPushButton(self.scrollAreaWidgetContents)
            self.page_elements["horizantalLayout_fp"+str(i)] = QtGui.QHBoxLayout()
            self.page_elements["horizantalLayout_fp"+str(i)].setObjectName(_fromUtf8("horizantalLayout_fp"+str(i)))
            self.page_elements["verticalLayout_fp"+str(i)] = QtGui.QVBoxLayout()
            self.page_elements["verticalLayout_fp"+str(i)].setObjectName(_fromUtf8("verticalLayout_fp"+str(i)))
            sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.page_elements["li_fp"+str(i)].sizePolicy().hasHeightForWidth())
            self.page_elements["li_fp"+str(i)].setSizePolicy(sizePolicy)
            self.page_elements["li_fp"+str(i)].setText(_fromUtf8(""))
            self.page_elements["li_fp"+str(i)].setObjectName(_fromUtf8("li_fp"+str(i)))
            self.page_elements["horizantalLayout_fp"+str(i)].addWidget(self.page_elements["li_fp"+str(i)])
            self.page_elements["ln_fp"+str(i)].setObjectName(_fromUtf8("ln_fp"+str(i)))
            self.page_elements["ln_fp"+str(i)].setFlat(True)
            self.page_elements["ln_fp"+str(i)].setStyleSheet("Text-align:left")
            sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(1)
            sizePolicy.setVerticalStretch(1)
            sizePolicy.setHeightForWidth( self.page_elements["ln_fp"+str(i)].sizePolicy().hasHeightForWidth())
            self.page_elements["ln_fp"+str(i)].setSizePolicy(sizePolicy)
            font = self.generate_font(family = "Ubuntu Condensed",point_size = 12)
            #font.setKerning(True)
            self.page_elements["ln_fp"+str(i)].setFont(font)
            self.page_elements["verticalLayout_fp"+str(i)].addWidget( self.page_elements["ln_fp"+str(i)])
            self.page_elements["btn_fr_fp"+str(i)].setStyleSheet(_fromUtf8("Text-align:left"))
            sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.page_elements["btn_fr_fp"+str(i)].sizePolicy().hasHeightForWidth())
            self.page_elements["btn_fr_fp"+str(i)].setSizePolicy(sizePolicy)
            self.page_elements["btn_fr_fp"+str(i)].setFlat(True)
            self.page_elements["btn_fr_fp"+str(i)].setIcon(QtGui.QIcon("default_icons/accept.png"))
            self.page_elements["btn_fr_fp"+str(i)].setIconSize(QtCore.QSize(20,20))
            self.page_elements["btn_fr_fp"+str(i)].setObjectName(_fromUtf8("btn_fr_fp"+str(i)))
            font.setPointSize(11)
            self.page_elements["btn_fr_fp"+str(i)].setFont(font)
            self.page_elements["btn_fr_fp"+str(i)].clicked.connect(
                partial(self.send_frnd_req,self.page_elements["btn_fr_fp"+str(i)],result))

            self.page_elements["verticalLayout_fp"+str(i)].addWidget(self.page_elements["btn_fr_fp"+str(i)])
            self.page_elements["horizantalLayout_fp"+str(i)].addLayout(self.page_elements["verticalLayout_fp"+str(i)])
            self.verticalLayout_11.insertLayout(0,self.page_elements["horizantalLayout_fp"+str(i)])
            if str(result[2]) not in self.friend_list and str(result[2]) not in self.sent:
                self.page_elements["btn_fr_fp"+str(i)].setText("send request")
            elif str(result[2]) in self.friend_list and str(result[2]) not in self.sent:
                self.page_elements["btn_fr_fp"+str(i)].setText("Already Friend")
                self.page_elements["btn_fr_fp"+str(i)].setEnabled(False)
            elif str(result[2]) in self.sent and str(result[2]) not in self.friend_list:
                self.page_elements["btn_fr_fp"+str(i)].setText("Request Already Sent")
                self.page_elements["btn_fr_fp"+str(i)].setEnabled(False)

            fullname = result[0]+" "+result[1]
            self.page_elements["ln_fp"+str(i)].setText(result[0]+" "+result[1])
            self.page_elements["ln_fp"+str(i)].clicked.connect(partial(self.scout_page,(result[4],result[2],fullname)))
            self.page_elements["li_fp"+str(i)].setPixmap(QtGui.QPixmap(result[3]))
            self.page_elements["line_search"+str(i)] = QtGui.QFrame(self.scrollAreaWidgetContents)
            self.page_elements["line_search"+str(i)].setFrameShape(QtGui.QFrame.HLine)
            self.page_elements["line_search"+str(i)].setFrameShadow(QtGui.QFrame.Raised)
            self.page_elements["line_search"+str(i)].setLineWidth(2)
            self.page_elements["line_search"+str(i)].setObjectName(_fromUtf8("line_search"+str(i)))
            self.verticalLayout_11.insertWidget(1,self.page_elements["line_search"+str(i)])
        
        self.spacerItem_fp = QtGui.QSpacerItem(15, 10, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_11.addItem(self.spacerItem_fp)

    def send_frnd_req(self,button,result):
        button.setText("Friend Request sent")
        button.setEnabled(False)
        self.send_req = threading.Thread(target = client.send_frnd_req,args = (self.user_detail["email"],result[2]))
        self.send_req.start()
        self.send_req.setDaemon = True

    def fetch_req(self):
            self.change_page(second = 2)
            
            self.thread_friend = friend_thread(self.user_detail["email"])
            self.thread_friend.start()

            loading = self.generate_loading_icon("default_icons/loading.gif")
            self.clear(self.verticalLayout_12)
            self.verticalLayout_12.addLayout(loading)
            
            self.thread_friend.signal.connect(self.friend_req)
            self.thread_friend.signal_error.connect(self.friend_req)

    def friend_req(self,req_list):
        self.clear(self.verticalLayout_12)
        self.req_list = req_list
        self.page_elements_fr = {}
        
        if req_list == "Connection refused by server":
            flag_location = "default_icons/connection_refused.png"
            flag = self.generate_flag(flag_location)
            self.verticalLayout_12.addLayout(flag)
            return

        if self.req_list == []:
            flag_location = "default_icons/friend_flag.png"
            flag = self.generate_flag(flag_location = flag_location)
            self.verticalLayout_12.addLayout(flag)
            return
        
        for i,request in enumerate(self.req_list):
            request_detail = request.split(" ")
            self.page_elements_fr["l_fr"+str(i)] = QtGui.QLabel(self.scrollAreaWidgetContents_2)
            self.page_elements_fr["ln_fr"+str(i)] = QtGui.QPushButton(self.scrollAreaWidgetContents_2)
            self.page_elements_fr["btn_fr"+str(i)] = QtGui.QPushButton(self.scrollAreaWidgetContents_2)
            self.page_elements_fr["btn_fr_reject"+str(i)] = QtGui.QPushButton(self.scrollAreaWidgetContents_2)
            self.page_elements_fr["horizantalLayout_fr"+str(i)] = QtGui.QHBoxLayout()
            self.page_elements_fr["horizantalLayout_fr"+str(i)].setObjectName(_fromUtf8("horizantalLayout_fr"+str(i)))
            self.page_elements_fr["verticalLayout_fr"+str(i)] = QtGui.QVBoxLayout()
            self.page_elements_fr["verticalLayout_fr"+str(i)].setObjectName(_fromUtf8("verticalLayout_fr"+str(i)))
            self.page_elements_fr["horizontalLayout_response"+str(i)] = QtGui.QHBoxLayout()
            self.page_elements_fr["horizontalLayout_response"+str(i)].setObjectName(_fromUtf8("horizontalLayout_response"+str(i)))
            sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(1)
            sizePolicy.setVerticalStretch(1)
            sizePolicy.setHeightForWidth(self.page_elements_fr["l_fr"+str(i)].sizePolicy().hasHeightForWidth())
            self.page_elements_fr["l_fr"+str(i)].setSizePolicy(sizePolicy)
            self.page_elements_fr["l_fr"+str(i)].setText(_fromUtf8(""))
            self.page_elements_fr["l_fr"+str(i)].setObjectName(_fromUtf8("l_fr"+str(i)))
            self.page_elements_fr["horizantalLayout_fr"+str(i)].addWidget(self.page_elements_fr["l_fr"+str(i)])
            self.page_elements_fr["ln_fr"+str(i)].setStyleSheet("Text-align:left")
            self.page_elements_fr["ln_fr"+str(i)].setFlat(True)
            fullname = request_detail[0]+" "+request_detail[1]
            self.page_elements_fr["ln_fr"+str(i)].clicked.connect(partial(self.scout_page,(request_detail[4],request_detail[2],fullname)))
            self.page_elements_fr["ln_fr"+str(i)].setObjectName(_fromUtf8("ln_fr"+str(i)))
            sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth( self.page_elements_fr["ln_fr"+str(i)].sizePolicy().hasHeightForWidth())
            self.page_elements_fr["ln_fr"+str(i)].setSizePolicy(sizePolicy)
            font = self.generate_font(family = "Ubuntu Condensed", point_size = 12,kerning = True)
            self.page_elements_fr["ln_fr"+str(i)].setFont(font)
            self.page_elements_fr["verticalLayout_fr"+str(i)].addWidget( self.page_elements_fr["ln_fr"+str(i)])
            self.page_elements_fr["btn_fr"+str(i)].setStyleSheet(_fromUtf8("Text-align:left"))
            self.page_elements_fr["btn_fr_reject"+str(i)].setStyleSheet(_fromUtf8("Text-align:left"))
            sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.page_elements_fr["btn_fr"+str(i)].sizePolicy().hasHeightForWidth())
            self.page_elements_fr["btn_fr"+str(i)].setSizePolicy(sizePolicy)
            self.page_elements_fr["btn_fr"+str(i)].setFlat(True)
            self.page_elements_fr["btn_fr"+str(i)].setObjectName(_fromUtf8("btn_fr"+str(i)))
            self.page_elements_fr["btn_fr_reject"+str(i)].setSizePolicy(sizePolicy)
            self.page_elements_fr["btn_fr_reject"+str(i)].setFlat(True)
            self.page_elements_fr["btn_fr_reject"+str(i)].setObjectName(_fromUtf8("btn_fr_reject"+str(i)))
            font.setPointSize(11)
            self.page_elements_fr["btn_fr"+str(i)].setFont(font)
            self.page_elements_fr["btn_fr_reject"+str(i)].setFont(font)
            self.page_elements_fr["btn_fr"+str(i)].clicked.connect(partial(self.accept_frnd_req,
            (self.page_elements_fr["btn_fr"+str(i)],request,self.page_elements_fr["btn_fr_reject"+str(i)])))
            self.page_elements_fr["btn_fr_reject"+str(i)].clicked.connect(partial(self.reject_frnd_req,
            (self.page_elements_fr["btn_fr"+str(i)],request,self.page_elements_fr["btn_fr_reject"+str(i)])))
            self.page_elements_fr["horizontalLayout_response"+str(i)].addWidget(self.page_elements_fr["btn_fr"+str(i)])
            self.page_elements_fr["horizontalLayout_response"+str(i)].addWidget(self.page_elements_fr["btn_fr_reject"+str(i)])
            self.page_elements_fr["spacerItem_response"+str(i)] = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
            self.page_elements_fr["horizontalLayout_response"+str(i)].addItem(self.page_elements_fr["spacerItem_response"+str(i)])
            self.page_elements_fr["verticalLayout_fr"+str(i)].addLayout(self.page_elements_fr["horizontalLayout_response"+str(i)])
            self.page_elements_fr["horizantalLayout_fr"+str(i)].addLayout(self.page_elements_fr["verticalLayout_fr"+str(i)])
            self.verticalLayout_12.insertLayout(0,self.page_elements_fr["horizantalLayout_fr"+str(i)])
            self.page_elements_fr["btn_fr"+str(i)].setIcon(QtGui.QIcon("default_icons/accept.png"))
            self.page_elements_fr["btn_fr"+str(i)].setIconSize(QtCore.QSize(20,20))
            self.page_elements_fr["btn_fr"+str(i)].setText("Accept request")
            self.page_elements_fr["btn_fr_reject"+str(i)].setIcon(QtGui.QIcon("default_icons/reject.png"))
            self.page_elements_fr["btn_fr_reject"+str(i)].setIconSize(QtCore.QSize(18,18))
            self.page_elements_fr["btn_fr_reject"+str(i)].setText("reject request")
            self.page_elements_fr["ln_fr"+str(i)].setText(request_detail[0]+" "+request_detail[1])
            self.page_elements_fr["l_fr"+str(i)].setPixmap(QtGui.QPixmap(request_detail[3]))
            self.page_elements_fr["line_fr"+str(i)] = QtGui.QFrame(self.scrollAreaWidgetContents_2)
            self.page_elements_fr["line_fr"+str(i)].setFrameShape(QtGui.QFrame.HLine)
            self.page_elements_fr["line_fr"+str(i)].setFrameShadow(QtGui.QFrame.Raised)
            self.page_elements_fr["line_fr"+str(i)].setLineWidth(2)
            self.page_elements_fr["line_fr"+str(i)].setObjectName(_fromUtf8("line_fr"+str(i)))
            self.verticalLayout_12.insertWidget(1,self.page_elements_fr["line_fr"+str(i)])
        
        spacerItem_fr = QtGui.QSpacerItem(15, 10, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_12.addItem(spacerItem_fr)
    
    def accept_frnd_req(self,args):
        button_accept,request,button_reject = args
        button_accept.setText("Request Accepted")
        button_accept.setEnabled(False)
        button_reject.setEnabled(False)
        self.req_list.remove(request)
        request = request.split(" ")
        client.accept_req(request[2] ,self.req_list,self.user_detail["id"])

    def reject_frnd_req(self,args):
        button_accept,request,button_reject = args
        button_reject.setText("Request Rejected")
        button_reject.setEnabled(False)
        button_accept.setEnabled(False)
        self.req_list.remove(request)
        new_req_list = (" ").join(self.req_list)
        request = request.split(' ')
        client.reject_request(self.user_detail["id"],new_req_list,request[2])


    def feed_page(self):
        self.change_page(first = 2,second = 0)
        self.clear(self.verticalLayout_22)
        
        loading = self.generate_loading_icon("default_icons/loading.gif")
        self.verticalLayout_22.addLayout(loading)
        

        self.thread_feed = feed_thread(self.user_detail["email"])
        self.thread_feed.start()
        self.thread_feed.signal.connect(self.display_feed)
        self.thread_feed.signal_error.connect(self.display_feed)
        

    def display_feed(self,feed):
        self.clear(self.verticalLayout_22)
        self.feed_page_elements = {}
        self.feed = feed
        if feed=='Connection refused by server':
            flag_text = 'Connection refused by server'
            flag_location = "default_icons/connection_refused.png"
            flag = self.generate_flag(flag_location)
            self.verticalLayout_22.addLayout(flag)
            return
        
        if self.feed==[]:
            flag_location = "default_icons/feed_flag.png"
            flag = self.generate_flag(flag_location = flag_location)
            self.verticalLayout_22.addLayout(flag)
            return   
        
        for i,feed_contents in enumerate(self.feed):
            self.feed_page_elements["horizontalLayout_feed"+str(i)] = QtGui.QHBoxLayout()
            self.feed_page_elements["horizontalLayout_feed"+str(i)].setObjectName(_fromUtf8("horizontalLayout_feed"+str(i)))
            self.feed_page_elements["feed_image"+str(i)] = QtGui.QLabel(self.scrollAreaWidgetContents_3)
            self.feed_page_elements["horizontalLayout_like"+str(i)] = QtGui.QHBoxLayout()
            self.feed_page_elements["horizontalLayout_like"+str(i)].setContentsMargins(-1, 0, -1, -1)
            self.feed_page_elements["horizontalLayout_like"+str(i)].setObjectName(_fromUtf8("horizontalLayout_like"+str(i)))
            self.feed_page_elements["btn_like"+str(i)] = QtGui.QPushButton(self.scrollAreaWidgetContents_3)
            self.feed_page_elements["time_stamp"+str(i)] = QtGui.QLabel(self.scrollAreaWidgetContents_3)
            self.feed_page_elements["time_stamp"+str(i)].setObjectName("time_stamp"+str(i))
            font = self.generate_font(family = "Ubuntu",point_size = 8)
            self.feed_page_elements["time_stamp"+str(i)].setFont(font)

            sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.feed_page_elements["btn_like"+str(i)].sizePolicy().hasHeightForWidth())
            self.feed_page_elements["btn_like"+str(i)].setSizePolicy(sizePolicy)
            self.feed_page_elements["btn_like"+str(i)].setText(_fromUtf8(""))
            self.feed_page_elements["btn_like"+str(i)].setFlat(True)
            self.feed_page_elements["btn_like"+str(i)].setObjectName(_fromUtf8("btn_like"+(str(i))))
            
            self.feed_page_elements["time_stamp"+str(i)].setText(self.get_time_difference(feed_contents[7]))

            self.feed_page_elements["horizontalLayout_like"+str(i)].addWidget(self.feed_page_elements["btn_like"+str(i)])
            self.feed_page_elements["l_count"+str(i)] = QtGui.QLabel(self.scrollAreaWidgetContents_3)
            self.feed_page_elements["l_count"+str(i)].setObjectName(_fromUtf8("l_count"+str(i)))
            font = self.generate_font(family = "Ubuntu Condensed",point_size = 13)
            self.feed_page_elements["l_count"+str(i)].setFont(font)
            self.feed_page_elements["l_count"+str(i)].setText(feed_contents[3])

            if str(self.user_detail["id"]) not in feed_contents[5]:
                self.feed_page_elements["btn_like"+str(i)].setIcon(QtGui.QIcon("default_icons/notLiked.png"))
                self.feed_page_elements["btn_like"+str(i)].setIconSize(QtCore.QSize(23,23))
                self.feed_page_elements["btn_like"+str(i)].clicked.connect(partial(self.like , 
                (self.feed_page_elements["btn_like"+str(i)],
                self.feed_page_elements["l_count"+str(i)],
                feed_contents[0],feed_contents[4],feed_contents[6],feed_contents[3],"like")))

            else:
                self.feed_page_elements["btn_like"+str(i)].setIcon(QtGui.QIcon("default_icons/liked.png"))
                self.feed_page_elements["btn_like"+str(i)].setIconSize(QtCore.QSize(23,23))
                self.feed_page_elements["btn_like"+str(i)].clicked.connect(partial(self.like , 
                (self.feed_page_elements["btn_like"+str(i)],
                self.feed_page_elements["l_count"+str(i)],
                feed_contents[0],feed_contents[4],feed_contents[6],feed_contents[3],"unlike")))
            self.feed_page_elements["horizontalLayout_like"+str(i)].addWidget(self.feed_page_elements["l_count"+str(i)])
            self.feed_page_elements["spacerItem"+str(i)] = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
            self.feed_page_elements["horizontalLayout_like"+str(i)].addItem(self.feed_page_elements["spacerItem"+str(i)])
            sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(1)
            sizePolicy.setVerticalStretch(1)
            sizePolicy.setHeightForWidth(self.feed_page_elements["feed_image"+str(i)].sizePolicy().hasHeightForWidth())
            self.feed_page_elements["feed_image"+str(i)].setSizePolicy(sizePolicy)
            self.feed_page_elements["feed_image"+str(i)].setObjectName(_fromUtf8("feed_image"+str(i)))
            self.feed_page_elements["feed_image"+str(i)].setPixmap(QtGui.QPixmap(feed_contents[2]))
            self.feed_page_elements["horizontalLayout_feed"+str(i)].addWidget(self.feed_page_elements["feed_image"+str(i)])
            self.feed_page_elements["feed_name"+str(i)] = QtGui.QPushButton(self.scrollAreaWidgetContents_3)
            sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.feed_page_elements["feed_name"+str(i)].sizePolicy().hasHeightForWidth())
            self.feed_page_elements["feed_name"+str(i)].setSizePolicy(sizePolicy)
            font.setPointSize(11)
            self.feed_page_elements["feed_name"+str(i)].setFont(font)
            self.feed_page_elements["feed_name"+str(i)].setText(feed_contents[1])
            self.feed_page_elements["feed_name"+str(i)].setStyleSheet("Text-align:left")
            self.feed_page_elements["feed_name"+str(i)].setFlat(True)
            self.feed_page_elements["feed_name"+str(i)].clicked.connect(partial(
                self.scout_page,
                (feed_contents[6],
                feed_contents[4],feed_contents[1])))
            self.feed_page_elements["feed_name"+str(i)].setObjectName(_fromUtf8("feed_name"+str(i)))
            self.feed_page_elements["horizontalLayout_feed"+str(i)].addWidget(self.feed_page_elements["feed_name"+str(i)])
            self.verticalLayout_22.insertLayout(0,self.feed_page_elements["horizontalLayout_feed"+str(i)])
            self.feed_page_elements["feed_content"+str(i)] = QtGui.QLabel(self.scrollAreaWidgetContents_3)
            sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.feed_page_elements["feed_content"+str(i)].sizePolicy().hasHeightForWidth())
            self.feed_page_elements["feed_content"+str(i)].setSizePolicy(sizePolicy)
            self.feed_page_elements["feed_content"+str(i)].setFont(font)
            self.feed_page_elements["feed_content"+str(i)].setObjectName(_fromUtf8("feed_content"+str(i)))
            self.feed_page_elements["feed_content"+str(i)].setPixmap(QtGui.QPixmap(feed_contents[0]))
            self.verticalLayout_22.insertWidget(1,self.feed_page_elements["feed_content"+str(i)])
            self.verticalLayout_22.insertLayout(2,self.feed_page_elements["horizontalLayout_like"+str(i)])
            self.feed_page_elements["line_feed"+str(i)] = QtGui.QFrame(self.scrollAreaWidgetContents_3)
            self.feed_page_elements["line_feed"+str(i)].setFrameShape(QtGui.QFrame.HLine)
            self.feed_page_elements["line_feed"+str(i)].setFrameShadow(QtGui.QFrame.Raised)
            self.feed_page_elements["line_feed"+str(i)].setLineWidth(2)
            self.feed_page_elements["line_feed"+str(i)].setObjectName(_fromUtf8("line_feed"+str(i)))
            self.verticalLayout_22.insertWidget(3,self.feed_page_elements["time_stamp"+str(i)])
            self.verticalLayout_22.insertWidget(4,self.feed_page_elements["line_feed"+str(i)])
        spacerItem_feed = QtGui.QSpacerItem(20, 13, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout_22.addItem(spacerItem_feed)
    
    def scout_page(self,details):
        self.change_page(second = 5)
        self.clear(self.verticalLayout_23)
        person_email,person_id,fullname = details
        
        self.thread_scout = scout_thread(self.user_detail['email'],person_email,person_id,fullname)
        self.thread_scout.start()
        self.thread_scout.signal.connect(self.display_scout)
        self.thread_scout.signal_error.connect(self.display_scout)

        loading_scout = self.generate_loading_icon("default_icons/loading.gif")
        self.verticalLayout_23.addLayout(loading_scout)

    def display_scout(self,details):
        self.clear(self.verticalLayout_23)
        
        if details == "Connection refused by server":
            flag_location = "default_icons/connection_refused.png"
            flag = self.generate_flag(flag_location = flag_location)
            self.verticalLayout_23.addLayout(flag)
            return

        images,likes,people_liked,propic,thumbnail,time_post,person_email,person_id,fullname = details
        self.horizontalLayout_13 = QtGui.QHBoxLayout()
        self.horizontalLayout_13.setObjectName(_fromUtf8("horizontalLayout_13"))
        spacerItem73 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem73)
        self.verticalLayout_16 = QtGui.QVBoxLayout()
        self.verticalLayout_16.setObjectName(_fromUtf8("verticalLayout_16"))
        self.l_propic_scout = QtGui.QLabel(self.scout)
        self.l_propic_scout.setText(_fromUtf8(""))
        self.l_propic_scout.setObjectName(_fromUtf8("l_propic_scout"))
        self.verticalLayout_16.addWidget(self.l_propic_scout)
        self.l_name_scout = QtGui.QLabel(self.scout)
        font = self.generate_font(family = "Ubuntu Condensed", point_size = 15, set_bold = True)
        self.l_name_scout.setFont(font)
        self.l_name_scout.setText(_fromUtf8(""))
        self.l_name_scout.setAlignment(QtCore.Qt.AlignCenter)
        self.l_name_scout.setObjectName(_fromUtf8("l_name_scout"))
        self.verticalLayout_16.addWidget(self.l_name_scout)
        self.horizontalLayout_13.addLayout(self.verticalLayout_16)
        spacerItem74 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem74)
        self.verticalLayout_23.addLayout(self.horizontalLayout_13)
        self.line_scout = QtGui.QFrame(self.scrollAreaWidgetContents_3)
        self.line_scout.setFrameShape(QtGui.QFrame.HLine)
        self.line_scout.setFrameShadow(QtGui.QFrame.Raised)
        self.line_scout.setLineWidth(2)
        self.line_scout.setObjectName(_fromUtf8("line_scout"))
        self.verticalLayout_23.insertWidget(1,self.line_scout)
        
        self.l_propic_scout.setPixmap(QtGui.QPixmap(propic))
        self.l_name_scout.setText(fullname)
        self.scout_ = [(image,like,people,time) for image,like,people,time in zip(images,likes,people_liked,time_post) ]
        self.scout_page_elements={}
        
        if self.scout_==[]:
            flag_location = "default_icons/feed_flag.png"
            flag = self.generate_flag(flag_location = flag_location)
            self.verticalLayout_23.addLayout(flag)
            return

        for i,scout_elements in enumerate(self.scout_):
            self.scout_page_elements["horizontal_layout_scout"+str(i)] = QtGui.QHBoxLayout()
            self.scout_page_elements["horizontal_layout_scout"+str(i)].setObjectName(_fromUtf8("horizontal_layout_scout"+str(i)))
            self.scout_page_elements["propic_scout"+str(i)] = QtGui.QLabel(self.scrollAreaWidgetContents_4)
            
            self.scout_page_elements["time_stamp"+str(i)] = QtGui.QLabel(self.scrollAreaWidgetContents_4)
            self.scout_page_elements["time_stamp"+str(i)].setObjectName("time_stamp"+str(i))
            self.scout_page_elements["time_stamp"+str(i)].setText(self.get_time_difference(scout_elements[3]))
            font = self.generate_font(family = "Ubuntu",point_size = 8)
            self.scout_page_elements["time_stamp"+str(i)].setFont(font)

            sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.scout_page_elements["propic_scout"+str(i)].sizePolicy().hasHeightForWidth())
            self.scout_page_elements["propic_scout"+str(i)].setSizePolicy(sizePolicy)
            self.scout_page_elements["propic_scout"+str(i)].setPixmap(QtGui.QPixmap(thumbnail))
            self.scout_page_elements["propic_scout"+str(i)].setObjectName(_fromUtf8("propic_scout"+str(i)))
            self.scout_page_elements["horizontal_layout_scout"+str(i)].addWidget(self.scout_page_elements["propic_scout"+str(i)])
            self.scout_page_elements["preson_name_scout"+str(i)] = QtGui.QLabel(self.scrollAreaWidgetContents_4)
            sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.scout_page_elements["preson_name_scout"+str(i)].sizePolicy().hasHeightForWidth())
            self.scout_page_elements["preson_name_scout"+str(i)].setText(fullname)
            self.scout_page_elements["preson_name_scout"+str(i)].setSizePolicy(sizePolicy)
            self.scout_page_elements["preson_name_scout"+str(i)].setObjectName("preson_name_scout"+str(i))
            font = self.generate_font(family = "Ubuntu Condensed",point_size = 11)
            self.scout_page_elements["preson_name_scout"+str(i)].setFont(font)
            self.scout_page_elements["horizontal_layout_scout"+str(i)].addWidget(self.scout_page_elements["preson_name_scout"+str(i)])
            self.verticalLayout_23.insertLayout(2,self.scout_page_elements["horizontal_layout_scout"+str(i)])
            self.scout_page_elements["l_feed_scout"+str(i)] = QtGui.QLabel(self.scrollAreaWidgetContents_4)
            sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
            sizePolicy.setHorizontalStretch(1)
            sizePolicy.setVerticalStretch(1)
            sizePolicy.setHeightForWidth(self.scout_page_elements["l_feed_scout"+str(i)].sizePolicy().hasHeightForWidth())
            self.scout_page_elements["l_feed_scout"+str(i)].setSizePolicy(sizePolicy)
            self.scout_page_elements["l_feed_scout"+str(i)].setPixmap(QtGui.QPixmap(scout_elements[0]))
            self.scout_page_elements["l_feed_scout"+str(i)].setObjectName(_fromUtf8("l_feed_scout"+str(i)))
            self.verticalLayout_23.insertWidget(3,self.scout_page_elements["l_feed_scout"+str(i)])
            self.scout_page_elements["horizontal_layout1"+str(i)] = QtGui.QHBoxLayout()
            self.scout_page_elements["horizontal_layout1"+str(i)].setSpacing(6)
            self.scout_page_elements["horizontal_layout1"+str(i)].setObjectName(_fromUtf8("horizontal_layout1"+str(i)))
            self.scout_page_elements["btn_like_scout"+str(i)] = QtGui.QPushButton(self.scrollAreaWidgetContents_4)
            sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.scout_page_elements["btn_like_scout"+str(i)].sizePolicy().hasHeightForWidth())
            self.scout_page_elements["btn_like_scout"+str(i)].setSizePolicy(sizePolicy)
            self.scout_page_elements["btn_like_scout"+str(i)].setText(_fromUtf8(""))
            self.scout_page_elements["btn_like_scout"+str(i)].setFlat(True)
            
            self.scout_page_elements["btn_like_scout"+str(i)].setObjectName(_fromUtf8("btn_like_scout"+str(i)))
            self.scout_page_elements["horizontal_layout1"+str(i)].addWidget(self.scout_page_elements["btn_like_scout"+str(i)])
            self.scout_page_elements["btn_count_scout"+str(i)] = QtGui.QLabel(self.scrollAreaWidgetContents_4)
            sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.scout_page_elements["btn_count_scout"+str(i)].sizePolicy().hasHeightForWidth())
            font = self.generate_font(family = "Ubuntu Condensed",point_size = 13)
            self.scout_page_elements["btn_count_scout"+str(i)].setFont(font)
            self.scout_page_elements["btn_count_scout"+str(i)].setSizePolicy(sizePolicy)
            self.scout_page_elements["btn_count_scout"+str(i)].setText(scout_elements[1])
            
            self.scout_page_elements["btn_count_scout"+str(i)].setObjectName(_fromUtf8("btn_count_scout"+str(i)))
            if str(self.user_detail["id"]) in scout_elements[2]:
                self.scout_page_elements["btn_like_scout"+str(i)].setIcon(QtGui.QIcon("default_icons/liked.png"))
                self.scout_page_elements["btn_like_scout"+str(i)].setIconSize(QtCore.QSize(23,23))
                self.scout_page_elements["btn_like_scout"+str(i)].clicked.connect(partial(self.like, (
                self.scout_page_elements["btn_like_scout"+str(i)],self.scout_page_elements["btn_count_scout"+str(i)],
                scout_elements[0],person_id,person_email,scout_elements[1],"unlike")))
            else:
                self.scout_page_elements["btn_like_scout"+str(i)].setIcon(QtGui.QIcon("default_icons/notLiked.png"))
                self.scout_page_elements["btn_like_scout"+str(i)].setIconSize(QtCore.QSize(23,23))
                self.scout_page_elements["btn_like_scout"+str(i)].clicked.connect(partial(self.like, (
                self.scout_page_elements["btn_like_scout"+str(i)],self.scout_page_elements["btn_count_scout"+str(i)],
                scout_elements[0],person_id,person_email,scout_elements[1],"like")))

            self.scout_page_elements["horizontal_layout1"+str(i)].addWidget(self.scout_page_elements["btn_count_scout"+str(i)])
            self.scout_page_elements["spacerItem_scout"+str(i)] = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
            self.scout_page_elements["horizontal_layout1"+str(i)].addItem(self.scout_page_elements["spacerItem_scout"+str(i)])
            self.verticalLayout_23.insertLayout(4,self.scout_page_elements["horizontal_layout1"+str(i)])
            self.scout_page_elements["line_scout"+str(i)] = QtGui.QFrame(self.scrollAreaWidgetContents_3)
            self.scout_page_elements["line_scout"+str(i)].setFrameShape(QtGui.QFrame.HLine)
            self.scout_page_elements["line_scout"+str(i)].setFrameShadow(QtGui.QFrame.Raised)
            self.scout_page_elements["line_scout"+str(i)].setLineWidth(2)
            self.scout_page_elements["line_scout"+str(i)].setObjectName(_fromUtf8("line_scout"+str(i)))
            self.verticalLayout_23.insertWidget(5,self.scout_page_elements["time_stamp"+str(i)])
            self.verticalLayout_23.insertWidget(6,self.scout_page_elements["line_scout"+str(i)])

    def like(self,details):
        button,like_count_lable,image,p_id,email,count,flag = details
        button.clicked.disconnect()
        button.setIcon(QtGui.QIcon("default_icons/liked.png"))
        button.setIconSize(QtCore.QSize(30,30))
        image = image.split('/')[-1]
        if flag=="like":
            button.setIcon(QtGui.QIcon("default_icons/liked.png"))
            button.setIconSize(QtCore.QSize(23,23))
            like_count = int(count)+1
            button.clicked.connect(partial(self.like , 
                (button,like_count_lable,image,p_id,email,like_count,"unlike")))
            self.like_thread = threading.Thread(target = client.like_unlike, args=(image,self.user_detail["id"],self.user_detail["email"],email,'like'))
            self.like_thread.start()
            self.like_thread.setDaemon = True

        elif flag=="unlike":
            button.setIcon(QtGui.QIcon("default_icons/notLiked.png"))
            button.setIconSize(QtCore.QSize(23,23))
            like_count = int(count)-1
            button.clicked.connect(partial(self.like , 
                (button,like_count_lable,image,p_id,email,like_count,"like")))
            self.like_thread = threading.Thread(target = client.like_unlike, args=(image,self.user_detail["id"],self.user_detail["email"],email,'unlike'))
            self.like_thread.start()
            self.like_thread.setDaemon = True
        
        like_count_lable.setText(str(like_count))

    def message_box(self,title,text):
        msg_box = QtGui.QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setStandardButtons(QtGui.QMessageBox.Ok)
        msg_box.exec_()

    def generate_loading_icon(self,icon_location):
        loading_icon = QtGui.QLabel()
        loading = QtGui.QMovie(icon_location)
        loading_icon.setMovie(loading)
        loading.start()
        horizontal_layout = QtGui.QHBoxLayout()
        spacer = QtGui.QSpacerItem(15,8,QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        spacer2 = QtGui.QSpacerItem(15,8,QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        horizontal_layout.addItem(spacer)
        horizontal_layout.addWidget(loading_icon)
        horizontal_layout.addItem(spacer2)
        return horizontal_layout

    def generate_font(self,family=None , point_size=None ,set_bold = False, kerning = False):
        font = QtGui.QFont()
        font.setFamily(family)
        font.setPointSize(point_size)
        font.setBold(set_bold)
        font.setKerning(kerning)
        return font

    def generate_flag(self,flag_location=None,flag_text = None):
        font = self.generate_font(family="Ubuntu",point_size=9)
        horizontal_layout = QtGui.QHBoxLayout()
        spacerItem = QtGui.QSpacerItem(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        lable = QtGui.QLabel()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(lable.sizePolicy().hasHeightForWidth())
        lable.setSizePolicy(sizePolicy)
        lable.setText(_fromUtf8(""))
        
        if flag_location!=None and flag_text==None:
            lable.setPixmap(QtGui.QPixmap(flag_location))
        if flag_text!=None and flag_location==None:
            lable.setFont(font)
            lable.setText(flag_text)
        
        horizontal_layout.addItem(spacerItem)
        horizontal_layout.addWidget(lable)
        return horizontal_layout

    def get_time_difference(self,time_post):
        time_diff = str(datetime.now()-time_post)
        if " " not in time_diff:
            time_diff = time_diff.split(":")
            if int(time_diff[0])!= 0: 
                return time_diff[0]+" hour ago"
            if int(time_diff[1])!= 0:
                if time_diff[1][0]=='0':
                    return time_diff[1][1]+" min ago"         
                return time_diff[1]+" min ago" 
            if time_diff[2].split('.')[0][0] == '0':
                return time_diff[2].split('.')[0][1]+" sec ago"
            return time_diff[2].split('.')[0]+" sec ago"
        else:
            time_diff = int(time_diff.split(" ")[0])
            if time_diff//365 > 0: 
                return str(time_diff//365)+" year ago"
            if time_diff//30 > 0:
                return str(time_diff//30)+" month ago"
            return str(time_diff)+" day ago"

if __name__ == "__main__":
    
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())