import sys
import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QTableWidgetItem
from PyQt5 import uic, QtWidgets, QtGui, QtCore 
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QDate, QRegExp
from resources.model_sqlite import Model
from resources.docente import Docente
from resources.dlgSeleccionMateria import SeleccionMateria
import pathlib
from pathlib import Path

class VentanaAltaDocentes(QDialog):

	
	def __init__(self):
		QDialog.__init__(self)
		pathAbsolute = str(pathlib.Path().absolute())
		uic.loadUi(pathAbsolute + "\\interfaces\\dlgAltaDocentes.ui", self) #uso archivo generado en designer
		
		############ ajuste de objetos en la primer visualizacion
		self.iconV = QtGui.QIcon()
		self.iconV.addPixmap(QtGui.QPixmap(pathAbsolute + "\\resources\\elTato.ico"),QtGui.QIcon.Normal, QtGui.QIcon.On)
		self.setWindowIcon(self.iconV)
		self.pbAgregarMateria.setEnabled(False)
		self.limpiarDocente()
		self.desactivaPantallaMateriasTelefonos()
		self.twMateriasAElegir.setColumnWidth(0,130)
		self.twMateriasAElegir.setColumnWidth(1,40)
		self.twMateriasElegidas.setColumnWidth(0,130)
		self.twMateriasElegidas.setColumnWidth(1,40)

        ############ funcionalidad BOTONES #########################
		self.pbAgregarTelefono.clicked.connect(self.agregaTelefono)
		self.pbAgregarMateria.clicked.connect(self.vinculaMateria)
		self.pbGuardarDocente.clicked.connect(self.guardaDocente)
		self.pbNuevoDocente.clicked.connect(self.nuevoDocente)
				
		############ funcionalidad #########################
		self.leDNI.editingFinished.connect(self.verificaDocente)
		self.twMateriasAElegir.itemClicked.connect(self.seleccionaMateriaElegir)
		

		self.leDNI.setMaxLength(9)
		self.leDNI.setClearButtonEnabled(True)
		self.leDNI.setValidator(QRegExpValidator(QRegExp("[0-9]+")))

		self.leApellido.setMaxLength(50)
		self.leApellido.setClearButtonEnabled(True)
		self.leApellido.setValidator(QRegExpValidator(QRegExp("[^0-9]+")))

		self.leNombre.setMaxLength(50)
		self.leNombre.setClearButtonEnabled(True)
		self.leNombre.setValidator(QRegExpValidator(QRegExp("[^0-9]+")))

		self.leDomicilio.setMaxLength(50)
		self.leDomicilio.setClearButtonEnabled(True)
		

		self.leLocalidad.setMaxLength(50)
		self.leLocalidad.setClearButtonEnabled(True)
		

		self.leCodigoPostal.setMaxLength(6)
		self.leCodigoPostal.setClearButtonEnabled(True)
		self.leCodigoPostal.setValidator(QRegExpValidator(QRegExp("[0-9]+")))

		self.leEMail.setMaxLength(50)
		self.leEMail.setClearButtonEnabled(True)

		#self.leEMail.setValidator(QRegExpValidator(QRegExp("^[a-zA-Z0-9\._-]+@[a-zA-Z0-9-]{2,}[.][a-zA-Z]{2,4}$")))


	
	def limpiarDocente(self): #limpia todos los line edits
		self.leDNI.setText("")
		self.leApellido.setText("")
		self.leNombre.setText("")
		self.leDomicilio.setText("")
		self.leLocalidad.setText("")
		self.leCodigoPostal.setText("")
		self.leEMail.setText("")
		self.deFechaIngreso.setDate(QDate.currentDate())
	
	def desactivaPantallaDocente(self):
		self.leDNI.setEnabled(False)
		self.leApellido.setEnabled(False)
		self.leNombre.setEnabled(False)
		self.leDomicilio.setEnabled(False)
		self.leLocalidad.setEnabled(False)
		self.leCodigoPostal.setEnabled(False)
		self.leEMail.setEnabled(False)
		self.deFechaIngreso.setEnabled(False)

	def activaPantallaDocente(self):
		self.leDNI.setEnabled(True)
		self.leApellido.setEnabled(True)
		self.leNombre.setEnabled(True)
		self.leDomicilio.setEnabled(True)
		self.leLocalidad.setEnabled(True)
		self.leCodigoPostal.setEnabled(True)
		self.leEMail.setEnabled(True)
		self.deFechaIngreso.setEnabled(True)

	def desactivaPantallaMateriasTelefonos(self):
		self.leTelefono.setEnabled(False)
		self.leAclaracion.setEnabled(False)
		self.twTelefonos.setRowCount(0)
		self.twMateriasElegidas.setRowCount(0)
		self.twMateriasAElegir.setRowCount(0)
		self.pbAgregarTelefono.setEnabled(False)

	def activaPantallaMateriasTelefonos(self):
		self.leTelefono.setEnabled(True)
		self.leAclaracion.setEnabled(True)
		self.twTelefonos.setRowCount(0)
		self.pbAgregarTelefono.setEnabled(True)
		self.twMateriasElegidas.setRowCount(0)
		self.twMateriasAElegir.setRowCount(0)


	def guardaDocente(self):
		if self.verificaDocente():
			self.limpiarDocente()
		else:
			if self.leDNI.text() == "":
				QMessageBox.warning(self, "Advertencia", "Debe proporcionar un DNI")
				self.leDNI.setFocus(True)
			else:
				self.pbGuardarDocente.setEnabled(False)
				docente = [self.leDNI.text(), self.leApellido.text().upper(), self.leNombre.text().upper(), self.leDomicilio.text().upper(), self.leLocalidad.text().upper(), self.leCodigoPostal.text().upper(), self.fechaAStr(self.deFechaIngreso.date()).upper(), self.leEMail.text().upper(), "0"]
				docente_nuevo = Docente(docente)
				Model().nuevoDocente(docente_nuevo)
				self.desactivaPantallaDocente()
				self.activaPantallaMateriasTelefonos()
				self.cargaMateriasAElegir(self.leDNI.text())


	def nuevoDocente(self):
		self.limpiarDocente()
		self.desactivaPantallaMateriasTelefonos()
		self.activaPantallaDocente()
		self.pbGuardarDocente.setEnabled(True)
		self.pbAgregarMateria.setEnabled(False)
	
	def verificaDocente(self): #verifica si ya existe docente
		resultado = Model().verificaDocente(self.leDNI.text())
		if len(resultado) > 0:
			if resultado[0][8] == 1:
				respuesta = QMessageBox.question(self, "Advertencia", "El docente se encuentra deshabilitado, desea habilitarlo?", QMessageBox.Yes | QMessageBox.No)
				if respuesta == QMessageBox.Yes:
					Model().habilitaDocente(self.leDNI.text())
				self.leDNI.setText("")
				self.leDNI.setFocus(True)

				
			else:
				QMessageBox.warning(self, "Advertencia", "El docente ya existe")
				self.leDNI.setFocus(True)
			return True
		return False


	def agregaTelefono(self):
		dni = self.leDNI.text()
		if self.leTelefono.text() == "":
			QMessageBox.information(self, "Advertencia", "Debe proporcionar un número de telefono")
		else:
			Model().agregaTelefonoDocente(dni, self.leTelefono.text().upper(), self.leAclaracion.text().upper())
			self.leTelefono.setText("")
			self.leAclaracion.setText("")
			self.cargaTelefonos(dni)


	def cargaTelefonos(self, dni):
		datos=Model().selectTelefonoDocente(dni)
		self.twTelefonos.setRowCount(len(datos))
		fila=0
		for dato in datos:
			self.twTelefonos.setItem(fila, 0, QTableWidgetItem(dato[0])) #columna telefono
			self.twTelefonos.setItem(fila, 1, QTableWidgetItem(dato[1])) #columna tipo
			fila += 1

	def seleccionaMateriaElegir(self):
		if self.twMateriasAElegir.rowCount() == 0:
			self.pbAgregarMateria.setEnabled(False)
		else:
			self.pbAgregarMateria.setEnabled(True)
		

	def cargaMateriasAElegir(self, dni):
		self.materiasAElegir=Model().selectMateriaNoDocente(dni)
		#print(self.materiasAElegir)
		self.twMateriasAElegir.setRowCount(len(self.materiasAElegir))
		fila=0
		for dato in self.materiasAElegir:
			self.twMateriasAElegir.setItem(fila, 0, QTableWidgetItem(dato[1])) #columna materia
			self.twMateriasAElegir.setItem(fila, 1, QTableWidgetItem(str(dato[2])))
			fila += 1
		self.pbAgregarMateria.setEnabled(False)
	

	def cargaMateriasElegidas(self, dni):
		self.materiasElegidas=Model().selectMateriaDocente(dni)
		self.twMateriasElegidas.setRowCount(len(self.materiasElegidas))
		fila=0
		for dato in self.materiasElegidas:
			self.twMateriasElegidas.setItem(fila, 0, QTableWidgetItem(dato[1])) #columna materia
			fila += 1
		
	def vinculaMateria(self):
		dni = self.leDNI.text()
		id_materia = self.materiasAElegir[self.twMateriasAElegir.currentRow()][0]
		Model().vinculaDocenteMateria(dni, id_materia)
		self.cargaMateriasElegidas(dni)
		self.cargaMateriasAElegir(dni)

	def strAFecha(self, fechatxt):
		anio = int(int(fechatxt)/10000)
		mes = int((int(fechatxt)-(anio*10000))/100)
		dia = int(fechatxt)-((anio*10000)+(mes*100))
		#print(anio, mes, dia)
		return QDate(anio, mes, dia)

	def fechaAStr(self, fecha):
		#REVISAR
		str(fecha.year())+"0"+str(fecha.month())+"0"+str(fecha.day())
		mes = str(fecha.month())
		dia = str(fecha.day())
		if len(str(fecha.month())) == 1:
			mes = "0" + mes

		if len(str(fecha.day())) == 1:
			dia = "0" + dia
		fechaStr= str(fecha.year()) + mes + dia
		return fechaStr
	
"""
app=QApplication(sys.argv)

# Crear un objeto de la clase
ventana=VentanaAltaDocentes()
# Mostrar ventana
ventana.show()

# Ejecutar la aplicacion
app.exec_()
"""