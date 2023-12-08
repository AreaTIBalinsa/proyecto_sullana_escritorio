# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\AproyectoSullana\ProyectoSullana_Escritorio\View\inicioSistema.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        MainWindow.setStyleSheet("background-color: rgb(254, 182, 26);\n"
"border-radius: 7px;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lblTituloPrincipal = QtWidgets.QLabel(self.centralwidget)
        self.lblTituloPrincipal.setGeometry(QtCore.QRect(535, 154, 850, 250))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(32)
        font.setBold(True)
        font.setWeight(75)
        self.lblTituloPrincipal.setFont(font)
        self.lblTituloPrincipal.setAlignment(QtCore.Qt.AlignCenter)
        self.lblTituloPrincipal.setWordWrap(True)
        self.lblTituloPrincipal.setObjectName("lblTituloPrincipal")
        self.imgVenta = QtWidgets.QLabel(self.centralwidget)
        self.imgVenta.setGeometry(QtCore.QRect(785, 504, 350, 250))
        self.imgVenta.setStyleSheet("border-color: rgb(0, 0, 0);\n"
"border: 2px solid black;\n"
"border-radius: 15px;\n"
"background-color: rgb(36, 211, 21);")
        self.imgVenta.setText("")
        self.imgVenta.setScaledContents(True)
        self.imgVenta.setWordWrap(True)
        self.imgVenta.setObjectName("imgVenta")
        self.lblVenta = QtWidgets.QLabel(self.centralwidget)
        self.lblVenta.setGeometry(QtCore.QRect(785, 794, 350, 40))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.lblVenta.setFont(font)
        self.lblVenta.setAlignment(QtCore.Qt.AlignCenter)
        self.lblVenta.setObjectName("lblVenta")
        self.lblSubTituloPrincipal = QtWidgets.QLabel(self.centralwidget)
        self.lblSubTituloPrincipal.setGeometry(QtCore.QRect(535, 404, 850, 60))
        font = QtGui.QFont()
        font.setFamily("Poppins SemiBold")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.lblSubTituloPrincipal.setFont(font)
        self.lblSubTituloPrincipal.setStyleSheet(" letter-spacing: 2px;\n"
"")
        self.lblSubTituloPrincipal.setAlignment(QtCore.Qt.AlignCenter)
        self.lblSubTituloPrincipal.setIndent(-1)
        self.lblSubTituloPrincipal.setObjectName("lblSubTituloPrincipal")
        self.lblmimizar = QtWidgets.QLabel(self.centralwidget)
        self.lblmimizar.setGeometry(QtCore.QRect(1840, 10, 30, 30))
        self.lblmimizar.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.lblmimizar.setText("")
        self.lblmimizar.setScaledContents(True)
        self.lblmimizar.setWordWrap(False)
        self.lblmimizar.setObjectName("lblmimizar")
        self.lblcerrar = QtWidgets.QLabel(self.centralwidget)
        self.lblcerrar.setGeometry(QtCore.QRect(1880, 10, 30, 30))
        self.lblcerrar.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lblcerrar.setAutoFillBackground(False)
        self.lblcerrar.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.lblcerrar.setText("")
        self.lblcerrar.setScaledContents(True)
        self.lblcerrar.setAlignment(QtCore.Qt.AlignCenter)
        self.lblcerrar.setWordWrap(False)
        self.lblcerrar.setIndent(-1)
        self.lblcerrar.setObjectName("lblcerrar")
        self.btnminimizar = QtWidgets.QPushButton(self.centralwidget)
        self.btnminimizar.setGeometry(QtCore.QRect(1840, 10, 30, 30))
        self.btnminimizar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnminimizar.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.btnminimizar.setText("")
        self.btnminimizar.setObjectName("btnminimizar")
        self.btnCerrar = QtWidgets.QPushButton(self.centralwidget)
        self.btnCerrar.setGeometry(QtCore.QRect(1880, 10, 30, 30))
        self.btnCerrar.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnCerrar.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.btnCerrar.setText("")
        self.btnCerrar.setObjectName("btnCerrar")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lblTituloPrincipal.setText(_translate("MainWindow", "SISTEMA INTEGRADO DE VENTA"))
        self.lblVenta.setText(_translate("MainWindow", "VENTA"))
        self.lblSubTituloPrincipal.setText(_translate("MainWindow", "PRESIONE ENTER PARA INICIAR :"))
