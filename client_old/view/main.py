# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 567)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("../img/42.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.txtOutput = QtGui.QTextEdit(self.centralwidget)
        self.txtOutput.setGeometry(QtCore.QRect(14, 151, 100, 361))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtOutput.sizePolicy().hasHeightForWidth())
        self.txtOutput.setSizePolicy(sizePolicy)
        self.txtOutput.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(14)
        font.setItalic(False)
        self.txtOutput.setFont(font)
        self.txtOutput.setFocusPolicy(QtCore.Qt.NoFocus)
        self.txtOutput.setAcceptDrops(False)
        self.txtOutput.setStyleSheet(_fromUtf8("      position: relative;\n"
"      border-radius: 2px;\n"
"      font-size: 0.9em;\n"
"background-color: #FAFAFA;\n"
"      color: #646464;"))
        self.txtOutput.setFrameShape(QtGui.QFrame.NoFrame)
        self.txtOutput.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.txtOutput.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.txtOutput.setObjectName(_fromUtf8("txtOutput"))
        self.horizontalLayoutWidget_2 = QtGui.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 40, 781, 51))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_3 = QtGui.QLabel(self.horizontalLayoutWidget_2)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_2.addWidget(self.label_3)
        self.lineEdit_4 = QtGui.QLineEdit(self.horizontalLayoutWidget_2)
        self.lineEdit_4.setStyleSheet(_fromUtf8("    border: solid 1px #ccc;\n"
"    font-size:15px;\n"
"    background-color:rgb(255, 255, 255);"))
        self.lineEdit_4.setInputMask(_fromUtf8(""))
        self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))
        self.horizontalLayout_2.addWidget(self.lineEdit_4)
        self.label_4 = QtGui.QLabel(self.horizontalLayoutWidget_2)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_2.addWidget(self.label_4)
        self.lineEdit_3 = QtGui.QLineEdit(self.horizontalLayoutWidget_2)
        self.lineEdit_3.setStyleSheet(_fromUtf8("    border: solid 1px #ccc;\n"
"    font-size:15px;\n"
"    background-color:rgb(255, 255, 255);"))
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.horizontalLayout_2.addWidget(self.lineEdit_3)
        self.label_5 = QtGui.QLabel(self.horizontalLayoutWidget_2)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_2.addWidget(self.label_5)
        self.lineEdit_2 = QtGui.QLineEdit(self.horizontalLayoutWidget_2)
        self.lineEdit_2.setStyleSheet(_fromUtf8("    border: solid 1px #ccc;\n"
"    font-size:15px;\n"
"    background-color:rgb(255, 255, 255);"))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.horizontalLayout_2.addWidget(self.lineEdit_2)
        self.pushButton_6 = QtGui.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_6.setStyleSheet(_fromUtf8("\n"
"  vertical-align: top;\n"
"  color: white;\n"
"  text-align: center;\n"
"  background: #3498db;\n"
"  border: 0;\n"
"  border-bottom: 2px solid #2a8bcc;\n"
"  padding: 2px 10px 2px 10px;\n"
""))
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.horizontalLayout_2.addWidget(self.pushButton_6)
        self.pushButton_3 = QtGui.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_3.setStyleSheet(_fromUtf8("\n"
"  vertical-align: top;\n"
"  color: white;\n"
"  text-align: center;\n"
"  background: #3498db;\n"
"  border: 0;\n"
"  border-bottom: 2px solid #2a8bcc;\n"
"  padding: 2px 10px 2px 10px;"))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        self.pushButton_2 = QtGui.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_2.setStyleSheet(_fromUtf8("\n"
"  vertical-align: top;\n"
"  color: white;\n"
"  text-align: center;\n"
"  background: #3498db;\n"
"  border: 0;\n"
"  border-bottom: 2px solid #2a8bcc;\n"
"  padding: 2px 10px 2px 10px;"))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 520, 781, 41))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lineEdit = QtGui.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit.setStyleSheet(_fromUtf8("    border: solid 1px #ccc;\n"
"    font-size:20px;\n"
"    background-color:rgb(255, 255, 255);"))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setStyleSheet(_fromUtf8("QPushButton {\n"
"  vertical-align: top;\n"
"  color: white;\n"
"  text-align: center;\n"
"  background: #3498db;\n"
"  border: 0;\n"
"  padding: 2px 10px 2px 10px;\n"
"  border-bottom: 2px solid #2a8bcc;\n"
"}\n"
"\n"
"QPushButton : !enabled { \n"
"\n"
"  vertical-align: top;\n"
"  color: white;\n"
"  text-align: center;\n"
"  background: rgb(255, 255, 255);\n"
"  border: 0;\n"
"  border-bottom: 2px solid #2a8bcc;\n"
"\n"
"}"))
        self.pushButton.setInputMethodHints(QtCore.Qt.ImhNone)
        self.pushButton.setDefault(False)
        self.pushButton.setFlat(False)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        self.horizontalLayoutWidget_3 = QtGui.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(10, 100, 561, 40))
        self.horizontalLayoutWidget_3.setObjectName(_fromUtf8("horizontalLayoutWidget_3"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.pushButton_5 = QtGui.QPushButton(self.horizontalLayoutWidget_3)
        self.pushButton_5.setStyleSheet(_fromUtf8("\n"
"  vertical-align: top;\n"
"  color: white;\n"
"  text-align: center;\n"
"  background: #3498db;\n"
"  border: 0;\n"
"  border-bottom: 2px solid #2a8bcc;\n"
"  padding: 2px 10px 2px 10px;"))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.horizontalLayout_3.addWidget(self.pushButton_5)
        self.verticalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(590, 100, 201, 411))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.listNames = QtGui.QListWidget(self.verticalLayoutWidget)
        self.listNames.setMinimumSize(QtCore.QSize(50, 0))
        self.listNames.setMaximumSize(QtCore.QSize(200, 16777215))
        self.listNames.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Cantarell"))
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.listNames.setFont(font)
        self.listNames.setFocusPolicy(QtCore.Qt.NoFocus)
        self.listNames.setAcceptDrops(False)
        self.listNames.setStyleSheet(_fromUtf8("\n"
"      position: relative;\n"
"      border-radius: 2px;\n"
"      font-size: 0.9em;\n"
"background-color: #DEDEDE;\n"
"      color: #646464;"))
        self.listNames.setFrameShape(QtGui.QFrame.NoFrame)
        self.listNames.setFrameShadow(QtGui.QFrame.Sunken)
        self.listNames.setLineWidth(1)
        self.listNames.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.listNames.setObjectName(_fromUtf8("listNames"))
        self.verticalLayout.addWidget(self.listNames)
        self.listNames_2 = QtGui.QListWidget(self.verticalLayoutWidget)
        self.listNames_2.setMinimumSize(QtCore.QSize(50, 0))
        self.listNames_2.setMaximumSize(QtCore.QSize(200, 16777215))
        self.listNames_2.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Cantarell"))
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStrikeOut(True)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.listNames_2.setFont(font)
        self.listNames_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.listNames_2.setAcceptDrops(False)
        self.listNames_2.setStyleSheet(_fromUtf8("      position: relative;\n"
"      border-radius: 2px;\n"
"      font-size: 0.9em;\n"
"background-color: #DEDEDE;\n"
"      color: #646464;"))
        self.listNames_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.listNames_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.listNames_2.setLineWidth(1)
        self.listNames_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.listNames_2.setObjectName(_fromUtf8("listNames_2"))
        self.verticalLayout.addWidget(self.listNames_2)
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(748, 6, 41, 41))
        self.label_6.setText(_fromUtf8(""))
        self.label_6.setPixmap(QtGui.QPixmap(_fromUtf8("../img/42.png")))
        self.label_6.setScaledContents(True)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.webView = QtWebKit.QWebView(self.centralwidget)
        self.webView.setGeometry(QtCore.QRect(125, 149, 456, 360))
        self.webView.setObjectName(_fromUtf8("webView"))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.txtOutput.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Arial\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Inconsolata\';\"><br /></p></body></html>", None))
        self.label_3.setText(_translate("MainWindow", "IP : ", None))
        self.lineEdit_4.setText(_translate("MainWindow", "127.0.0.1", None))
        self.label_4.setText(_translate("MainWindow", "Port :", None))
        self.lineEdit_3.setText(_translate("MainWindow", "2222", None))
        self.label_5.setText(_translate("MainWindow", "Pseudo :", None))
        self.lineEdit_2.setText(_translate("MainWindow", "anonymous", None))
        self.pushButton_6.setText(_translate("MainWindow", "Change pseudo", None))
        self.pushButton_3.setText(_translate("MainWindow", "Disconnect", None))
        self.pushButton_2.setText(_translate("MainWindow", "Connect", None))
        self.label_2.setText(_translate("MainWindow", "Welcome to DNC42", None))
        self.pushButton.setText(_translate("MainWindow", "Send message", None))
        self.pushButton_5.setText(_translate("MainWindow", "Away From Keyboard", None))
        self.label.setText(_translate("MainWindow", "Nick list", None))
        self.listNames.setSortingEnabled(True)
        self.listNames_2.setSortingEnabled(True)

from PyQt4 import QtWebKit
