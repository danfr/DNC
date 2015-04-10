# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pmFile.ui'
#
# Created: Fri Apr 10 16:31:47 2015
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

class Ui_Dialog3(object):
    def setupUi(self, Dialog3):
        Dialog3.setObjectName(_fromUtf8("Dialog3"))
        Dialog3.resize(612, 161)
        Dialog3.setMaximumSize(QtCore.QSize(612, 161))
        self.horizontalLayoutWidget = QtGui.QWidget(Dialog3)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 100, 531, 41))
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
        self.pushButton_2 = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.horizontalLayoutWidget_2 = QtGui.QWidget(Dialog3)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(30, 10, 391, 71))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.label_2 = QtGui.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)

        self.retranslateUi(Dialog3)
        QtCore.QMetaObject.connectSlotsByName(Dialog3)

    def retranslateUi(self, Dialog3):
        Dialog3.setWindowTitle(_translate("Dialog3", "Dialog", None))
        self.pushButton.setText(_translate("Dialog3", "Send message", None))
        self.pushButton_2.setText(_translate("Dialog3", "send file", None))
        self.label.setText(_translate("Dialog3", "Sending a file to : ", None))
        self.label_2.setText(_translate("Dialog3", "BobZorro", None))

