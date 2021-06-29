import sys
import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QTableWidgetItem
from PyQt5 import uic, QtGui
from resources.model_sqlite import Model
from resources.dlgValidPass import dlgValidPass
from PyQt5 import uic, QtWidgets, QtGui, QtCore
import pathlib
from pathlib import Path

class VentanaUsuarios(QDialog):

	"""
	Clase que abre ventana de Administracion de usuarios y le brinda funcionalidad
	"""
	usuario=""
	password=""
	minLenUsuario=6
	NON_ACCESS = 0					#Sin Acceso
	NORMAL_USER = 1				#Acceso de operador basico
	ADMIN_USER = 2					#Acceso de Administrador

	def __init__(self, usuarioActivo):
		QDialog.__init__(self)
		pathAbsolute = str(pathlib.Path().absolute())
		uic.loadUi(pathAbsolute + "\\interfaces\\dlgAdminUsuarios.ui", self) #uso archivo generado en designer
		self.iconV = QtGui.QIcon()
		self.iconV.addPixmap(QtGui.QPixmap(pathAbsolute + "\\resources\\elTato.ico"),QtGui.QIcon.Normal, QtGui.QIcon.On)
		self.setWindowIcon(self.iconV)
		self.pbBlanquearPass.setText("Generar\nPassword")
		self.usuarioActivo = usuarioActivo
		self.twUsuarios.setColumnWidth(0,150)
		self.clearAll()
		#self.gbAcceso.setEnabled(False)
		
		############ funcionalidad BOTONES #########################
		self.pbGuardar.clicked.connect(self.guardar)
		self.pbBlanquearPass.clicked.connect(self.blanquearPass)
		self.pbEliminar.clicked.connect(self.eliminarUsuario)

		############ funcionalidad #########################
		self.leUsuario.textChanged.connect(self.traeUsuarios)
		self.twUsuarios.itemSelectionChanged.connect(self.seleccionaItem)

	def guardar(self):
		fechaVenc=int((datetime.date.today()+datetime.timedelta(30)).strftime("%Y%m%d"))
		datos=Model().selectUsuarioExacto(self.leUsuario.text())
		acceso=self.traeAccesoRadioB()

		if self.leUsuario.text() == "sa":
			QMessageBox.information(self, "ADVERTENCIA", "No puede modificarse el usuario Administrador(sa)")
			self.leUsuario.setText("")
			self.password=""

		else:
			if len(datos)!=0: #mismo usuario es UPDATE
				if datos[0][1]==self.password:
					QMessageBox.information(self, "Error", "Igual a password anterior\nIngrese una diferente")
				elif self.password == "":
					QMessageBox.information(self, "Error", "Password Vacía")
				else:
					update=[self.password, acceso[0], fechaVenc, self.leUsuario.text() ]
					Model().updateUsuario(update)

					QMessageBox.information(self, "Usuario Actualizado", "Usuario : " +
					self.leUsuario.text() + "\nAcceso : " + acceso[1])
					self.leUsuario.setText("")
					self.password=""

			else: #es INSERT
				if self.leUsuario=="" or self.password=="":
					QMessageBox.information(self, "Error", "Debe proveerse Usuario\ny Password")
				elif len(self.leUsuario.text())<6:
					QMessageBox.information(self, "Error", "El usuario debe tener " +
						str(self.minLenUsuario) + " dígitos como mínimo")
				else:
					insert=[self.leUsuario.text(), self.password, acceso[0], fechaVenc]
					Model().insertUsuario(insert)
					QMessageBox.information(self, "Usuario Nuevo", "Usuario : " +
					self.leUsuario.text() + "\nAcceso : " + acceso[1])
					self.clearAll()
					self.password=""



	def traeAccesoRadioB(self):
		if self.rbOperador.isChecked():
			acceso=[self.NORMAL_USER,"Operador"]
		elif self.rbAdmin.isChecked():
			acceso=[self.ADMIN_USER,"Administrador"]
		return acceso

	def eliminarUsuario(self):
		if self.leUsuario.text() == "sa":
			QMessageBox.information(self, "ADVERTENCIA", "El Usuario Administrador" +
				"\nNo puede ser eliminado")
			self.clearAll()

		elif self.leUsuario.text() == self.usuarioActivo:
			QMessageBox.information(self, "ADVERTENCIA", "No puede eliminarse a sí mismo")
			self.clearAll()

		else:
			respuesta=QMessageBox.question(self, "Eliminar Usuario", "¿Desea eliminar el usuario\n" + 
				self.leUsuario.text() + "?", QMessageBox.Yes | QMessageBox.No)
			if  respuesta==QMessageBox.Yes:
				Model().eliminaUsuario(self.leUsuario.text())
				QMessageBox.information(self, "Eliminacion de Usuario", "Usuario\n" +
					self.leUsuario.text() + "\nEliminado")
				self.clearAll()


	def blanquearPass(self):
		dialogo = dlgValidPass(self.usuario)
		dialogo.exec_()
		self.password=dialogo.getPassword()


	def traeUsuarios(self):
		self.twUsuarios.setRowCount(0)
		if len(self.leUsuario.text()) > 1:
			datos=Model().selectUsuario(self.leUsuario.text())
			self.pbBlanquearPass.setText("Generar\nPassword")
			self.pbEliminar.setEnabled(False)
			self.twUsuarios.setRowCount(len(datos))
			fila=0
			for dato in datos:
				self.twUsuarios.setItem(fila, 0, QTableWidgetItem(dato[0]))
				fila += 1

	def clearAll(self):
		self.leUsuario.setText("")
		self.pbEliminar.setEnabled(False)
	
	def seleccionaItem(self):

		self.gbAcceso.setEnabled(True)
		seleccionado=self.twUsuarios.selectedItems()
		if len(seleccionado)>0:
			texto=seleccionado[0].text()
			datos=Model().selectUsuario(texto)
				
			if datos[0][2]==self.NORMAL_USER:
				self.rbOperador.setChecked(True)
			elif datos[0][2]==self.ADMIN_USER:
				self.rbAdmin.setChecked(True)
			else:
				self.rbOperador.setChecked(False)
				self.rbAdmin.setChecked(False)
		
			self.leUsuario.setText("")
			self.leUsuario.setText(texto)
			self.pbBlanquearPass.setText("Blanquear\nPassword")		
			self.pbEliminar.setEnabled(True)
			if self.leUsuario.text() == "sa":
				self.gbAcceso.setEnabled(False)

"""
app=QApplication(sys.argv)

# Crear un objeto de la clase
ventana=VentanaUsuarios("frank")
# Mostrar ventana
ventana.show()

# Ejecutar la aplicacion
app.exec_()
"""
