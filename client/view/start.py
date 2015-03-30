from irc import Ui_Dialog
from PyQt4 import QtGui, QtCore

class start(QtGui.QDialog):

    def __init__(self):
        super(start, self).__init__()
        self.createWidgets()

    def createWidgets(self):
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        #self.connectActions()

    def connectActions(self):
        self.ui.pushButton_2.clicked.connect(self.admin)
        self.ui.pushButton.clicked.connect(self.client)

    def admin(self):
        self.hide()
        self.admin = mainAdmin(self)

    def client(self):
        self.hide()
        self.admin = mainUtilisateur(self)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    myapp = start()
    myapp.show()
    myapp.focusWidget()
    sys.exit(app.exec_())
