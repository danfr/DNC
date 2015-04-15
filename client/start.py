from view.main import Ui_MainWindow
from PyQt4 import QtGui, QtCore
from PySide.QtCore import *
from PySide.QtGui import *
import time, threading, datetime, time, random,re
from socket import *
from view.pmWindow import Ui_Dialog2
from view.pmFile import Ui_Dialog3
import configparser
import pydoc
from threading import *


#########################################################


##
# this class can receive files sent by p2p
# to run this class, we need to do :
#             s = StreamHandler(portFile, fileName)
#               s.start()
#


class StreamHandler (Thread):
    """
    this class can receive files sent by p2p
    to run this class, we need to do :
              s = StreamHandler(portFile, fileName)
              s.start()
    """
    def __init__(self, port, filename):
        """

        :param port: the port of the new connection
        :param filename: the name of the file you wish to receive
        :return:
        """

        Thread.__init__(self)
        self.port = port
        self.filename = filename

    def run(self):
        """
         Execute the process function
        :return:
        """
        self.process()

    def bindmsock(self):
        """
        creation of a new socket for the p2p transfert file
        :return:
        """
        self.msock = socket(AF_INET, SOCK_STREAM)
        self.msock.bind(('', int(self.port)))
        self.msock.listen(1)
        print('[Media] Listening on port'+self.port)

    def acceptmsock(self):
        """
        Get the address of the connection
        :return:
        """
        self.mconn, self.maddr = self.msock.accept()
        print('[Media] Got connection from', self.maddr)


    def acceptcsock(self):
        """
        accept to receive the file
        :return:
        """
        self.cconn, self.maddr = self.csock.accept()
        print('[Control] Got connection from'+ self.maddr)
        
        while 1:
            data = self.cconn.recv(1024)
            if not data: break
            if data[0:4] == "SEND": self.filename = data[5:]
            print ('[Control] Getting ready to receive ' + self.filename)
            break

    def transfer( self ):
        """
        Starting the transfert of the file
        :return:
        """
        print('[Media] Starting media transfer for ' + self.filename)

        f = open("download/" + self.filename,"wb")
        while 1:
            data = self.mconn.recv(1024)
            if not data: break
            f.write(data)
        f.close()

        print('[Media] Got ' + self.filename)
        print('[Media] Closing media transfer for ' + self.filename)
    
    def close(self):
        """
        We close the connection
        :return:
        """

        self.mconn.close()
        self.msock.close()

    def process(self):
        """
        function who start all the function
        :return:
        """

        self.bindmsock()
        self.acceptmsock()
        self.transfer()
        self.close()

#########################################################

class MySignal(QObject):
        sig = Signal(str)

class MyLongThread(QThread):
        def __init__(self, parent = None):

                QThread.__init__(self, parent)
                self.exiting = False
                self.signal = MySignal()

        def run(self):
                end = time.time()+10
                while not self.exiting:
                        sys.stdout.write('*')
                        sys.stdout.flush()
                        time.sleep(1)
                        now = time.time()
                        if now >= end:
                                self.exiting=True
                self.signal.sig.emit('OK')

class MyThread(QThread):
        def __init__(self, parent = None):
                QThread.__init__(self, parent)

                self.exiting = False

        def run(self):
            self.s.settimeout(None)
            data = self.s.recv(4096)
            messgServeur = (data.decode())
            self.gui.setNewMsg(messgServeur)

        def setConfig(self,s,gui):
            self.s = s
            self.gui = gui
            
       
#########################################################

            
class privateFile():
    def __init__(self, main, s, pseudoFile):
        """
        new windows for the p2p
        :param main:
        :param s:
        :param pseudoFile: pseudo of the people who need to send the file
        :return:
        """
        self.main = main
        self.s = s
        self.pseudoFile = pseudoFile
        self.g = QtGui.QWidget()
        self.ui = Ui_Dialog3()
        self.ui.setupUi(self.g)
        self.g.show()
        self.ui.label_2.setText(self.pseudoFile)
        self.ui.pushButton_2.clicked.connect(self.selectFile)
        self.ui.pushButton.clicked.connect(self.sendFile)
        

    def sendFile(self):
        """
        Send to the sever the command : /pmfile + pseudo to send + name of the file
        :return:
        """
        if self.ui.lineEdit.text() != "":
            self.ui.lineEdit.setText("")
            self.s.settimeout(5.0)
            try:
                print(self.cmd1.encode())
                self.s.send(self.cmd1.encode())
                self.g.close()
                
            except timeout:
                self.ShowMessageErreur("Erreur : Timeout. Le serveur ne repond pas")
        
    def selectFile(self):
        """
        buttton to open and chose the file to send and create the name of the command
        :return:
        """
        nomFile = ' '.join(QFileDialog.getOpenFileName())
        self.ui.lineEdit.setText('/pmfile '+self.pseudoFile+ " "+nomFile )
        self.cmd1 = self.ui.lineEdit.text()
        self.bob = ' '.join(nomFile.split("/")[-1:])

