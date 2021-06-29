import sys
import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QTableWidgetItem
from PyQt5 import uic, QtGui
from PyQt5.QtCore import QDate
from resources.model_sqlite import Model
import pathlib
from pathlib import Path

class VentanaAdminMaterias(QDialog):

	
	def __init__(self):
		QDialog.__init__(self)
		pathAbsolute = str(pathlib.Path().absolute())
		uic.loadUi(pathAbsolute + "\\interfaces\\dlgAdminMaterias.ui", self) #uso archivo generado en designer
		self.iconV = QtGui.QIcon()
		self.iconV.addPixmap(QtGui.QPixmap(pathAbsolute + "\\resources\\elTato.ico"),QtGui.QIcon.Normal, QtGui.QIcon.On)
		self.setWindowIcon(self.iconV)
		
		############ se cargan combo boxes #########################
		niveles = ["1","2","3"]
		horasCatedra = ["1","2","3","4","5","6"]
		self.cbNivel.addItems(niveles)
		self.cbHsCatedra.addItems(horasCatedra)
		self.twMaterias.setColumnWidth(0,200) #ancho materia
		self.twMaterias.setColumnWidth(1,70) #ancho nivel
		self.twMaterias.setColumnWidth(2,70) #ancho hscatedra
		self.cargaTablaMaterias()
		self.lblEstado.setText("ALTA MATERIA")


        ############ funcionalidad BOTONES #########################
		self.pbGuardaMateria.clicked.connect(self.guardaMateria)
		self.pbAlta.clicked.connect(self.cambiaEstadoAlta)
				
		############ funcionalidad #########################
		self.leBusqueda.textChanged.connect(self.traeMaterias)
		self.twMaterias.itemSelectionChanged.connect(self.seleccionaMateria)
			
	def cambiaEstadoAlta(self):
		self.lblEstado.setText("ALTA MATERIA")
		self.leMateria.setText("")

	def cargaTablaMaterias(self):
		self.twMaterias.setRowCount(0)
		self.materiasTabla = Model().selectMaterias()
		self.twMaterias.setRowCount(len(self.materiasTabla))
		fila = 0
		for dato in self.materiasTabla:
			self.twMaterias.setItem(fila, 0, QTableWidgetItem(dato[1])) #columna materia
			self.twMaterias.setItem(fila, 1, QTableWidgetItem(str(dato[2]))) #columna nivel
			self.twMaterias.setItem(fila, 2, QTableWidgetItem(str(dato[3]))) #columna hscatedra
			fila += 1

	def seleccionaMateria(self):
		filaTabla = self.twMaterias.currentRow()
		self.materiaElegida = self.materiasTabla[filaTabla]
		self.leMateria.setText(self.materiaElegida[1])
		self.cbNivel.setItemText(0, str(self.materiaElegida[2]))
		self.cbHsCatedra.setItemText(0, str(self.materiaElegida[3]))
		self.lblEstado.setText("MODIFICA MATERIA")


	def traeMaterias(self):
		
		if len(self.leBusqueda.text()) > 1:
			self.twMaterias.setRowCount(0)
			self.materiasTabla = Model().selectMateriasPorNombreLike(self.leBusqueda.text().upper())
			self.twMaterias.setRowCount(len(self.materiasTabla))

			fila=0
			for dato in self.materiasTabla:
				self.twMaterias.setItem(fila, 0, QTableWidgetItem(dato[1])) #columna materia
				self.twMaterias.setItem(fila, 1, QTableWidgetItem(str(dato[2]))) #columna nivel
				self.twMaterias.setItem(fila, 2, QTableWidgetItem(str(dato[3]))) #columna hscatedra
				fila += 1

	def limpiar(self): #limpia todos los line edits
		self.leMateria.setText("")
		self.lblEstado.setText("ALTA MATERIA")
		self.leMateria.setText("")
		self.cbNivel.setItemText(0, "1")
		self.cbHsCatedra.setItemText(0, "1")

	def guardaMateria(self):
		if self.leMateria.text() == "":
			QMessageBox.warning(self, "Advertencia", "Debe proporcionar un nombre de Materia")
		elif self.lblEstado.text() == "MODIFICA MATERIA":
			id_materia = self.materiaElegida[0]
			registro = [id_materia, self.leMateria.text().upper(), self.cbNivel.currentText(), self.cbHsCatedra.currentText()]
			Model().actualizaMateria(registro)
			self.cargaTablaMaterias()
			self.limpiar()
			
		elif self.lblEstado.text() == "ALTA MATERIA":
			self.agregaMateria()
			self.limpiar()
			
	
	def agregaMateria(self):
 
		#genera lista para pasar como registro
		registroMateria = [self.leMateria.text().upper(), self.cbNivel.currentText(), self.cbHsCatedra.currentText()] 
		if self.leMateria.text() == "":
			QMessageBox.warning(self, "Advertencia", "Debe proporcionar un nombre de Materia")
		else:
			resultado = Model().selectMateriaExacta(registroMateria)
			if len(resultado) > 0:
				QMessageBox.warning(self, "Advertencia", "Ese nombre de Materia ya existe con Nivel y Horas Cátedra")
			else:	
				Model().agregaMateria(registroMateria)
			self.limpiar()
			self.cargaTablaMaterias()

"""
app=QApplication(sys.argv)

# Crear un objeto de la clase
ventana=VentanaAdminMaterias()
# Mostrar ventana
ventana.show()

# Ejecutar la aplicacion
app.exec_()
"""