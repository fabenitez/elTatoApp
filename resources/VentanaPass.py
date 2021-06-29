import sys
import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog
from PyQt5 import uic
from PyQt5.QtCore import QDate, Qt 
from resources.model_sqlite import Model
from PyQt5 import uic, QtWidgets, QtGui, QtCore
from resources.dlgValidPass import dlgValidPass
from resources.fechas import Fechas
import pathlib
from pathlib import Path


class VentanaPass(QDialog):

	NON_ACCESS = 0					#Sin Acceso
	NORMAL_USER = 1				#Acceso de operador basico
	ADMIN_USER = 2					#Acceso de Administrador
	
	__user = ""
	__access = NON_ACCESS


	def __init__(self):
		QDialog.__init__(self)
		pathAbsolute = str(pathlib.Path().absolute()) 
		uic.loadUi(pathAbsolute + "\\interfaces\\dlgVentanaPass.ui", self)
		self.pbOK.clicked.connect(self.__validaIngreso)
		self.iconV = QtGui.QIcon()
		self.iconV.addPixmap(QtGui.QPixmap(pathAbsolute + "\\resources\\elTato.ico"),QtGui.QIcon.Normal, QtGui.QIcon.On)
		self.setWindowIcon(self.iconV)


	def __validaIngreso(self):
		params=[self.leUsuario.text(),self.lePassword.text()]
		datos=Model().selectUsuarioPass(params)
		
		if len(datos)<1:
			QMessageBox.information(self, "Error en el acceso", "Combinacion de Usuario y Password Incorrecta")
			self.__user = "No Ingresado"
			self.__access = self.NON_ACCESS
			self.clearAll()
			self.leUsuario.setFocus(True)
		else:
			hoy=QDate.currentDate()
			vto=Fechas().aFecha(datos[0][3])
						
			if vto<=hoy:
				QMessageBox.information(self, "Contraseña Vencida", "Contraseña Vencida\nIngrese NUEVA password diferente a la anterior")
				dialogo = dlgValidPass(self.leUsuario.text())
				dialogo.exec_()


			self.__user = "No Ingresado"

			self.__user = datos[0][0]
			self.__access = datos[0][2]
			self.close()


	def getUser(self):
		return self.__user

	def getAccess(self):
		return self.__access

	def clearAll(self):
		self.leUsuario.setText("")
		self.lePassword.setText("")

"""
app=QApplication(sys.argv)

# Crear un objeto de la clase
ventana=VentanaPass()
# Mostrar ventana
ventana.show()

# Ejecutar la aplicacion
app.exec_()

"""