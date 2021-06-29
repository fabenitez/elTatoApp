import sys
import datetime
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QTableWidgetItem
from PyQt5 import uic, QtGui
from PyQt5.QtCore import QDate
from resources.model_sqlite import Model
from resources.docente import Docente
from resources.dlgSeleccionMateria import SeleccionMateria
import pathlib
from pathlib import Path

class VentanaCargaDisponibilidad(QDialog):

	
	def __init__(self):
		QDialog.__init__(self)
		pathAbsolute = str(pathlib.Path().absolute())
		uic.loadUi(pathAbsolute + "\\interfaces\\dlgCargaDisponibilidad.ui", self) #uso archivo generado en designer
		self.iconV = QtGui.QIcon()
		self.iconV.addPixmap(QtGui.QPixmap(pathAbsolute + "\\resources\\elTato.ico"),QtGui.QIcon.Normal, QtGui.QIcon.On)
		self.setWindowIcon(self.iconV)
		
		############ ajuste de objetos en la primer visualizacion
		self.pbGuardaDisponibilidad.setEnabled(False)
		self.twDocentes.setColumnWidth(0,70) #ancho de DNI
		self.twDocentes.setColumnWidth(1,140) #ancho de apellido
		self.twDocentes.setColumnWidth(2,140) #ancho de nombre
		self.twMateriasElegidas.setColumnWidth(0,270)
		self.twMateriasElegidas.setColumnWidth(1,30)
		self.leBusqueda.setFocus(True)
		self.gbHoraElegir.setEnabled(False)
		#cargar combo box de años lectivos
		inicio = QDate.currentDate().year() - 1
		anios = [str(inicio), str(inicio + 1), str(inicio + 2)]
		self.cbAnioLectivo.addItems(anios)
								
		############ funcionalidad BOTONES #########################
		self.pbGuardaDisponibilidad.clicked.connect(self.guardaDisponibilidad)
		
		############ funcionalidad #########################
		self.leBusqueda.textChanged.connect(self.traeDocentes) #al modificar el LineEdit leBusqueda
		self.twDocentes.itemClicked.connect(self.seleccionaDocente) #al seleccionar item de la tabla twDocentes
		
	def limpiar(self): #limpia todos los line edits
		self.leBusqueda.setText("")
		self.twMateriasElegidas.setRowCount(0)

		self.limpiarHoras()	
		
		

	def limpiarHoras(self):
		self.cbLun1.setChecked(False)
		self.cbLun2.setChecked(False)
		self.cbLun3.setChecked(False)
		self.cbLun4.setChecked(False)

		self.cbMar1.setChecked(False)
		self.cbMar2.setChecked(False)
		self.cbMar3.setChecked(False)
		self.cbMar4.setChecked(False)

		self.cbMie1.setChecked(False)
		self.cbMie2.setChecked(False)
		self.cbMie3.setChecked(False)
		self.cbMie4.setChecked(False)

		self.cbJue1.setChecked(False)
		self.cbJue2.setChecked(False)
		self.cbJue3.setChecked(False)
		self.cbJue4.setChecked(False)

		self.cbVie1.setChecked(False)
		self.cbVie2.setChecked(False)
		self.cbVie3.setChecked(False)
		self.cbVie4.setChecked(False)
		self.gbHoraElegir.setEnabled(False)	
		self.lblDocente.setText("")
		
	
	def traeDocentes(self): #avisa que cambia a estado busqueda
			
		#carga tabla
		self.twDocentes.setRowCount(0)
		if len(self.leBusqueda.text()) > 1:
			datos=Model().selectBusquedaDocente(self.leBusqueda.text())
			self.twDocentes.setRowCount(len(datos))
			self.limpiarHoras()
			self.twMateriasElegidas.setRowCount(0)
			fila = 0
			for dato in datos:
				self.twDocentes.setItem(fila, 0, QTableWidgetItem(dato[0])) #columna dni
				self.twDocentes.setItem(fila, 1, QTableWidgetItem(dato[1])) #columna apellido
				self.twDocentes.setItem(fila, 2, QTableWidgetItem(dato[2])) #columna nombre
				fila += 1
		
	def seleccionaDocente(self):
		
		self.twDocentes.setCurrentCell(self.twDocentes.currentRow(), 0) #fuerzo la eleccion de la primera columna
		dniItem = self.twDocentes.selectedItems() #traigo el item seleccionado
		dni = dniItem[0].text()
		self.docente_select = Model().selectDocenteExacto(dni)
		self.leBusqueda.setText("")
				
		############ cargo Etiqueta #######################
		self.lblDocente.setText("PROFESOR: " + self.docente_select.getDNI() +" - "+ self.docente_select.getApellido() +" "+ self.docente_select.getNombre())
		self.cargaMateriasElegidas(dni)
		self.limpiarHoras
		self.pbGuardaDisponibilidad.setEnabled(True)
		self.gbHoraElegir.setEnabled(True)

		

	def cargaMateriasElegidas(self, dni):
		self.materiasElegidas=Model().selectMateriaDocente(dni)
		self.twMateriasElegidas.setRowCount(len(self.materiasElegidas))
		
		fila=0
		for dato in self.materiasElegidas:
			
			self.twMateriasElegidas.setItem(fila, 0, QTableWidgetItem(dato[1])) #columna materia
			self.twMateriasElegidas.setItem(fila, 1, QTableWidgetItem(str(dato[2])))
			fila += 1
		

	def guardaDisponibilidad(self):

		respuesta = QMessageBox.question(self, "Advertencia", "La disponibilidad no podrá modificarse\n DESEA GUARDAR?", QMessageBox.Yes | QMessageBox.No)

		if respuesta == QMessageBox.Yes:
			dni = self.docente_select.getDNI()
			anioLectivo = self.cbAnioLectivo.itemText(self.cbAnioLectivo.currentIndex())
			turno = self.cbTurno.itemText(self.cbTurno.currentIndex())

			if len(Model().verificaDispo([dni, anioLectivo, turno])) > 0:
				QMessageBox.information(self, "Error", "Ya se cargó la disponibilidad del profesor en el año y turno dado")
				self.limpiar()
			else:
				checks = [[self.cbLun1, self.cbLun2, self.cbLun3, self.cbLun4],
				[self.cbMar1, self.cbMar2, self.cbMar3, self.cbMar4],
				[self.cbMie1, self.cbMie2, self.cbMie3, self.cbMie4],
				[self.cbJue1, self.cbJue2, self.cbJue3, self.cbJue4],
				[self.cbVie1, self.cbVie2, self.cbVie3, self.cbVie4]]
			
				dias = ["lunes", "martes", "miercoles", "jueves", "viernes"]

				registros = []

				itDia = 0
				for chkdia in checks:
					itHora = 1
					for chkobj in chkdia:
						if chkobj.isChecked():
							registros.append([dni, anioLectivo, turno, dias[itDia], str(itHora)])
						itHora += 1
					itDia += 1


				try:
					Model().guardaDisponibilidad(registros)
					self.limpiar()
					self.gbHoraElegir.setEnabled(False)
				except sqlite3.IntegrityError:
					QMessageBox.information(self, "Error", "Ya se cargó la disponibilidad del profesor en el año y turno dado")

"""
app=QApplication(sys.argv)

# Crear un objeto de la clase
ventana=VentanaCargaDisponibilidad()
# Mostrar ventana
ventana.show()

# Ejecutar la aplicacion
app.exec_()
"""