from mainWindow import Ui_Dialog
from PyQt4 import QtGui, QtCore
from PySide.QtCore import *
from PySide.QtGui import *
import time, threading, datetime, time, random,re
from socket import *
from pmWindow import Ui_Dialog2
import configparser



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
    def __init__(self,main,s, pmPerson, pmPerso):
       
        self.main = main
        self.s = s
        self.pmPerso = pmPerso
        self.pmPerson = pmPerson
        self.g = QtGui.QWidget()
        self.ui = Ui_Dialog2()
        self.ui.setupUi(self.g)
        self.g.show()
        old = start()
        self.message_buffer2 = ""

        self.queueMsg2= []
        self.thread = MyThread()
        self.thread.finished.connect(self.UpdateChatP)

        self.ui.pushButton.clicked.connect(self.send)
        self.ui.pushButton_3.clicked.connect(self.accept)
        self.ui.pushButton_2.clicked.connect(self.selectFile)
        self.ui.label_2.setText(pmPerson)

    def accept(self):
        self.cmAcc = "/acceptpm "+self.pmPerson
        try:
            self.s.send(self.cmAcc.encode())

        except timeout:
            self.ShowMessageErreur("Erreur : Timeout. Le serveur ne repond pas")
            self.ui.txtOutput.setText(self.message_buffer2)
            sb = self.ui.txtOutput.verticalScrollBar()
            sb.setValue(sb.maximum())
        
    def selectFile(self):
        self.ui.lineEdit.setText('/pmfile '+self.pmPerson+ ' '.join(QFileDialog.getOpenFileName()))

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
                #self.ui.txtOutput.setText(self.message_buffer2)
                #sb = self.ui.txtOutput.verticalScrollBar()
                #sb.setValue(sb.maximum())

    def getTimeStamp(self):
        return ('[%s] ' % str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%H:%M')))

    def ShowMessageAsTextPm(self, txt) :

            self.message_buffer2 += '<br><span style="color : grey">'+txt+'</span>'
            if txt.split(" ")[0] == "SUCC_PM_SENDED":
                self.message_buffer2 += '<br><span style="color : grey"> ' + self.getTimeStamp() + '</span> <span style="color : red"> &#60; '+self.pmPerso +' &#62; </span> ' + self.htmlToText(self.cmdP) + ''


            if txt.split(" ")[0] == "SUCC_PRIVATE_DISCUSSION_ACCEPTED":
                 self.message_buffer2 += '<br> <span style="color : green"> Chalange Accepted ! </span>'
  
            if txt.split(" ")[0] == "NEW_PM" :
                self.message_buffer2 += '<br><span style="color : grey"> ' + self.getTimeStamp() + '</span> <span style="color : red"> &#60; '+ self.pmPerso +' &#62; </span> ' + self.htmlToText(' '.join(txt.split(" ")[2:])) + ''


            self.ui.txtOutput.setText(self.message_buffer2)
            sb = self.ui.txtOutput.verticalScrollBar()
            sb.setValue(sb.maximum())

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
        
        
        
        if txt.split(" ")[0] == "SUCC_PRIVATE_DISCUSSION_ACCEPTED":
             self.message_buffer += '<br> <span style="color : green"> PRIVATE DISCUSSION ? challenge accepted ! '

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

        #if txt.split(" ")[0] == "SUCC_PM_SENDED":
        #    self.private
            

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
             
        if txt.split(" ")[0] == "ERR_INVALID_NICKNAME" :
            self.pseudo = "INVALID_NICKNAME"

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
        
        #self.connect(self.ui.listNames,
        #     QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem *)"),
        #     self.someMethod)
        self.ui.listNames.itemActivated.connect(self.someMethod)
               
    def someMethod(self,item):
        nom = item.text().replace("SUCC_INVITED","")
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
