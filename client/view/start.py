from mainWindow import Ui_Dialog
from PyQt4 import QtGui, QtCore
from PySide.QtCore import *
from PySide.QtGui import *
import time, threading, datetime, time, random,re
from socket import *
from pm import Ui_Form
Host = "127.0.0.1"
Port = 2222

#def selectFile():
#    lineEdit.setText(QFileDialog.getOpenFileName())

#pushButton.clicked.connect(selectFile)


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
                        
class privateMessage () :
   def __init__(self,main):

        #self.queueMsg= []
        #self.thread = MyThread()
        #self.thread.finished.connect(self.UpdateChat)
        
        self.main = main
        self.g = QtGui.QWidget()
        self.ui = Ui_Form()
        self.ui.setupUi(self.g)
        self.g.show()
        
        def selectFile():
            self.ui.lineEdit.setText(''.join(QFileDialog.getOpenFileName()))

        self.ui.pushButton_2.clicked.connect(selectFile)

                        

class start(QtGui.QDialog):
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
        html = html.replace(':-)', '&#9786;')
        html = html.replace(':-(', '&#9785;')

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
        
        
        
        
        if txt.split(" ")[0] == "SUCC_INVITED" : 
             self.ShowMessageOK("invitation requested")
             
        if txt.split(" ")[0] == "ASKING_FOR_PM" : 
             self.ShowMessageOK("private discution from "+ txt.split(" ")[1] )
             #ouvrir fenetre !!!!
             self.admin = privateMessage(self)
          
             
        if txt.split(" ")[0] == "SUCCESSFUL_LOGOUT" : 
             self.ShowMessageOK("Sucessful logout !")
             
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
             
             
             #HAS_LEFT anonymous52 
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
            self.message_buffer += '<br><span style="color : grey"> ' + self.getTimeStamp() + '</span> <span style="color : red"> &#60; '+txt.split(" ")[1] +' &#62; </span> ' + self.htmlToText(' '.join(txt.split(" ")[2:])) + ''

        if txt == "SUCC_MESSAGE_SENDED" : 
            self.message_buffer += '<br><span style="color : grey"> ' + self.getTimeStamp() + '</span> <span style="color : red"> &#60; '+ self.pseudo +' &#62; </span> ' + self.htmlToText(self.cmd) + ''
            
        
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
        


    def connectActions(self):
        self.ui.pushButton_2.clicked.connect(self.connecter)
        self.ui.pushButton_3.clicked.connect(self.deco)
        self.ui.pushButton.clicked.connect(self.client)
        self.ui.pushButton_6.clicked.connect(self.changeN)
        
        self.ui.pushButton_5.clicked.connect(self.away)
        

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
        if ip is None or port is None :
            Addr = (Host, Port)
        else :
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
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        ano = "anonymous" + ''.join(str(random.randint(1,9)) for _ in range(2))
        self.ui.lineEdit_2.setText(ano)
        
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
