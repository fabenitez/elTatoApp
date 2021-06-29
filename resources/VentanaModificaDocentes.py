import sys
import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QTableWidgetItem
from PyQt5 import uic, QtGui
from PyQt5.QtCore import QDate
from resources.model_sqlite import Model
from resources.docente import Docente
from resources.dlgSeleccionMateria import SeleccionMateria
import pathlib
from pathlib import Path

class VentanaModificaDocentes(QDialog):

	
	def __init__(self):
		QDialog.__init__(self)
		pathAbsolute = str(pathlib.Path().absolute())
		uic.loadUi(pathAbsolute + "\\interfaces\\dlgModificaDocentes.ui", self) #uso archivo generado en designer
		self.iconV = QtGui.QIcon()
		self.iconV.addPixmap(QtGui.QPixmap(pathAbsolute + "\\resources\\elTato.ico"),QtGui.QIcon.Normal, QtGui.QIcon.On)
		self.setWindowIcon(self.iconV)
		
		############ ajuste de objetos en la primer visualizacion
		self.pbBorrarDocente.setEnabled(False)
		self.pbEliminarTelefono.setEnabled(False)
		self.pbAgregarMateria.setEnabled(False)
		self.gbNuevoTelefono.setEnabled(False)
		self.pbGuardarCambios.setEnabled(False)
		self.leDNI.setReadOnly(True)

		self.pbDesvincularMateria.setEnabled(False)
		self.twDocentes.setColumnWidth(0,70) #ancho de DNI
		self.twDocentes.setColumnWidth(1,140) #ancho de apellido
		self.twDocentes.setColumnWidth(2,140) #ancho de nombre
		self.twMateriasAElegir.setColumnWidth(0,180)
		self.twMateriasElegidas.setColumnWidth(0,180)
		self.leBusqueda.setFocus(True)
		self.twTelefonos.setColumnWidth(1,140) #ancho de la columna Aclaracion
		self.deFechaIngreso.setDate(QDate.currentDate())
				
		############ funcionalidad BOTONES #########################
		self.pbAgregarTelefono.clicked.connect(self.agregaTelefono)
		self.pbAgregarMateria.clicked.connect(self.vinculaMateria)
		self.pbEliminarTelefono.clicked.connect(self.eliminaTelefono)
		self.pbDesvincularMateria.clicked.connect(self.desvinculaMateria)
		self.pbGuardarCambios.clicked.connect(self.guardaCambios)
		self.pbBorrarDocente.clicked.connect(self.borraDocente)
		
		############ funcionalidad #########################
		self.leBusqueda.textChanged.connect(self.traeDocentes) #al modificar el LineEdit leBusqueda
		self.twDocentes.itemClicked.connect(self.seleccionaDocente) #al seleccionar item de la tabla twDocentes
		self.twTelefonos.itemClicked.connect(self.seleccionaTelefono)
		self.twMateriasAElegir.itemClicked.connect(self.seleccionaMateriaElegir)
		self.twMateriasElegidas.itemClicked.connect(self.seleccionaMateriaElegida)
	
	def limpiar(self): #limpia todos los line edits
		self.leDNI.setText("")
		self.leApellido.setText("")
		self.leNombre.setText("")
		self.leDomicilio.setText("")
		self.leLocalidad.setText("")
		self.leCodigoPostal.setText("")
		self.leEMail.setText("")
		self.leTelefono.setText("")
		self.leAclaracion.setText("")
		self.deFechaIngreso.setDate(QDate.currentDate())
		self.twTelefonos.setRowCount(0)
		self.twMateriasElegidas.setRowCount(0)
		self.twMateriasAElegir.setRowCount(0)
		self.pbBorrarDocente.setEnabled(False)
		self.pbGuardarCambios.setEnabled(False)
		self.pbEliminarTelefono.setEnabled(False)
		
	
	def traeDocentes(self): #avisa que cambia a estado busqueda
			
		#carga tabla
		self.twDocentes.setRowCount(0)
		if len(self.leBusqueda.text()) > 1:
			datos=Model().selectBusquedaDocente(self.leBusqueda.text())
			self.twDocentes.setRowCount(len(datos))
			self.limpiar()
			fila = 0
			for dato in datos:
				self.twDocentes.setItem(fila, 0, QTableWidgetItem(dato[0])) #columna dni
				self.twDocentes.setItem(fila, 1, QTableWidgetItem(dato[1])) #columna apellido
				self.twDocentes.setItem(fila, 2, QTableWidgetItem(dato[2])) #columna nombre
				fila += 1
		
	def seleccionaDocente(self):
		
		self.twDocentes.setCurrentCell(self.twDocentes.currentRow(), 0) #fuerzo la eleccion de la primera columna
		dni = self.twDocentes.selectedItems() #traigo el item seleccionado
		self.docente_select = Model().selectDocenteExacto(dni[0].text())
		self.leBusqueda.setText("")
				
		############ cargo Edits #######################
		self.leDNI.setText(self.docente_select.getDNI())
		self.leApellido.setText(self.docente_select.getApellido())
		self.leNombre.setText(self.docente_select.getNombre())
		self.leDomicilio.setText(self.docente_select.getDomicilio())
		self.leLocalidad.setText(self.docente_select.getLocalidad())
		self.leCodigoPostal.setText(self.docente_select.getCodigoPostal())
		self.leEMail.setText(self.docente_select.getEMail())
		self.deFechaIngreso.setDate(self.strAFecha(self.docente_select.getFechaIngreso()))
		self.cargaTelefonos(self.docente_select.getDNI())
		self.cargaMateriasAElegir(self.docente_select.getDNI())
		self.cargaMateriasElegidas(self.docente_select.getDNI())
		self.pbGuardarCambios.setEnabled(True)
		self.pbBorrarDocente.setEnabled(True)

	def seleccionaMateria(self):
		self.pbDesvincularMateria.setEnabled(True)

	def seleccionaTelefono(self):
		self.pbEliminarTelefono.setEnabled(True)	

	def eliminaTelefono(self):
		try:
			if self.twTelefonos.currentRow() > -1:
				telefono = self.twTelefonos.item(self.twTelefonos.currentRow(),0).text() #devuelve el telefono seleccionado en tabla
				dni = self.docente_select.getDNI()
				respuesta = QMessageBox.question(self, "Eliminacion de Telefono", "El telefono: " +
						telefono + " será eliminado, OK?? ", QMessageBox.Yes | QMessageBox.No)

				if  respuesta==QMessageBox.Yes:
					Model().eliminaTelefono(dni, telefono)
					self.cargaTelefonos(dni)
		
		except AttributeError:
			QMessageBox.information(self, "Eliminacion de Telefono", "Sin elemento a eliminar")
			self.twTelefonos.removeRow(self.twTelefonos.currentRow())

	def agregaTelefono(self):
		dni = self.docente_select.getDNI()
		if self.leTelefono.text() == "":
			QMessageBox.information(self, "Advertencia", "Debe proporcionar un número de telefono")
			self.leTelefono.setFocus(True)
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
		self.gbNuevoTelefono.setEnabled(True)

	def seleccionaMateriaElegir(self):
		if self.twMateriasAElegir.rowCount() == 0:
			self.pbAgregarMateria.setEnabled(False)
		else:
			self.pbAgregarMateria.setEnabled(True)
		self.pbDesvincularMateria.setEnabled(False)
		

	def seleccionaMateriaElegida(self):
		if self.twMateriasElegidas.rowCount() == 0:
			self.pbDesvincularMateria.setEnabled(False)
		else:
			self.pbDesvincularMateria.setEnabled(True)
		self.pbAgregarMateria.setEnabled(False)

	def cargaMateriasAElegir(self, dni):
		self.materiasAElegir=Model().selectMateriaNoDocente(dni)
		self.twMateriasAElegir.setRowCount(len(self.materiasAElegir))
		fila=0
		for dato in self.materiasAElegir:
			self.twMateriasAElegir.setItem(fila, 0, QTableWidgetItem(dato[1])) #columna materia
			fila += 1
		self.pbAgregarMateria.setEnabled(False)
	

	def cargaMateriasElegidas(self, dni):
		self.materiasElegidas=Model().selectMateriaDocente(dni)
		self.twMateriasElegidas.setRowCount(len(self.materiasElegidas))
		fila=0
		for dato in self.materiasElegidas:
			self.twMateriasElegidas.setItem(fila, 0, QTableWidgetItem(dato[1])) #columna materia
			fila += 1
		self.pbDesvincularMateria.setEnabled(False)

	def vinculaMateria(self):
		dni = self.docente_select.getDNI()
		id_materia = self.materiasAElegir[self.twMateriasAElegir.currentRow()][0]
		Model().vinculaDocenteMateria(dni, id_materia)
		self.cargaMateriasElegidas(dni)
		self.cargaMateriasAElegir(dni)
		self.pbAgregarMateria.setEnabled(False)

	def desvinculaMateria(self):
		id_materia = self.materiasElegidas[self.twMateriasElegidas.currentRow()][0] #devuelve el id de la materia desde la lista
		dni = self.docente_select.getDNI()
		Model().desvinculaDocenteMateria(dni, id_materia)
		self.cargaMateriasElegidas(dni)
		self.cargaMateriasAElegir(dni)
		self.pbDesvincularMateria.setEnabled(False)

	def guardaCambios(self):
		
		claveActualizacion = self.docente_select.getDNI() #dato que va en el WHERE del UPDATE

		#preparo campos a actualizar dentro del objeto docente
		self.docente_select.setFechaIngreso(self.fechaAStr(self.deFechaIngreso.date()))
		self.docente_select.setApellido(self.leApellido.text().upper())
		self.docente_select.setNombre(self.leNombre.text().upper())
		self.docente_select.setDomicilio(self.leDomicilio.text().upper())
		self.docente_select.setLocalidad(self.leLocalidad.text().upper())
		self.docente_select.setCodigoPostal(self.leCodigoPostal.text().upper())
		self.docente_select.setEMail(self.leEMail.text().upper())

		if self.leDNI.text() != self.docente_select.getDNI():
			respuesta = QMessageBox.question(self, "Advertencia", "Ha modificado el DNI " +
						self.docente_select.getDNI() + " Es correcto?? ", QMessageBox.Yes | QMessageBox.No)

			if  respuesta==QMessageBox.Yes:					
				self.docente_select.setDNI(self.leDNI.text())
	
		self.docente_select.setClaveActualizacion(claveActualizacion)
		
		Model().actualizaDocente(self.docente_select)
		self.limpiar()
		self.gbNuevoTelefono.setEnabled(False)

	def borraDocente(self):
		Model().deshabilitaDocente(self.docente_select.getDNI())
		self.limpiar()
		self.gbNuevoTelefono.setEnabled(False)

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
ventana=VentanaModificaDocentes()
# Mostrar ventana
ventana.show()

# Ejecutar la aplicacion
app.exec_()
"""