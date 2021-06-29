# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dlgValidPass.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QLineEdit, QMessageBox
from PyQt5.QtCore import QDate, Qt 
from resources.Logger import ValidPassword
from resources.model_sqlite import Model
import datetime
import pathlib
from pathlib import Path


class dlgValidPass(QDialog):

    minLenPass = 6
    levelPass = ValidPassword.WEAK_PASS #modificar si se quiere una mayor seguridad
    valPass = False
    valComp = False
    usuario = ""
    password = ""

    def __init__(self, usuario):
        QDialog.__init__(self)
        self.usuario = usuario
        self.setupUi(self)
        pathAbsolute = str(pathlib.Path().absolute()) 
        self.iconV = QtGui.QIcon()
        self.iconV.addPixmap(QtGui.QPixmap(pathAbsolute + "\\resources\\elTato.ico"),QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.setWindowIcon(self.iconV)
       

    def setupUi(self, dlgValidPass):
        self.logger=ValidPassword(self.minLenPass, self.levelPass)

        dlgValidPass.setObjectName("dlgValidPass")
        dlgValidPass.resize(387, 225)
        dlgValidPass.setMinimumSize(QtCore.QSize(387, 225))
        dlgValidPass.setMaximumSize(QtCore.QSize(387, 225))
        self.lblTitulo = QtWidgets.QLabel(dlgValidPass)
        self.lblTitulo.setGeometry(QtCore.QRect(80, 40, 221, 16))
        self.lblTitulo.setObjectName("lblTitulo")

        self.lePassword = QtWidgets.QLineEdit(dlgValidPass)
        self.lePassword.setGeometry(QtCore.QRect(170, 80, 113, 20))
        self.lePassword.setObjectName("lePassword")
        self.lePassword.setEchoMode(QLineEdit.Password)

        self.leComprobacion = QtWidgets.QLineEdit(dlgValidPass)
        self.leComprobacion.setGeometry(QtCore.QRect(170, 120, 113, 20))
        self.leComprobacion.setObjectName("leComprobacion")
        self.leComprobacion.setEchoMode(QLineEdit.Password)

        self.lblPassword = QtWidgets.QLabel(dlgValidPass)
        self.lblPassword.setGeometry(QtCore.QRect(110, 80, 51, 16))
        self.lblPassword.setObjectName("lblPassword")

        self.lblComprobacion = QtWidgets.QLabel(dlgValidPass)
        self.lblComprobacion.setGeometry(QtCore.QRect(90, 120, 71, 20))
        self.lblComprobacion.setObjectName("lblComprobacion")

        self.pbOK = QtWidgets.QPushButton(dlgValidPass)
        self.pbOK.setGeometry(QtCore.QRect(160, 170, 81, 31))
        self.pbOK.setObjectName("pbOK")

        self.retranslateUi(dlgValidPass)
        QtCore.QMetaObject.connectSlotsByName(dlgValidPass)
        self.lePassword.setText("")
        self.leComprobacion.setText("")

        #**************** EVENTOS **************************

        self.lePassword.textChanged.connect(self.validaPass)
        self.leComprobacion.textChanged.connect(self.validaComprobacion)
        self.pbOK.clicked.connect(self.accionOK)


    def retranslateUi(self, dlgValidPass):
        _translate = QtCore.QCoreApplication.translate
        dlgValidPass.setWindowTitle(_translate("dlgValidPass", "Nueva Password para : " + self.usuario))
        self.lblTitulo.setText(_translate("dlgValidPass", "Ingrese Password y repita para comprobación"))
        self.lblPassword.setText(_translate("dlgValidPass", "Password"))
        self.lblComprobacion.setText(_translate("dlgValidPass", "Comprobación"))
        self.pbOK.setText(_translate("dlgValidPass", "OK"))

    def validaPass(self):
        self.valPass=self.logger.validatePassword(self.lePassword.text())
        if self.valPass:
            self.lePassword.setStyleSheet("color: green;")
        else:
            self.lePassword.setStyleSheet("color: red;")
        
    def validaComprobacion(self):        
        if self.lePassword.text() == self.leComprobacion.text():
            self.leComprobacion.setStyleSheet("color: green;")
            self.valComp=True
        else:
            self.leComprobacion.setStyleSheet("color: red;")
            self.valComp=False

    def accionOK(self):        
        if self.valPass and self.valComp:
            self.password=self.leComprobacion.text()
            datos=Model().selectUsuarioExacto(self.usuario)
            vto=datetime.date.today() + datetime.timedelta(30)
            fecha=vto.strftime("%Y%m%d")
            print(fecha)
            if len(datos)>0: #usuario existe - se esta modificando pass
                if datos[0][1]==self.password: #password igual a la anterior
                    QMessageBox.warning(self, "Error en Password", "La password debe ser diferente a la anterior")
                else:
                    datosUpdate=[self.password, int(fecha), self.usuario]
                    Model().updatePassword(datosUpdate)
                    QMessageBox.information(self, "Password Actualizada", "Password actualizada correctamente")
                    self.close()
            else:
                self.close()
        elif not self.valPass:
            self.lePassword.setText("")
            self.leComprobacion.setText("")
            QMessageBox.warning(self, "Error en Password", "Password no cumple con los requerimientos")
        elif not self.valComp:
            self.leComprobacion.setText("")
            QMessageBox.warning(self, "Error en Comprobación", "Comprobación no es igual a Password")

    def getPassword(self):
        return self.password            

"""
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialogo = dlgValidPass('frank')
    dialogo.show()
    sys.exit(app.exec_())
"""