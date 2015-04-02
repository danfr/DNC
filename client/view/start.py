from mainWindow import Ui_Dialog
from PyQt4 import QtGui, QtCore
import time, threading, datetime
from socket import *

Host = "127.0.0.1"
Port = 2222
Addr = (Host, Port)


class start(QtGui.QDialog):
    def __init__(self):
        super(start, self).__init__()
        self.createWidgets()

    def getTimeStamp(self):
        return ('[%s] ' % str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%H:%M')))
        
    def htmlToText( self, html ):

        html = html.replace('<', '&#60;')
        html = html.replace('>', '&#62;')
        html = html.replace(':-)', '&#9786;')
        html = html.replace(':-(', '&#9785;')

        return html


    def ShowMessageAsText(self, txt):
        self.message_buffer += '<br><span style="color : grey"> ' + self.getTimeStamp() + '</span> <span style="color : red"> &#60;BOB&#62; </span> ' + self.htmlToText(txt) + ''
        
    def UpdateChat(self, messgServeur) :
        self.ShowMessageAsText(messgServeur)
        self.ui.txtOutput.setText(self.message_buffer)
        sb = self.ui.txtOutput.verticalScrollBar()
        sb.setValue(sb.maximum())

    def connectActions(self):
        self.ui.pushButton_2.clicked.connect(self.connecter)
        self.ui.pushButton_3.clicked.connect(self.deco)
        self.ui.pushButton.clicked.connect(self.client)

    def connecter(self):
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.connect(Addr)
        self.ui.lineEdit.setDisabled(False)
        self.ui.pushButton.setDisabled(False)
        self.ui.pushButton_2.setDisabled(True)
        self.ui.pushButton_3.setDisabled(False)
        
        #threading.Thread(target=self.ecoute).start()
        #for t in threading.enumerate():
        #    if t != threading.main_thread(): t.join()
        
    def deco(self):
        self.s.close()
        self.ui.lineEdit.setDisabled(True)
        self.ui.pushButton.setDisabled(True)
        self.ui.pushButton_2.setDisabled(False)
        
    def ecoute(self):
        while 1 :
            data = self.s.recv(4096)
            if not data :
                break
            messgServeur = (data.decode())
            self.UpdateChat(messgServeur)


    def createWidgets(self):
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        self.ui.lineEdit.setDisabled(True)
        self.ui.pushButton.setDisabled(True)
        self.ui.pushButton_3.setDisabled(True)
        self.message_buffer = ""
        self.connectActions()



    """
            try :
                while 1 :
                    data = self.s.recv(4096)
                    if not data :
                        break
                    messgServeur = (data.decode())
                    self.ShowMessageAsText(messgServeur)
                    self.ui.txtOutput.setText(self.message_buffer)
                self.s.close()
            except timeout:
                print("Erreur : Timeout. Le serveur ne repond pas.")
    """




    def client(self):

        cmd = self.ui.lineEdit.text()
        if cmd != "":
            self.ui.lineEdit.setText('')

            try:
                self.s.send(cmd.encode())
                data = self.s.recv(4096)
                messgServeur = (data.decode())
                self.UpdateChat(messgServeur)

                
            except timeout:
                print("Erreur : Timeout. Le serveur ne repond pas.")


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    myapp = start()
    myapp.show()
    myapp.focusWidget()
    sys.exit(app.exec_())
