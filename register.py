# Form implementation generated from reading ui file 'register.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_registration(object):
    def setupUi(self, registration):
        registration.setObjectName("registration")
        registration.resize(552, 397)
        self.centralwidget = QtWidgets.QWidget(registration)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 70, 231, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(0, 130, 231, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.regbtn = QtWidgets.QPushButton(self.centralwidget)
        self.regbtn.setGeometry(QtCore.QRect(170, 270, 131, 71))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.regbtn.setFont(font)
        self.regbtn.setObjectName("regbtn")
        self.new_login = QtWidgets.QLineEdit(self.centralwidget)
        self.new_login.setGeometry(QtCore.QRect(190, 80, 231, 41))
        self.new_login.setObjectName("new_login")
        self.new_pass = QtWidgets.QLineEdit(self.centralwidget)
        self.new_pass.setGeometry(QtCore.QRect(190, 140, 231, 41))
        self.new_pass.setObjectName("new_pass")
        registration.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(registration)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 552, 21))
        self.menubar.setObjectName("menubar")
        registration.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(registration)
        self.statusbar.setObjectName("statusbar")
        registration.setStatusBar(self.statusbar)

        self.retranslateUi(registration)
        QtCore.QMetaObject.connectSlotsByName(registration)

    def retranslateUi(self, registration):
        _translate = QtCore.QCoreApplication.translate
        registration.setWindowTitle(_translate("registration", "Окно регистрации"))
        self.label.setText(_translate("registration", "Введите логин:"))
        self.label_2.setText(_translate("registration", "Введите пароль:"))
        self.regbtn.setText(_translate("registration", "OK"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    registration = QtWidgets.QMainWindow()
    ui = Ui_registration()
    ui.setupUi(registration)
    registration.show()
    sys.exit(app.exec())