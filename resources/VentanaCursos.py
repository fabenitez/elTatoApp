import sys
import datetime
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QTableWidgetItem
from PyQt5 import uic, QtGui
from PyQt5.QtCore import QDate
from resources.model_sqlite import Model
import pathlib
from pathlib import Path


class VentanaCursos(QDialog):

	
	def __init__(self):
		QDialog.__init__(self)
		pathAbsolute = str(pathlib.Path().absolute()) 
		uic.loadUi(pathAbsolute + "\\interfaces\\dlgCursos.ui", self) #uso archivo generado en designer
		self.iconV = QtGui.QIcon()
		self.iconV.addPixmap(QtGui.QPixmap(pathAbsolute + "\\resources\\elTato.ico"),QtGui.QIcon.Normal, QtGui.QIcon.On)
		self.setWindowIcon(self.iconV)
		self.cbboxAnio.currentIndexChanged.connect(self.cargaConfiguracionGuardada)
		

		############ ajuste de objetos en la primer visualizacion
		anio_inicio = QDate.currentDate().year() - 1
		aniosList = [str(anio_inicio), str(anio_inicio + 1), str(anio_inicio + 2)]
		self.cbboxAnio.addItems(aniosList)
								
		############ funcionalidad BOTONES #########################
		self.pbGuardarCursos.clicked.connect(self.guardaConfiguracion)
		
	def habilitaGuardar(self):
		self.pbGuardarCursos.setEnabled(True)
				
	def cargaConfiguracionGuardada(self):

		respuesta = Model().traeConfigCursos(self.cbboxAnio.currentText())
		estado = []
		if len(respuesta) == 0:
			respuesta = Model().generaConfigCursos(self.cbboxAnio.currentText())

		#se convierten estados 0 o 1 en True o False

		for fila in respuesta:
			for columna in fila:
				for dato in columna:
					if dato == "1":
						estado.append(True)
					else:
						estado.append(False)
		
		#Turno Maniana
		self.cbM1A.setChecked(estado[0])
		self.cbM1B.setChecked(estado[1])
		self.cbM1C.setChecked(estado[2])

		self.cbM2A.setChecked(estado[3])
		self.cbM2B.setChecked(estado[4])
		self.cbM2C.setChecked(estado[5])

		self.cbM3A.setChecked(estado[6])
		self.cbM3B.setChecked(estado[7])
		self.cbM3C.setChecked(estado[8])

		#Turno Tarde
		self.cbT1A.setChecked(estado[9])
		self.cbT1B.setChecked(estado[10])
		self.cbT1C.setChecked(estado[11])

		self.cbT2A.setChecked(estado[12])
		self.cbT2B.setChecked(estado[13])
		self.cbT2C.setChecked(estado[14])

		self.cbT3A.setChecked(estado[15])
		self.cbT3B.setChecked(estado[16])
		self.cbT3C.setChecked(estado[17])

		#self.pbGuardarCursos.setEnabled(False)

	def guardaConfiguracion(self):


		anio = self.cbboxAnio.currentText()
		#Turno Maniana
		turno = "MAÑANA"
		
		nivel = "1"
		if self.cbM1A.isChecked(): cursos = "1" 
		else: cursos = "0"
		if self.cbM1B.isChecked(): cursos += "1" 
		else: cursos += "0"
		if self.cbM1C.isChecked(): cursos += "1" 
		else: cursos += "0"
		Model().configuraCursos(anio, turno, nivel, cursos)

		nivel = "2"
		if self.cbM2A.isChecked(): cursos = "1" 
		else: cursos = "0"
		if self.cbM2B.isChecked(): cursos += "1" 
		else: cursos += "0"
		if self.cbM2C.isChecked(): cursos += "1" 
		else: cursos += "0"
		Model().configuraCursos(anio, turno, nivel, cursos)

		nivel = "3"
		if self.cbM3A.isChecked(): cursos = "1" 
		else: cursos = "0"
		if self.cbM3B.isChecked(): cursos += "1" 
		else: cursos += "0"
		if self.cbM3C.isChecked(): cursos += "1" 
		else: cursos += "0"
		Model().configuraCursos(anio, turno, nivel, cursos)

		#Turno Tarde
		turno = "TARDE"

		nivel = "1"
		if self.cbT1A.isChecked(): cursos = "1" 
		else: cursos = "0"
		if self.cbT1B.isChecked(): cursos += "1" 
		else: cursos += "0"
		if self.cbT1C.isChecked(): cursos += "1" 
		else: cursos += "0"
		Model().configuraCursos(anio, turno, nivel, cursos)

		nivel = "2"
		if self.cbT2A.isChecked(): cursos = "1" 
		else: cursos = "0"
		if self.cbT2B.isChecked(): cursos += "1" 
		else: cursos += "0"
		if self.cbT2C.isChecked(): cursos += "1" 
		else: cursos += "0"
		Model().configuraCursos(anio, turno, nivel, cursos)

		nivel = "3"
		if self.cbT3A.isChecked(): cursos = "1" 
		else: cursos = "0"
		if self.cbT3B.isChecked(): cursos += "1" 
		else: cursos += "0"
		if self.cbT3C.isChecked(): cursos += "1" 
		else: cursos += "0"
		Model().configuraCursos(anio, turno, nivel, cursos)

		#self.cbboxAnio.setEnabled(True)

"""
app=QApplication(sys.argv)

# Crear un objeto de la clase
ventana=VentanaCursos()
# Mostrar ventana
ventana.show()

# Ejecutar la aplicacion
app.exec_()
"""