#########################################################

class privateMessage() :
    def __init__(self,main,s, pmPerson, pmPerso):
        """
        new windows for a private conversation
        :param main:
        :param s:
        :param pmPerson:
        :param pmPerso:
        :return:
        """
        self.main = main
        self.s = s
        self.pmPerso = pmPerso
        self.pmPerson = pmPerson
        self.g = QtGui.QWidget()
        self.ui = Ui_Dialog2()
        self.ui.setupUi(self.g)
        self.g.show()
        self.message_buffer2 = ""

        self.g.setWindowState(self.g.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        self.g.activateWindow()

        Qt.WindowStaysOnTopHint

        self.queueMsg2=[]
        self.thread = MyThread()
        self.thread.finished.connect(self.UpdateChatP)

        self.ui.pushButton.clicked.connect(self.send)
        self.ui.lineEdit.returnPressed.connect(self.send)

        self.ui.pushButton_4.clicked.connect(self.reject)
        self.ui.pushButton_3.clicked.connect(self.accept)

        self.ui.label_2.setText(pmPerson)

    def codeNb(self, txt):
        """
        converted a return code (info and succes) in the message
        :param txt: code from the server
        :return: info, String return from server
        """
        if txt == "300": info = "USERLIST"
        elif txt == "301": info = "USERAWAY"
        elif txt == "302": info = "HAS_JOIN"
        elif txt == "303": info = "HAS_LEFT"
        elif txt == "304": info = "NEW_MSG"
        elif txt == "305": info = "NAME_CHANGED"
        elif txt == "306": info = "NEW_PM"
        elif txt == "307": info = "ASKING_FOR_PM"
        elif txt == "308": info = "PRIVATE_DISCU_ACCEPTED_FROM"
        elif txt == "309": info = "PRIVATE_DISCU_REFUSED_FROM"
        elif txt == "310": info = "IS_NOW_ENABLE"
        elif txt == "311": info = "IS_NOW_DISABLE"
        elif txt == "312": info = "HAS_ASKED_FILE"
        elif txt == "313": info = "CAN_SEND_FILE"
        elif txt == "314": info = "HAS_REJECT_FILE"
        elif txt == "200" or txt == "200300": info = "SUCC_CHANNEL_JOINED"
        elif txt == "200300": info = "SUCC_CHANNEL_JOINED USERLIST"
        elif txt == "201": info = "SUCC_CHANNEL_QUIT"
        elif txt == "202": info = "SUCC_MESSAGE_SENDED"
        elif txt == "203": info = "SUCC_NICKNAME_CHANGED"
        elif txt == "204": info = "SUCC_VALID_NICKNAME"
        elif txt == "205": info = "SUCC_PM_SENDED"
        elif txt == "206": info = "SUCCESSFUL_ASKED_CONV"
        elif txt == "207": info = "SUCCESSFUL_ACCEPTED_CONV"
        elif txt == "208": info = "SUCCESSFUL_REFUSED_CONV"
        elif txt == "209": info = "SUCC_ENABLED"
        elif txt == "210": info = "SUCC_DISABLED"
        elif txt == "211": info = "SUCC_PMFILE"
        elif txt == "212": info = "SUCC_ACCEPTED_FILE"
        elif txt == "213": info = "SUCC_REFUSED_FILE"
        else: info = txt
        
        return info
        
    def reject(self):
        """
        if a user reject a pm conversation
        :return:
        """
        self.cmRej = "/rejectpm "+self.pmPerson
        self.s.settimeout(5.0)
        try:
            self.s.send(self.cmRej.encode())

        except timeout:
            self.ShowMessageErreur("Erreur : Timeout. Le serveur ne repond pas")
            self.ui.txtOutput.setText(self.message_buffer2)
            sb = self.ui.txtOutput.verticalScrollBar()
            sb.setValue(sb.maximum())

    def accept(self):
        """
        if a user accept a pm with another user
        :return:
        """
        self.cmAcc = "/acceptpm "+self.pmPerson
        self.s.settimeout(5.0)
        try:
            self.s.send(self.cmAcc.encode())

        except timeout:
            self.ShowMessageErreur("Erreur : Timeout. Le serveur ne repond pas")
            self.ui.txtOutput.setText(self.message_buffer2)
            sb = self.ui.txtOutput.verticalScrollBar()
            sb.setValue(sb.maximum())

    def htmlToText( self, html ):
        """
        converted some characters written by the user (html tag, smiley)
        :param html: message written by an user
        :return: html, message converted
        """
        html = html.replace('&', '&amp;')
        html = html.replace('>', '&#62;')
        html = html.replace('<', '&quot;')
        html = html.replace(':-)', '<img src="img/happy.png" alt="Smiley face">')
        html = html.replace(':-(', '<img src="img/sad.png" alt="sad face">')
        html = html.replace(':-p', '<img src="img/langue.png" alt="langue face">')
        html = html.replace(';-)', '<img src="img/oeil.png" alt="oeil face">')
        html = html.replace(':-D', '<img src="img/veryHappy.png" alt="very happy face">')
        html = html.replace(':-o', '<img src="img/etonne.png" alt="etonne face">')
        html = html.replace(':\'(', '<img src="img/cry.png" alt="cry face">')
        html = html.replace('(y)', '<img src="img/like.png" alt="like face">')
        html = html.replace('8|', '<img src="img/lunette.png" alt="lunette face">')
        html = html.replace('3:)', '<img src="img/hell.png" alt="hell face">')
        html = html.replace(':pedobear', '<img src="img/pedo.gif"  alt="hell face">')
        html = html.replace(':homer', '<img src="img/homer.gif"  alt="homer face">')
        html = html.replace(':dalek', '<img src="img/Dalek.gif"  alt="homer face">')
        html = html.replace(':tardis', '<img src="img/tardis.png"  alt="homer face">')

        return html

    def ShowMessageErreur(self, txt):
        """
        Show with color message from the server with error
        :param txt:message from server
        :return: message with color
        """
        self.message_buffer2 += '<br> <span style="color : red; font-weight: bold;"> ' + self.htmlToText(txt) + ' </span>'

    def send(self):
        """
        send the message written in the pm conversation
        :return:
        """
        self.cmdP = self.ui.lineEdit.text()
        if self.cmdP != "":
            self.ui.lineEdit.setText('')
            self.s.settimeout(5.0)
            self.cmd = "/pm " +self.pmPerson+ " " + self.cmdP
            self.s.settimeout(5.0)
            try:
                self.s.send(self.cmd.encode())

            except timeout:
                self.ShowMessageErreur("Erreur : Timeout. Le serveur ne repond pas")
                self.ui.txtOutput.setText(self.message_buffer2)
                sb = self.ui.txtOutput.verticalScrollBar()
                sb.setValue(sb.maximum())

    def UpdateChatP(self):
        """
        update the chat box
        :return:
        """
        if self.queueMsg2  :
            m = self.queueMsg2.pop(0)
            if  m :
                self.thread.start()
                self.ShowMessageAsTextPm(m)

    def getTimeStamp(self):
        """
        the time format: H:M
        :return: time
        """
        return ('[%s] ' % str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%H:%M')))

    def ShowMessageAsTextPm(self, txt):
        """
        add txt to the buffer with the time and color
        :param txt: message from sever
        :return:
        """
        #self.message_buffer2 += '<br><span style="color : grey">'+self.codeNb(txt)+'</span>'

        if self.codeNb(txt.split(" ")[0]) == "SUCC_PRIVATE_DISCUSSION_REFUSED":
            self.g.close()

        if self.codeNb(txt.split(" ")[0]) == "SUCC_PRIVATE_DISCUSSION_REJECTED":
            self.g.close()


        if self.codeNb(txt.split(" ")[0]) == "SUCC_PM_SENDED":
            self.message_buffer2 += '<br><span style="color : grey"> ' + self.getTimeStamp() + '</span> <span style="color : red"> &#60; '+self.pmPerso +' &#62; </span> <span style="color : black">' + self.htmlToText(self.cmdP) + '</span>'


        if self.codeNb(txt.split(" ")[0]) == "SUCC_PRIVATE_DISCUSSION_ACCEPTED":
            self.message_buffer2 += '<br> <span style="color : green"> Chalange Accepted ! </span>'
            self.ui.pushButton_4.setDisabled(True)
            self.ui.pushButton_3.setDisabled(True)


        if self.codeNb(txt.split(" ")[0]) == "PRIVATE_DISCU_ACCEPTED_FROM":
            self.message_buffer2 += '<br> <span style="color : green"> Private discussion with '+txt.split(" ")[1]+' accepted ! </span>'
            self.ui.pushButton_4.setDisabled(True)
            self.ui.pushButton_3.setDisabled(True)


        if self.codeNb(txt.split(" ")[0]) == "NEW_PM" :
            self.message_buffer2 += '<br><span style="color : grey"> ' + self.getTimeStamp() + '</span> <span style="color : red"> &#60; '+ txt.split(" ")[1] +' &#62; </span> ' + self.htmlToText(' '.join(txt.split(" ")[2:])) + ''


        self.ui.txtOutput.setText(self.message_buffer2)
        sb = self.ui.txtOutput.verticalScrollBar()
        sb.setValue(sb.maximum())

######################################################################################################################

class start(QtGui.QMainWindow):
    def __init__(self):
        """
        Main Windows with the main conversation
        :return:
        """
        super(start, self).__init__()
        self.queueMsg= []
        self.thread = MyThread()
        self.thread.finished.connect(self.UpdateChat)
        self.createWidgets()

    def setNewMsg (self,msg) :
        """
        add msg to the queueMsg
        :param msg:
        :return:
        """
        self.queueMsg.append(msg)

    def getTimeStamp(self):
        """
        the time format: H:M
        :return: time
        """
        return('[%s] ' % str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%H:%M')))

    def htmlToText( self, html):
        """
        converted some characters written by the user (html tag, smiley)
        :param html: message written by an user
        :return: html, message converted
        """


        html = html.replace('&', '&amp;')
        html = html.replace('>', '&#62;')
        html = html.replace('<', '&quot;')
        html = html.replace(':-)', '<img src="img/happy.png" alt="Smiley face">')
        html = html.replace(':-(', '<img src="img/sad.png" alt="sad face">')
        html = html.replace(':-p', '<img src="img/langue.png" alt="langue face">')
        html = html.replace(';-)', '<img src="img/oeil.png" alt="oeil face">')
        html = html.replace(':-D', '<img src="img/veryHappy.png" alt="very happy face">')
        html = html.replace(':-o', '<img src="img/etonne.png" alt="etonne face">')
        html = html.replace(':\'(', '<img src="img/cry.png" alt="cry face">')
        html = html.replace('(y)', '<img src="img/like.png" alt="like face">')
        html = html.replace('8|', '<img src="img/lunette.png" alt="lunette face">')
        html = html.replace('3:)', '<img src="img/hell.png" alt="hell face">')
        html = html.replace(':pedobear', '<img src="img/pedo.gif"  alt="hell face">')
        html = html.replace(':homer', '<img src="img/homer.gif"  alt="homer face">')
        html = html.replace(':dalek', '<img src="img/Dalek.gif"  alt="homer face">')
        html = html.replace(':tardis', '<img src="img/tardis.png"  alt="homer face">')

        return html

    def ShowMessageErreur(self, txt):
        """
        add to the buffer an erreur message with color
        :param txt:message from the server
        :return:
        """
        self.message_buffer += '<br> <span style="color : red; font-weight: bold;"> '+  self.htmlToText(txt) +' </span>'

    def ShowMessageOK(self, txt):
        """
        add to the buffer a good message with style
        :param txt:message from the server
        :return:
        """
        self.message_buffer += '<br> <span style="color : green; font-weight: bold;"> '+  self.htmlToText(txt) +' </span>'

    def ShowMessageInfo (self, txt):
        """
        add to the buffer an info message with style
        :param txt:message from the server
        :return:
        """
        self.message_buffer += '<br> <span style="color : #FF00FF; font-weight: bold;"> '+  self.htmlToText(txt) +' </span>'

    def ShowMessageAsText(self, txt):
        """
        add to the buffer message from the server with style and run some function
        :param txt:message from the server
        :return:
        """
        #self.message_buffer += '<br> <span style="color : #E6E6E6"> '+  self.codeNb(str(txt)) +' </span>'
        
        if re.match("^4", txt):
            self.ShowMessageErreur("Erreur ! : " + self.errNb(txt))

        if self.codeNb(txt.split(" ")[0]) == "IS_NOW_DISABLE":
            self.ShowMessageInfo(txt.split(" ")[1]+" is Away From Keyboard")
            self.ui.listNames.clear()
            self.ui.listNames_2.clear()
            self.s.send("/userlist".encode())
            self.s.send("/userlistaway".encode())

        if self.codeNb(txt.split(" ")[0]) == "IS_NOW_ENABLE":
            self.ShowMessageInfo(txt.split(" ")[1]+" is Back !!")
            self.ui.listNames.clear()
            self.ui.listNames_2.clear()
            self.s.send("/userlist".encode())
            self.s.send("/userlistaway".encode())

        if self.codeNb(txt.split(" ")[0]) == "HAS_ASKED_FILE":
            self.ShowMessageOK(txt.split(" ")[1]+" share a file with you, do you want download "+' '.join(txt.split(" ")[2].split("/")[-1:])+" ?")
            self.questionMessage(txt.split(" ")[1],txt.split(" ")[2])
            self.fileNom = ' '.join(txt.split(" ")[2].split("/")[-1:])

        if self.codeNb(txt.split(" ")[0]) == "SUCC_ASKED_FILE":
            self.ShowMessageOK("Succes asked file")

        if self.codeNb(txt.split(" ")[0]) == "SUCC_ACCEPTED_FILE":
            self.ShowMessageOK("accepted file on ip "+txt.split(" ")[1])
            s = StreamHandler(self.portFile, self.fileNom)
            s.start()

        if self.codeNb(txt.split(" ")[0]) == "CAN_SEND_FILE":
            self.ShowMessageOK("file can be send  ")
            ms = socket(AF_INET, SOCK_STREAM)
            print(txt.split(" ")[2]+" "+txt.split(" ")[3])
            ms.connect((str(txt.split(" ")[2]), int(txt.split(" ")[3])))
            f = open(txt.split(" ")[4], "rb")
            data = f.read()
            f.close()
            ms.send(data)
            ms.close() 

        if self.codeNb(txt.split(" ")[0]) == "SUCCESSFUL_ACCEPTED_CONV":
            self.message_buffer += '<br> <span style="color : green"> PRIVATE DISCUSSION ? challenge accepted ! '
            self.private2.ShowMessageAsTextPm("SUCC_PRIVATE_DISCUSSION_ACCEPTED")

        if self.codeNb(txt.split(" ")[0]) == "PRIVATE_DISCU_ACCEPTED_FROM":
            self.message_buffer += '<br> <span style="color : green"> PRIVATE DISCUSSION WITH '+txt.split(" ")[1] + ' ? challenge accepted ! '
            self.private2.ShowMessageAsTextPm(txt)

        if self.codeNb(txt.split(" ")[0]) == "SUCCESSFUL_ASKED_CONV":
             self.ShowMessageOK("invitation requested")
             self.private2 = privateMessage(self, self.s, self.demande, self.pseudo)

        if self.codeNb(txt.split(" ")[0]) == "ASKING_FOR_PM":
             self.ShowMessageOK("private discution from "+ txt.split(" ")[1])
             self.private2 = privateMessage(self,self.s,txt.split(" ")[1], self.pseudo)

        if self.codeNb(txt.split(" ")[0]) == "SUCC_PM_SENDED":
            self.private2.ShowMessageAsTextPm(txt.split(" ")[0])

        if self.codeNb(txt.split(" ")[0]) == "NEW_PM":
            self.private2.ShowMessageAsTextPm(txt)

        if self.codeNb(txt.split(" ")[0]) == "SUCC_PRIVATE_DISCUSSION_REFUSED":
            self.private2.ShowMessageAsTextPm(txt)
            self.ShowMessageOK("Private discussion refused !!")

        if self.codeNb(txt.split(" ")[0]) == "SUCC_PRIVATE_DISCUSSION_REJECTED":
            self.private2.ShowMessageAsTextPm(txt)
            self.ShowMessageOK(txt.split(" ")[1]+" Rejected your Private discussion !!")

        if self.codeNb(txt.split(" ")[0]) == "SUCC_CHANNEL_QUIT":
            self.ShowMessageOK("You have logged out of the DNC !")
            self.ui.listNames.clear()
            self.ui.listNames_2.clear()
            self.ui.lineEdit.setDisabled(True)
            self.ui.pushButton.setDisabled(True)
            self.ui.pushButton_2.setDisabled(False)
            self.ui.pushButton_3.setDisabled(True)
            self.ui.pushButton_6.setDisabled(True)

            self.ui.lineEdit_4.setDisabled(False)
            self.ui.lineEdit_3.setDisabled(False)

        if self.codeNb(txt.split(" ")[0]) == "SUCC_DISABLED":
            self.ShowMessageOK("You are AFK !")
            self.ui.listNames.clear()
            self.ui.listNames_2.clear()
            self.s.send("/userlist".encode())
            self.s.send("/userlistaway".encode())

        if self.codeNb(txt.split(" ")[0]) == "SUCC_ENABLED":
            self.ShowMessageOK("You are back !")
            self.ui.listNames.clear()
            self.ui.listNames_2.clear()
            self.s.send("/userlist".encode())
            self.s.send("/userlistaway".encode())

        if self.codeNb(txt.split(" ")[0]) == "SUCC_NICKNAME_CHANGED":
            self.ShowMessageOK("Sucessful nickname change !")
            self.ui.listNames.clear()
            self.s.send("/userlist".encode())

        if self.errNb(txt.split(" ")[0]) == "ERR_INVALID_NICKNAME":
            self.pseudo = "INVALID_NICKNAME"

        if self.codeNb(txt.split(" ")[0]) == "NAME_CHANGED":
            self.ShowMessageNameChange(txt.split(" ")[1], txt.split(" ")[2])
            self.ui.listNames.clear()
            self.s.send("/userlist".encode())

        if self.codeNb(txt.split(" ")[0]) == "HAS_JOIN" :
             self.ShowMessageHasJoin(txt.split(" ")[1])
             self.ui.listNames.addItem(txt.split(" ")[1])

        if self.codeNb(txt.split(" ")[0]) == "HAS_LEFT" :
            self.ShowMessageHasLeft(txt.split(" ")[1])
            self.ui.listNames.clear()
            self.s.send("/userlist".encode())

        if self.codeNb(txt.split(" ")[0]) == "SUCC_CHANNEL_JOINED" or txt.split(" ")[0] == "200":
            self.ShowMessageHasJoin(self.pseudo)
            self.ui.listNames.clear()
            self.ui.listNames_2.clear()
            self.s.send("/userlist".encode())
            self.s.send("/userlistaway".encode())

        if self.errNb(txt.split(" ")[0]) == "ERR_NICKNAME_ALREADY_USED":
            self.deco()

        if re.compile('USERLIST').search(self.codeNb(txt.split(" ")[0])):
            self.ui.listNames.clear()
            n = len(txt.split(" ")[1:]) + 1
            for i in range(1, n):
                self.ui.listNames.addItem(str(txt.split(" ")[i]).replace("301", ""))
            #print(str(txt.split(" ")[1:]))

        if re.compile('USERAWAY').search(self.codeNb(txt.split(" ")[0])):
            self.ui.listNames_2.clear()
            n = len(txt.split(" ")[1:]) + 1
            for i in range(1, n):
                self.ui.listNames_2.addItem(str(txt.split(" ")[i]))
            #print(str(txt.split(" ")[1:]))

        if self.codeNb(txt.split(" ")[0]) == "NEW_MSG" :
            self.message_buffer += '<br><span style="color : grey"> ' + self.getTimeStamp() + '</span> <span style="color : red"> &#60; '+txt.split(" ")[1] +' &#62; </span> <span style="color : black">' + self.htmlToText(' '.join(txt.split(" ")[2:])) + '</span>'

        if self.codeNb(txt) == "SUCC_MESSAGE_SENDED" :
            self.message_buffer += '<br><span style="color : grey"> ' + self.getTimeStamp() + '</span> <span style="color : red"> &#60; '+ self.pseudo +' &#62; </span><span style="color : black"> ' + self.htmlToText(self.cmd) + '</span>'

    def errNb (self, txt):
        """
        converted a return error code in the message
        :param txt: code from the server
        :return: String message
        """
        if txt == "400":
            info = "ERR_NICKNAME_ALREADY_USED"
            
        elif txt == "401":
            info = "ERR_NO_NICKNAME"
        
        elif txt == "402":
            info = "ERR_CONV_NOT_ALLOWED"

        elif txt == "403":
            info = "DEST_NOT_FOUND"
            
        elif txt == "404":
            info = "ERR_ALREADY_ASKED_FOR_PM"
            
        elif txt == "405":
            info = "ERR_NO_INVIT_TO_CONV_FOUND"
 
        elif txt == "406":
            info = "ERR_UNKNOWN_ACCEPTED_FILE"
            
        elif txt == "407":
            info = "COMMAND_NOT_FOUND"
            
        elif txt == "408":
            info = "ERR_INVALID_NICKNAME"
        else:
            info ="ERREUR " + txt
            
        return info


    def codeNb (self, txt):
        """
        converted a return code in the message
        :param txt: code from the server
        :return: info, String return from server
        """
        if txt == "300": info = "USERLIST"
        elif txt == "301": info = "USERAWAY"
        elif txt == "302": info = "HAS_JOIN"
        elif txt == "303": info = "HAS_LEFT"
        elif txt == "304": info = "NEW_MSG"
        elif txt == "305": info = "NAME_CHANGED"
        elif txt == "306": info = "NEW_PM"
        elif txt == "307": info = "ASKING_FOR_PM"
        elif txt == "308": info = "PRIVATE_DISCU_ACCEPTED_FROM"
        elif txt == "309": info = "PRIVATE_DISCU_REFUSED_FROM"
        elif txt == "310": info = "IS_NOW_ENABLE"
        elif txt == "311": info = "IS_NOW_DISABLE"
        elif txt == "312": info = "HAS_ASKED_FILE"
        elif txt == "313": info = "CAN_SEND_FILE"
        elif txt == "314": info = "HAS_REJECT_FILE"
        elif txt == "200" or txt=="200300": info = "SUCC_CHANNEL_JOINED"
        elif txt == "200300" : info = "SUCC_CHANNEL_JOINED USERLIST"
        elif txt == "201": info = "SUCC_CHANNEL_QUIT"
        elif txt == "202": info = "SUCC_MESSAGE_SENDED"
        elif txt == "203": info = "SUCC_NICKNAME_CHANGED"
        elif txt == "204": info = "SUCC_VALID_NICKNAME"
        elif txt == "205": info = "SUCC_PM_SENDED"
        elif txt == "206": info = "SUCCESSFUL_ASKED_CONV"
        elif txt == "207": info = "SUCCESSFUL_ACCEPTED_CONV"
        elif txt == "208": info = "SUCCESSFUL_REFUSED_CONV"
        elif txt == "209": info = "SUCC_ENABLED"
        elif txt == "210": info = "SUCC_DISABLED"
        elif txt == "211": info = "SUCC_PMFILE"
        elif txt == "212": info = "SUCC_ACCEPTED_FILE"
        elif txt == "213": info = "SUCC_REFUSED_FILE"
        else: info = txt
        
        return info

    def ShowMessageHasJoin(self, txt):
        """
        adds a message to the buffer to alert users that a person has joined the dnc
        :param txt: user name
        :return:
        """
        self.message_buffer += '<br> <span style="color : #FF00FF; font-weight: bold;"> '+  self.htmlToText(txt) +' has joined DNC </span>'

    def ShowMessageHasLeft(self, txt):
        """
        adds a message to the buffer to alert users that a person has left the dnc
        :param txt: user name
        :return:
        """
        self.message_buffer += '<br> <span style="color : #FF00FF; font-weight: bold;"> '+  self.htmlToText(txt) +' has left DNC </span>'

    def ShowMessageNameChange(self, txt, txt2):
        """
        adds a message to the buffer to alert users that a person change his name
        :param txt: old name
        :param txt2:new name
        :return:
        """
        self.message_buffer += '<br> <span style="color : #FF00FF; font-weight: bold;"> '+  self.htmlToText(txt) +' is now : '+self.htmlToText(txt2)+' </span>'

    def UpdateChat(self):
        """
        update the chat with the buffer
        :return:
        """
        if self.queueMsg :
            m = self.queueMsg.pop(0)
            if m:
                self.thread.start()
                self.ShowMessageAsText(m)
                self.ui.txtOutput.setText(self.message_buffer)
                sb = self.ui.txtOutput.verticalScrollBar()
                sb.setValue(sb.maximum())

    def questionMessage(self, name,fileN):
        """
        open un QMessageBox to  ask the user whether to download a file from another user
        :param name: user name who send file
        :param fileN: file name
        :return:
        """
        reply = QtGui.QMessageBox.question(self, "send file", "do you want to download the file : " + ' '.join(fileN.split("/")[-1:])+" from "+name+" ?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        
        if reply == QtGui.QMessageBox.Yes:
            text = ''.join(str(random.randint(1,9)) for _ in range(4))
            
            while text == self.portCo : 
                text = ''.join(str(random.randint(1,9)) for _ in range(4))
                
            cmdAccF = "/acceptfile "+name+" "+text+" "+fileN
            self.s.settimeout(5.0)
            try:
                self.s.send(cmdAccF.encode())
                print(cmdAccF)
                self.portFile = text

            except timeout:
                self.ShowMessageErreur("Erreur : Timeout. Le serveur ne repond pas")
                self.ui.txtOutput.setText(self.message_buffer)
                sb = self.ui.txtOutput.verticalScrollBar()
                sb.setValue(sb.maximum())

        elif reply == QtGui.QMessageBox.No:
            self.s.settimeout(5.0)
            try:
                cmdRej = "/rejectfile "+name+" "+fileN
                print(cmdRej)
                self.s.send(cmdRej.encode())

            except timeout:
                self.ShowMessageErreur("Erreur : Timeout. Le serveur ne repond pas")
                self.ui.txtOutput.setText(self.message_buffer)
                sb = self.ui.txtOutput.verticalScrollBar()
                sb.setValue(sb.maximum())

    def connectActions(self):
        """
        add an action to buttons
        :return:
        """
        self.ui.pushButton_2.clicked.connect(self.connecter)
        self.ui.pushButton_3.clicked.connect(self.deco)
        self.ui.pushButton.clicked.connect(self.client)
        self.ui.pushButton_6.clicked.connect(self.changeN)
        self.ui.pushButton_5.clicked.connect(self.away)
        self.ui.lineEdit.returnPressed.connect(self.client)

        self.ui.listNames.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.listNames.customContextMenuRequested.connect(self.buttonAMenu)


    @QtCore.pyqtSlot()
    def on_buttonA_released(self):
        print ('Doing Stuff when clicking on Button A')

    def buttonAMenu(self, pos):
        """
        menu with the right click on the user list
        :param pos:
        :return:
        """
        menu = QtGui.QMenu()
        menu.addAction('Private discussion', lambda:self.FirstActionButtonA())
        menu.addAction('Send file', lambda:self.SecondActionButtonA())
        menu.exec_(QtGui.QCursor.pos())

    def FirstActionButtonA(self):
        """
        first action (ask a pm) on the menu of the right click
        :return:
        """
        test1 = self.ui.listNames.currentItem().text()
        print("1e fonction : "+str(test1))
        self.someMethod(str(test1))


    def SecondActionButtonA(self):
        """
        second action (send file) on the menu of the right click
        :return:
        """
        test1 = self.ui.listNames.currentItem().text()
        print("2sd fonction : "+str(test1))
        self.privateFile = privateFile(self, self.s, str(test1))
        
        
    def someMethod(self,item):
        """
        ask a pm to another user of the list
        :param item: user name from the list
        :return:
        """
        nom = item.replace("SUCCESSFUL_ASKED_CONV","")
        cmdPM = "/askpm "+nom
        self.s.settimeout(5.0)
        try:
            self.s.send(cmdPM.encode())
            self.demande = nom

        except timeout:
            self.ShowMessageErreur("Erreur : Timeout. Le serveur ne repond pas")
            self.ui.txtOutput.setText(self.message_buffer)
            sb = self.ui.txtOutput.verticalScrollBar()
            sb.setValue(sb.maximum())

    def away(self):
        """
        action on the button afk and back
        :return:
        """
        if self.bouton == "disable" :
            cmdAway = "/disable "
            self.s.settimeout(5.0)
            try:
                self.s.send(cmdAway.encode())
                self.ui.pushButton_5.setText("Back")

            except timeout:
                self.ShowMessageErreur("Erreur : Timeout. Le serveur ne repond pas")
                self.ui.txtOutput.setText(self.message_buffer)
                sb = self.ui.txtOutput.verticalScrollBar()
                sb.setValue(sb.maximum())
            self.bouton = "enable"

        elif self.bouton == "enable" :
            self.bouton = "disable"
            cmdAway = "/enable "
            self.s.settimeout(5.0)
            try:
                self.s.send(cmdAway.encode())
                self.ui.pushButton_5.setText("Away From Keyboard")

            except timeout:
                self.ShowMessageErreur("Erreur : Timeout. Le serveur ne repond pas")
                self.ui.txtOutput.setText(self.message_buffer)
                sb = self.ui.txtOutput.verticalScrollBar()
                sb.setValue(sb.maximum())

    def changeN(self):
        """
        action to change name
        :return:
        """
        changePseudo = self.ui.lineEdit_2.text()
        if changePseudo != "":
            cmdChange = "/name "+changePseudo
            self.s.settimeout(5.0)
            try:
                self.s.send(cmdChange.encode())
                self.pseudo = changePseudo
                self.ui.listNames.clear()
                self.s.send("/userlist".encode())


            except timeout:
                self.ShowMessageErreur("Erreur : Timeout. Le serveur ne repond pas")
                self.ui.txtOutput.setText(self.message_buffer)
                sb = self.ui.txtOutput.verticalScrollBar()
                sb.setValue(sb.maximum())

    def connecter(self):
        """
        create a connection, chose name and start thread to update the chat
        :return:
        """
        ip = self.ui.lineEdit_4.text()
        port = int(self.ui.lineEdit_3.text())
        self.portCo = port
        Addr = (ip,port)
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.settimeout(5.0)
        try:
            self.s.connect(Addr)
        except timeout:
            self.ShowMessageErreur("Erreur : Timeout. Le serveur ne repond pas")
            self.ui.txtOutput.setText(self.message_buffer)
            sb = self.ui.txtOutput.verticalScrollBar()
            sb.setValue(sb.maximum())
            
        self.thread.setConfig(self.s, self)
        self.ui.lineEdit.setDisabled(False)
        self.ui.pushButton.setDisabled(False)
        self.ui.pushButton_2.setDisabled(True)
        self.ui.pushButton_3.setDisabled(False)
        self.ui.lineEdit_4.setDisabled(True)
        self.ui.lineEdit_3.setDisabled(True)
        self.thread.start()

        cmd2 = self.ui.lineEdit_2.text()
        if cmd2 != "":
            self.s.settimeout(5.0)
            cmdPseudo = "/newname "+cmd2
            self.s.settimeout(5.0)
            try:
                self.s.send(cmdPseudo.encode())
                self.pseudo = cmd2
                self.ui.pushButton_6.setDisabled(False)

            except timeout:
                self.ShowMessageErreur("Erreur : Timeout. Le serveur ne repond pas")
                self.ui.txtOutput.setText(self.message_buffer)
                sb = self.ui.txtOutput.verticalScrollBar()
                sb.setValue(sb.maximum())

    def deco(self):
        """
        action on the button to disconnect from dnc
        :return:
        """
        quitter = "/quit"
        self.s.send(quitter.encode())
        #self.s.close()


    def createWidgets(self):
        """
        run the main windows, with config
        :return:
        """
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ano = "anonymous" + ''.join(str(random.randint(1,9)) for _ in range(2))

        config = configparser.ConfigParser()
        config.read("dncClient.conf")

        port = config.get("NETWORK", "port")
        ip = config.get("NETWORK", "ip")
        name = config.get("PSEUDO", "name")

        if name is not None:
            self.ui.lineEdit_2.setText(name)
        else:
            self.ui.lineEdit_2.setText(ano)

        if ip is not None:
            self.ui.lineEdit_4.setText(ip)

        if port is not None:
            self.ui.lineEdit_3.setText(port)

        self.ui.lineEdit.setDisabled(True)
        self.ui.pushButton.setDisabled(True)
        self.ui.pushButton_3.setDisabled(True)
        self.ui.pushButton_6.setDisabled(True)
        self.message_buffer = ""
        self.bouton = "disable"
        self.connectActions()

    def client(self):
        """
        send a message to the sever
        :return:
        """
        self.cmd = self.ui.lineEdit.text()
        if self.cmd != "":
            self.ui.lineEdit.setText('')
            self.s.settimeout(5.0)
            try:
                self.s.send(self.cmd.encode())

                if self.cmd.split(" ")[0] == "/newname":
                    self.pseudo = self.cmd.split(" ")[1]

                if self.cmd.split(" ")[0] == "/name":
                    self.pseudo = self.cmd.split(" ")[1]

                if self.cmd.split(" ")[0] == "/askpm":
                    self.demande = self.cmd.split(" ")[1]

            except timeout:
                self.ShowMessageErreur("Erreur : Timeout. Le serveur ne repond pas")
                self.ui.txtOutput.setText(self.message_buffer)
                sb = self.ui.txtOutput.verticalScrollBar()
                sb.setValue(sb.maximum())


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    myapp = start()
    myapp.show()
    myapp.focusWidget()
    for t in threading.enumerate():
        if t != threading.main_thread(): t.join()
    sys.exit(app.exec_())
