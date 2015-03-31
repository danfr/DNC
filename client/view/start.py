from mainWindow import Ui_Dialog
from PyQt4 import QtGui, QtCore
import datetime
import time
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


    def ShowMessageAsText(self, txt):
        self.message_buffer += '\n' + self.getTimeStamp() + txt


    def createWidgets(self):
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.message_buffer = ""
        self.ShowMessageAsText("coucou ! comment ça va ?")
        self.ShowMessageAsText("ce site est une turie !")
        self.ShowMessageAsText("super et toi ?")
        self.ShowMessageAsText("Yo les poulets !")
        self.ShowMessageAsText("coucou ! comment ça va ?")
        self.ShowMessageAsText("ce site est une turie !")
        self.ShowMessageAsText("super et toi ?")
        self.ShowMessageAsText("Yo les poulets !")
        self.ShowMessageAsText("coucou ! comment ça va ?")
        self.ShowMessageAsText("ce site est une turie !")
        self.ShowMessageAsText("super et toi ?")
        self.ShowMessageAsText("Yo les poulets !")
        self.ShowMessageAsText("coucou ! comment ça va ?")
        self.ShowMessageAsText("ce site est une turie !")
        self.ShowMessageAsText("super et toi ?")
        self.ShowMessageAsText("Yo les poulets !")
        self.ShowMessageAsText("coucou ! comment ça va ?")
        self.ShowMessageAsText("ce site est une turie !")
        self.ShowMessageAsText("super et toi ?")
        self.ShowMessageAsText("Yo les poulets !")
        self.ShowMessageAsText("coucou ! comment ça va ?")
        self.ShowMessageAsText("ce site est une turie !")
        self.ShowMessageAsText("super et toi ?")
        self.ShowMessageAsText("Yo les poulets !")

        self.connectActions()


        # self.UpdateMainDisplay()

        self.ui.txtOutput.setText(self.message_buffer)

    def connectActions(self):
        self.ui.pushButton_2.clicked.connect(self.connecter)
        self.ui.pushButton_3.clicked.connect(self.deco)
        self.ui.pushButton.clicked.connect(self.client)

    def connecter(self):
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.connect(Addr)

    def deco(self):
        self.s.close()

    def client(self):

        cmd = self.ui.lineEdit.text()
        self.ui.lineEdit.setText('')
        if cmd.lower() == "quit":
            exit(0)
        try:
            self.s.send(cmd.encode())
            # data , addr = s.recvfrom(4096)
            # print(data.decode())
        except timeout:
            print("Erreur : Timeout. Le serveur ne repond pas.")



if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    myapp = start()
    myapp.show()
    myapp.focusWidget()
    sys.exit(app.exec_())
