from main import Ui_MainWindow
from PyQt4 import QtGui, QtCore
from PySide.QtCore import *
from PySide.QtGui import *
import time, threading, datetime, time, random,re
from socket import *
from pmWindow import Ui_Dialog2
from pmFile import Ui_Dialog3
import configparser
import string, sys, urllib.parse
from threading import *




#------------------------------------------------------------------------

class StreamHandler ( Thread ):

    def __init__( this , port, filename):
        Thread.__init__( this  )
        this.port = port
        this.filename = filename

    def run(this):
        this.process()

    def bindmsock( this ):
        this.msock = socket(AF_INET, SOCK_STREAM)
        this.msock.bind(('', int(this.port)))
        this.msock.listen(1)
        print ('[Media] Listening on port'+this.port)

    def acceptmsock( this ):
        this.mconn, this.maddr = this.msock.accept()
        print ('[Media] Got connection from', this.maddr)
    


    def acceptcsock( this ):
        this.cconn, this.maddr = this.csock.accept()
        print ('[Control] Got connection from'+ this.maddr)
        
        while 1:
            data = this.cconn.recv(1024)
            if not data: break
            if data[0:4] == "SEND": this.filename = data[5:]
            print ('[Control] Getting ready to receive ' + this.filename)
            break

    def transfer( this ):
        print ('[Media] Starting media transfer for ' + this.filename)

        f = open(this.filename,"wb")
        while 1:
            data = this.mconn.recv(1024)
            if not data: break
            f.write(data)
        f.close()

        print ('[Media] Got ' + this.filename)
        print ('[Media] Closing media transfer for ' + this.filename)
    
    def close( this ):
        #this.cconn.close()
        #this.csock.close()
        this.mconn.close()
        this.msock.close()

    def process( this ):
            #this.bindcsock()
            #this.acceptcsock()
            this.bindmsock()
            this.acceptmsock()
            this.transfer()
            this.close()

#------------------------------------------------------------------------





class MySignal(QObject):
        sig = Signal(str)

class MyLongThread(QThread):
        def __init__(self, parent = None):
                QThread.__init__(self, parent)
                self.exiting = False
                self.signal = MySignal()

        def run(self):
                end = time.time()+10
                while self.exiting==False:
                        sys.stdout.write('*')
                        sys.stdout.flush()
                        time.sleep(1)
                        now = time.time()
                        if now>=end:
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
            
            
class privateFile () : 
    def __init__(self,main,s, pseudoFile):

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
        if self.ui.lineEdit.text() != "" : 
            self.ui.lineEdit.setText("")
            try:
                print(self.cmd1.encode())
                self.s.send(self.cmd1.encode())
                self.g.close()
                
            except timeout:
                self.ShowMessageErreur("Erreur : Timeout. Le serveur ne repond pas")
        

    def selectFile(self):
        nomFile = ' '.join(QFileDialog.getOpenFileName())
        self.ui.lineEdit.setText('/pmfile '+self.pseudoFile+ " "+nomFile )
        self.cmd1 = self.ui.lineEdit.text()
        self.bob = ' '.join(nomFile.split("/")[-1:])

        
