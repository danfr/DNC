# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pmWindow.ui'
#
# Created: Sun Apr 12 16:19:04 2015
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_Dialog2(object):
    def setupUi(self, Dialog2):
        Dialog2.setObjectName(_fromUtf8("Dialog2"))
        Dialog2.resize(605, 373)
        self.horizontalLayoutWidget_2 = QtGui.QWidget(Dialog2)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(50, 50, 531, 31))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButton_3 = QtGui.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        self.pushButton_4 = QtGui.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.horizontalLayout_2.addWidget(self.pushButton_4)
        self.horizontalLayoutWidget = QtGui.QWidget(Dialog2)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(50, 320, 531, 41))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lineEdit = QtGui.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        self.txtOutput = QtGui.QTextEdit(Dialog2)
        self.txtOutput.setGeometry(QtCore.QRect(50, 80, 531, 231))
        self.txtOutput.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(14)
        font.setItalic(False)
        self.txtOutput.setFont(font)
        self.txtOutput.setFocusPolicy(QtCore.Qt.NoFocus)
        self.txtOutput.setAcceptDrops(False)
        self.txtOutput.setFrameShape(QtGui.QFrame.NoFrame)
        self.txtOutput.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.txtOutput.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.txtOutput.setObjectName(_fromUtf8("txtOutput"))
        self.horizontalLayoutWidget_3 = QtGui.QWidget(Dialog2)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(50, 10, 531, 41))
        self.horizontalLayoutWidget_3.setObjectName(_fromUtf8("horizontalLayoutWidget_3"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_4.setMargin(0)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label = QtGui.QLabel(self.horizontalLayoutWidget_3)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_4.addWidget(self.label)
        self.label_2 = QtGui.QLabel(self.horizontalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_4.addWidget(self.label_2)

        self.retranslateUi(Dialog2)
        QtCore.QMetaObject.connectSlotsByName(Dialog2)

    def retranslateUi(self, Dialog2):
        Dialog2.setWindowTitle(_translate("Dialog2", "Dialog", None))
        self.pushButton_3.setText(_translate("Dialog2", "Accept", None))
        self.pushButton_4.setText(_translate("Dialog2", "Refuse", None))
        self.pushButton.setText(_translate("Dialog2", "Send message", None))
        self.txtOutput.setHtml(_translate("Dialog2", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Arial\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Inconsolata\';\"><br /></p></body></html>", None))
        self.label.setText(_translate("Dialog2", "Private Discussion with :", None))
        self.label_2.setText(_translate("Dialog2", "TextLabel", None))

