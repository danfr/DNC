from mainWindow import Ui_Dialog
from PyQt4 import QtGui, QtCore
import datetime
import time

class start(QtGui.QDialog):

    def __init__(self):
        super(start, self).__init__()
        self.createWidgets()

    def getTimeStamp(self):
        return ('[%s] ' % str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%H:%M')))


    def ShowMessageAsText( self, txt ):
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


        #self.UpdateMainDisplay()

        self.ui.txtOutput.setText(self.message_buffer)

    def connectActions(self):
        self.ui.pushButton_2.clicked.connect(self.admin)
        self.ui.pushButton.clicked.connect(self.client)





    #def client(self):
     #   self.hide()
      #  self.admin = mainUtilisateur(self)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    myapp = start()
    myapp.show()
    myapp.focusWidget()
    sys.exit(app.exec_())