class privateMessage () :
    def __init__(self,main,s, pmPerson, pmPerso):

        self.main = main
        self.s = s
        self.pmPerso = pmPerso
        self.pmPerson = pmPerson
        self.g = QtGui.QWidget()
        self.ui = Ui_Dialog2()
        self.ui.setupUi(self.g)
        self.g.show()
        #old = start()
        self.message_buffer2 = ""

        self.g.setWindowState(self.g.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        self.g.activateWindow()

        Qt.WindowStaysOnTopHint

        self.queueMsg2= []
        self.thread = MyThread()
        self.thread.finished.connect(self.UpdateChatP)

        self.ui.pushButton.clicked.connect(self.send)
        self.ui.lineEdit.returnPressed.connect(self.send)

        self.ui.pushButton_4.clicked.connect(self.reject)
        self.ui.pushButton_3.clicked.connect(self.accept)

        self.ui.label_2.setText(pmPerson)

    def reject(self):
        self.cmRej = "/rejectpm "+self.pmPerson
        try:
            self.s.send(self.cmRej.encode())

        except timeout:
            self.ShowMessageErreur("Erreur : Timeout. Le serveur ne repond pas")
            self.ui.txtOutput.setText(self.message_buffer2)
            sb = self.ui.txtOutput.verticalScrollBar()
            sb.setValue(sb.maximum())

    def accept(self):
        self.cmAcc = "/acceptpm "+self.pmPerson
        try:
            self.s.send(self.cmAcc.encode())


        except timeout:
            self.ShowMessageErreur("Erreur : Timeout. Le serveur ne repond pas")
            self.ui.txtOutput.setText(self.message_buffer2)
            sb = self.ui.txtOutput.verticalScrollBar()
            sb.setValue(sb.maximum())



    def htmlToText( self, html ):

        html = html.replace('<', '&#60;')
        html = html.replace('>', '&#62;')
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


        return html

    def ShowMessageErreur(self, txt):
        self.message_buffer2 += '<br> <span style="color : red; font-weight: bold;"> '+  self.htmlToText(txt) +' </span>'


    def send(self):
        self.cmdP = self.ui.lineEdit.text()
        if self.cmdP != "":
            self.ui.lineEdit.setText('')
            self.s.settimeout(5.0)
            self.cmd = "/pm " +self.pmPerson+ " " + self.cmdP
            try:
                self.s.send(self.cmd.encode())

            except timeout:
                self.ShowMessageErreur("Erreur : Timeout. Le serveur ne repond pas")
                self.ui.txtOutput.setText(self.message_buffer2)
                sb = self.ui.txtOutput.verticalScrollBar()
                sb.setValue(sb.maximum())

    def UpdateChatP(self) :
        if self.queueMsg2  :
            m = self.queueMsg2.pop(0)
            if  m :
                self.thread.start()
                self.ShowMessageAsTextPm(m)


    def getTimeStamp(self):
        return ('[%s] ' % str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%H:%M')))

    def ShowMessageAsTextPm(self, txt) :

            self.message_buffer2 += '<br><span style="color : grey">'+txt+'</span>'

            if txt.split(" ")[0] == "SUCC_PRIVATE_DISCUSSION_REFUSED":
                self.g.close()

            if txt.split(" ")[0] == "SUCC_PRIVATE_DISCUSSION_REJECTED":
                self.g.close()


            if txt.split(" ")[0] == "SUCC_PM_SENDED":
                self.message_buffer2 += '<br><span style="color : grey"> ' + self.getTimeStamp() + '</span> <span style="color : red"> &#60; '+self.pmPerso +' &#62; </span> ' + self.htmlToText(self.cmdP) + ''


            if txt.split(" ")[0] == "SUCC_PRIVATE_DISCUSSION_ACCEPTED":
                self.message_buffer2 += '<br> <span style="color : green"> Chalange Accepted ! </span>'
                self.ui.pushButton_4.setDisabled(True)
                self.ui.pushButton_3.setDisabled(True)


            if txt.split(" ")[0] == "SUCC_PRIVATE_DISCUSSION_OK":
                self.message_buffer2 += '<br> <span style="color : green"> Private discussion with '+txt.split(" ")[1]+' accepted ! </span>'
                self.ui.pushButton_4.setDisabled(True)
                self.ui.pushButton_3.setDisabled(True)


            if txt.split(" ")[0] == "NEW_PM" :
                self.message_buffer2 += '<br><span style="color : grey"> ' + self.getTimeStamp() + '</span> <span style="color : red"> &#60; '+ self.pmPerso +' &#62; </span> ' + self.htmlToText(' '.join(txt.split(" ")[2:])) + ''


            self.ui.txtOutput.setText(self.message_buffer2)
            sb = self.ui.txtOutput.verticalScrollBar()
            sb.setValue(sb.maximum())

class start(QtGui.QMainWindow):
    def __init__(self):
        super(start, self).__init__()
        self.queueMsg= []
        self.thread = MyThread()
        self.thread.finished.connect(self.UpdateChat)


        self.createWidgets()

    def setNewMsg (self,msg) :
        self.queueMsg.append(msg)

    def getTimeStamp(self):
        return ('[%s] ' % str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%H:%M')))

    def htmlToText( self, html ):

        html = html.replace('<', '&#60;')
        html = html.replace('>', '&#62;')
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


        return html

    def ShowMessageErreur(self, txt):
        self.message_buffer += '<br> <span style="color : red; font-weight: bold;"> '+  self.htmlToText(txt) +' </span>'

    def ShowMessageOK(self, txt):
        self.message_buffer += '<br> <span style="color : green; font-weight: bold;"> '+  self.htmlToText(txt) +' </span>'

    def ShowMessageInfo (self, txt) :
        self.message_buffer += '<br> <span style="color : #FF00FF; font-weight: bold;"> '+  self.htmlToText(txt) +' </span>'


    def ShowMessageAsText(self, txt):

        if re.match("^ERR_", txt):
            self.ShowMessageErreur("Erreur ! : " + txt)

        self.message_buffer += '<br> <span style="color : #E6E6E6"> '+  txt +' </span>'

        if txt.split(" ")[0] == "IS_NOW_DISABLE":
            self.ShowMessageInfo(txt.split(" ")[1]+" is Away From Keyboard")
            self.ui.listNames.clear()
            self.ui.listNames_2.clear()
            self.s.send("/userlist".encode())
            self.s.send("/userlistaway".encode())


        if txt.split(" ")[0] == "IS_NOW_ENABLE":
            self.ShowMessageInfo(txt.split(" ")[1]+" is Back !!")
            self.ui.listNames.clear()
            self.ui.listNames_2.clear()
            self.s.send("/userlist".encode())
            self.s.send("/userlistaway".encode())


        if txt.split(" ")[0] == "HAS_ASKED_FILE":
            self.ShowMessageOK(txt.split(" ")[1]+" share a file with you, do you want download "+' '.join(txt.split(" ")[2].split("/")[-1:])+" ?")
            self.questionMessage(txt.split(" ")[1],txt.split(" ")[2])
            self.fileNom = ' '.join(txt.split(" ")[2].split("/")[-1:])

        if txt.split(" ")[0] == "SUCC_ASKED_FILE":
            self.ShowMessageOK("Succes asked file")

        if txt.split(" ")[0] == "SUCC_FILE_ACCEPTED":
            self.ShowMessageOK("accepted file on ip "+txt.split(" ")[1])
            s = StreamHandler(self.portFile, self.fileNom)
            s.start()
            
            
        if txt.split(" ")[0] == "CAN_SEND_FILE":
            self.ShowMessageOK("file can be send  ")
            
            ms = socket(AF_INET, SOCK_STREAM)
            
            print(txt.split(" ")[2]+" "+txt.split(" ")[3])
            
            ms.connect((str(txt.split(" ")[2]), int(txt.split(" ")[3])))

            f = open(txt.split(" ")[4], "rb")
            data = f.read()
            f.close()

            ms.send(data)
            ms.close() 
            



        if txt.split(" ")[0] == "SUCC_PRIVATE_DISCUSSION_ACCEPTED":
            self.message_buffer += '<br> <span style="color : green"> PRIVATE DISCUSSION ? challenge accepted ! '
            self.private2.ShowMessageAsTextPm("SUCC_PRIVATE_DISCUSSION_ACCEPTED")

        if txt.split(" ")[0] == "SUCC_PRIVATE_DISCUSSION_OK":
            self.message_buffer += '<br> <span style="color : green"> PRIVATE DISCUSSION WITH '+txt.split(" ")[1]+' ? challenge accepted ! '
            self.private2.ShowMessageAsTextPm(txt)



        if txt.split(" ")[0] == "SUCC_INVITED" :
             self.ShowMessageOK("invitation requested")
             self.private2 = privateMessage(self,self.s,self.demande,self.pseudo)

        if txt.split(" ")[0] == "ASKING_FOR_PM" :
             self.ShowMessageOK("private discution from "+ txt.split(" ")[1] )
             self.private2 = privateMessage(self,self.s,txt.split(" ")[1],self.pseudo)



        if txt.split(" ")[0] == "SUCC_PM_SENDED" :
            self.private2.ShowMessageAsTextPm(txt.split(" ")[0])

        if txt.split(" ")[0] == "NEW_PM" :
            self.private2.ShowMessageAsTextPm(txt)

        if txt.split(" ")[0] == "SUCC_PRIVATE_DISCUSSION_REFUSED" :
            self.private2.ShowMessageAsTextPm(txt)
            self.ShowMessageOK("Private discussion refused !!")

        if txt.split(" ")[0] == "SUCC_PRIVATE_DISCUSSION_REJECTED" :
            self.private2.ShowMessageAsTextPm(txt)
            self.ShowMessageOK(txt.split(" ")[1]+" Rejected your Private discussion !!")



        if txt.split(" ")[0] == "SUCCESSFUL_LOGOUT" :
            self.ShowMessageOK("You have logged out of the DNC !")
            self.ui.listNames.clear()
            self.ui.listNames_2.clear()

        if txt.split(" ")[0] == "SUCC_DISABLED" :
            self.ShowMessageOK("You are AFK !")
            self.ui.listNames.clear()
            self.ui.listNames_2.clear()
            self.s.send("/userlist".encode())
            self.s.send("/userlistaway".encode())


        if txt.split(" ")[0] == "SUCC_ENABLED" :
            self.ShowMessageOK("You are back !")
            self.ui.listNames.clear()
            self.ui.listNames_2.clear()
            self.s.send("/userlist".encode())
            self.s.send("/userlistaway".encode())


        if txt.split(" ")[0] == "SUCC_VALID_NICKNAME" :
             self.ShowMessageOK("Sucessful nickname change !")

        if txt.split(" ")[0] == "ERR_INVALID_NICKNAME" :
            self.pseudo = "INVALID_NICKNAME"


        if txt.split(" ")[0] == "NAME_CHANGED" :
            self.ShowMessageNameChange(txt.split(" ")[1], txt.split(" ")[2])
            self.ui.listNames.clear()
            self.s.send("/userlist".encode())

        if txt.split(" ")[0] == "HAS_JOIN" :
             self.ShowMessageHasJoin(txt.split(" ")[1])
             self.ui.listNames.addItem(txt.split(" ")[1])

        if txt.split(" ")[0] == "HAS_LEFT" :
            self.ShowMessageHasLeft(txt.split(" ")[1])
            self.ui.listNames.clear()
            self.s.send("/userlist".encode())


        if txt.split(" ")[0] == "SUCC_CHANNEL_JOINED" or txt.split(" ")[0] == "SUCC_CHANNEL_JOINEDUSERLIST" :
            self.ShowMessageHasJoin(self.pseudo)
            self.ui.listNames.clear()
            self.ui.listNames_2.clear()
            #self.s.send("/userlist".encode())
            #self.s.send("/userlistaway".encode())


        if txt.split(" ")[0] == "ERR_NICKNAME_ALREADY_USED" :
            self.deco()


        if re.compile('USERLIST').search(txt.split(" ")[0] ) :
            n = len(txt.split(" ")[1:]) +1
            for i in range(1,n) :
                self.ui.listNames.addItem(str(txt.split(" ")[i]).replace("USERAWAY",""))
            print(str(txt.split(" ")[1:]))

        if re.compile('USERAWAY').search(txt.split(" ")[0] ) :
            n = len(txt.split(" ")[1:]) +1
            for i in range(1,n) :
                self.ui.listNames_2.addItem(str(txt.split(" ")[i]))
            print(str(txt.split(" ")[1:]))



        if txt.split(" ")[0] == "NEW_MSG" :
            self.message_buffer += '<br><span style="color : grey"> ' + self.getTimeStamp() + '</span> <span style="color : red"> &#60; '+txt.split(" ")[1] +' &#62; </span> <span style="color : black">' + self.htmlToText(' '.join(txt.split(" ")[2:])) + '</span>'

        if txt == "SUCC_MESSAGE_SENDED" :
            self.message_buffer += '<br><span style="color : grey"> ' + self.getTimeStamp() + '</span> <span style="color : red"> &#60; '+ self.pseudo +' &#62; </span><span style="color : black"> ' + self.htmlToText(self.cmd) + '</span>'


    def ShowMessageHasJoin (self, txt) :
        self.message_buffer += '<br> <span style="color : #FF00FF; font-weight: bold;"> '+  self.htmlToText(txt) +' has joined DNC </span>'

    def ShowMessageHasLeft (self, txt) :
        self.message_buffer += '<br> <span style="color : #FF00FF; font-weight: bold;"> '+  self.htmlToText(txt) +' has left DNC </span>'

    def ShowMessageNameChange (self, txt, txt2) :
        self.message_buffer += '<br> <span style="color : #FF00FF; font-weight: bold;"> '+  self.htmlToText(txt) +' is now : '+self.htmlToText(txt2)+' </span>'

    def UpdateChat(self) :
        if self.queueMsg  :
            m = self.queueMsg.pop(0)
            if  m :
                self.thread.start()
                self.ShowMessageAsText(m)
                self.ui.txtOutput.setText(self.message_buffer)
                sb = self.ui.txtOutput.verticalScrollBar()
                sb.setValue(sb.maximum())


    def questionMessage(self,name,fileN):    
        reply = QtGui.QMessageBox.question(self, "send file", "do you want to download the file : "+ ' '.join(fileN.split("/")[-1:])+" from "+name+" ?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No )
        
        if reply == QtGui.QMessageBox.Yes:
            self.openInputDialog(name, fileN)
            
    
        elif reply == QtGui.QMessageBox.No:
            print("hello")


    def openInputDialog(self, name, fileN):

        text, result = QtGui.QInputDialog.getText(self, "Port",
                                            "What is the port of the transfert ?")
        if result and text != "":
            print ("le port d'envoi est : " + text)

            cmdAccF = "/acceptfile "+name+" "+text+" "+fileN
            try:
                self.s.send(cmdAccF.encode())
                print(cmdAccF)
                self.portFile = text

            except timeout:
                self.ShowMessageErreur("Erreur : Timeout. Le serveur ne repond pas")
                self.ui.txtOutput.setText(self.message_buffer)
                sb = self.ui.txtOutput.verticalScrollBar()
                sb.setValue(sb.maximum())


            #	Command: /acceptfile 
            #Parameters: <nickname> <file> <ip> <port>


    def connectActions(self):
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
        menu = QtGui.QMenu()
        menu.addAction('Private discussion', lambda:self.FirstActionButtonA())
        menu.addAction('Send file', lambda:self.SecondActionButtonA())
        menu.exec_(QtGui.QCursor.pos())

    def FirstActionButtonA(self):
        test1 = self.ui.listNames.currentItem().text()
        print("1e fonction : "+str(test1))
        self.someMethod(str(test1))


    def SecondActionButtonA(self):
        test1 = self.ui.listNames.currentItem().text()
        print("2sd fonction : "+str(test1))
        self.privateFile = privateFile(self,self.s,str(test1))
        
        
    def someMethod(self,item):
        nom = item.replace("SUCC_INVITED","")
        cmdPM = "/askpm "+nom
        try:
            self.s.send(cmdPM.encode())
            self.demande = nom

        except timeout:
            self.ShowMessageErreur("Erreur : Timeout. Le serveur ne repond pas")
            self.ui.txtOutput.setText(self.message_buffer)
            sb = self.ui.txtOutput.verticalScrollBar()
            sb.setValue(sb.maximum())


    def away(self):

        if self.bouton == "disable" :
            cmdAway = "/disable "
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
            try:
                self.s.send(cmdAway.encode())
                self.ui.pushButton_5.setText("Away From Keyboard")

            except timeout:
                self.ShowMessageErreur("Erreur : Timeout. Le serveur ne repond pas")
                self.ui.txtOutput.setText(self.message_buffer)
                sb = self.ui.txtOutput.verticalScrollBar()
                sb.setValue(sb.maximum())


    def changeN(self):
        changePseudo = self.ui.lineEdit_2.text()
        cmdChange = "/name "+changePseudo
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

        ip= self.ui.lineEdit_4.text()
        port = int(self.ui.lineEdit_3.text())
        Addr = (ip,port)


        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.connect(Addr)
        self.thread.setConfig(self.s,self)
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
        quitter = "/quit"
        self.s.send(quitter.encode())
        #self.s.close()
        self.ui.lineEdit.setDisabled(True)
        self.ui.pushButton.setDisabled(True)
        self.ui.pushButton_2.setDisabled(False)
        self.ui.pushButton_3.setDisabled(True)
        self.ui.pushButton_6.setDisabled(True)

        self.ui.lineEdit_4.setDisabled(False)
        self.ui.lineEdit_3.setDisabled(False)

    def ecoute(self):
        while 1 :
            data = self.s.recv(4096)
            if not data :
                break
            messgServeur = (data.decode())


            if messgServeur == "ERR_INVALID_NICKNAME" :
                self.pseudo = "INVALID_NICKNAME"


            self.UpdateChat(messgServeur)


    def createWidgets(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ano = "anonymous" + ''.join(str(random.randint(1,9)) for _ in range(2))

        config = configparser.ConfigParser()

        config.read("dncClient.conf")

        port = config.get("NETWORK", "port")
        ip =  config.get("NETWORK", "ip")
        name = config.get("PSEUDO", "name")

        if name is not None :
            self.ui.lineEdit_2.setText(name)
        else :
            self.ui.lineEdit_2.setText(ano)

        if ip is not None :
            self.ui.lineEdit_4.setText(ip)


        if port is not None :
            self.ui.lineEdit_3.setText(port)




        self.ui.lineEdit.setDisabled(True)
        self.ui.pushButton.setDisabled(True)
        self.ui.pushButton_3.setDisabled(True)
        self.ui.pushButton_6.setDisabled(True)
        self.message_buffer = ""
        self.bouton = "disable"

        self.connectActions()



    def client(self):

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

                if self.cmd.split(" ")[0]=="/askpm":
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
    sys.exit(app.exec_())
    for t in threading.enumerate():
        if t != threading.main_thread(): t.join()
