import sys
import datetime
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QTableWidgetItem
from PyQt5 import uic, QtCore
from PyQt5.QtCore import QDate, QDateTime
from resources.model_sqlite import Model
from resources.docenteMaterias import DocenteMaterias
from PyQt5 import uic, QtWidgets, QtGui, QtCore
import pathlib
from pathlib import Path
import os


class VentanaMuestraGrilla(QDialog):
	

	dicDias = {"lunes":0, "martes":1, "miercoles":2, "jueves":3, "viernes":4}
	deshacerList = []
	pathFile = "\\impresiones\\"
	CSVsep = ";"


	def __init__(self):
		QDialog.__init__(self)
		pathAbsolute = str(pathlib.Path().absolute())
		uic.loadUi(pathAbsolute + "\\interfaces\\dlgMuestraGrilla.ui", self) #uso archivo generado en designer
		self.iconV = QtGui.QIcon()
		self.iconV.addPixmap(QtGui.QPixmap(pathAbsolute + "\\resources\\elTato.ico"),QtGui.QIcon.Normal, QtGui.QIcon.On)
		self.setWindowIcon(self.iconV)

		self.listLblMate = [[self.lblMateriaL1, self.lblMateriaM1, self.lblMateriaX1, self.lblMateriaJ1, self.lblMateriaV1],
		[self.lblMateriaL2, self.lblMateriaM2, self.lblMateriaX2, self.lblMateriaJ2, self.lblMateriaV2],
		[self.lblMateriaL3, self.lblMateriaM3, self.lblMateriaX3, self.lblMateriaJ3, self.lblMateriaV3],
		[self.lblMateriaL4, self.lblMateriaM4, self.lblMateriaX4, self.lblMateriaJ4, self.lblMateriaV4]]

		self.listLblProf = [[self.lblProfesorL1, self.lblProfesorM1, self.lblProfesorX1, self.lblProfesorJ1, self.lblProfesorV1],
		[self.lblProfesorL2, self.lblProfesorM2, self.lblProfesorX2, self.lblProfesorJ2, self.lblProfesorV2],
		[self.lblProfesorL3, self.lblProfesorM3, self.lblProfesorX3, self.lblProfesorJ3, self.lblProfesorV3],
		[self.lblProfesorL4, self.lblProfesorM4, self.lblProfesorX4, self.lblProfesorJ4, self.lblProfesorV4]]

		self.cboxAnio.currentIndexChanged.connect(self.cargaTurnos)
		self.cboxTurno.currentIndexChanged.connect(self.cargaNiveles)
		self.cboxNivel.currentIndexChanged.connect(self.cargaCursos)
		self.cboxCurso.currentIndexChanged.connect(self.limpiarGrilla)
		
		############ ajuste de objetos en la primer visualizacion
		self.pbMuestraGrilla.setEnabled(False)
		self.pbImprimirGrilla.setEnabled(False)
				
		anios = Model().traeAniosGrilla()
		aniosList = []
		for anio in anios:
			aniosList.append(anio[0])
		self.cboxAnio.addItems(aniosList)

		

		self.limpiarGrilla()
				
								
		############ funcionalidad BOTONES #########################
		self.pbMuestraGrilla.clicked.connect(self.muestraGrilla)
		self.pbAbandonar.clicked.connect(self.abandona)
		self.pbImprimirGrilla.clicked.connect(self.imprimeGrilla)
		
	def cargaTurnos(self):
		turnos = Model().traeTurnosGrilla(self.cboxAnio.currentText())
		turnosList = []
		for turno in turnos:
			turnosList.append(turno[0])
		self.cboxTurno.addItems(turnosList)
		self.limpiarGrilla()

	def cargaNiveles(self):
		niveles = Model().traeNivelesGrilla(self.cboxAnio.currentText(), self.cboxTurno.currentText())
		nivelesList = []
		for nivel in niveles:
			nivelesList.append(str(nivel[0]))
		self.cboxNivel.addItems(nivelesList)
		self.limpiarGrilla()

	def cargaCursos(self):
		cursos = Model().traeCursosGrilla(self.cboxAnio.currentText(), self.cboxTurno.currentText(), self.cboxNivel.currentText())
		cursosList = []
		for curso in cursos:
			cursosList.append(curso[0])
		self.cboxCurso.addItems(cursosList)
		if self.cboxCurso.count() > 0:
			self.pbMuestraGrilla.setEnabled(True)
		else:
			self.pbMuestraGrilla.setEnabled(False)
		self.limpiarGrilla()
	
	def abandona(self, evnt):
		self.close()
		
	def limpiarGrilla(self):

		for x in range(0,4):
			for y in range(0,5):
				self.listLblProf[x][y].setText("")
				self.listLblMate[x][y].setText("")

		self.pbImprimirGrilla.setEnabled(False)
	
	def muestraGrilla(self):

		self.anio = self.cboxAnio.currentText()
		self.turno = self.cboxTurno.currentText()
		self.nivel = self.cboxNivel.currentText()
		self.curso = self.cboxCurso.currentText()

		grilla = Model().traeGrillaCreada(self.anio, self.turno, self.nivel, self.curso)
		self.grillaProf = [["","","","",""],
			["","","","",""],["","","","",""],["","","","",""]]
		self.grillaProfN = [["","","","",""],
			["","","","",""],["","","","",""],["","","","",""]]
		self.grillaMate = [["","","","",""],
			["","","","",""],["","","","",""],["","","","",""]]

		for record in grilla:
			
			nombreCompleto = Model().traeProfesor(record[0]) # prof.apellido, prof.nombre
			apellido = nombreCompleto[0][0]
			nombre = nombreCompleto[0][1]

			mateResult = Model().traeMateria(record[1])
			materia = mateResult[0][0]

			dia = record[5]	
			hora = int(record[6])
			
			self.grillaProf[hora-1][self.dicDias[dia]] = apellido + " " + nombre
			self.grillaMate[hora-1][self.dicDias[dia]] = materia
			
			self.listLblProf[hora-1][self.dicDias[dia]].setText(apellido + "\n" + nombre[0:25])
			self.listLblMate[hora-1][self.dicDias[dia]].setText(materia[0:25]+"\n"+materia[25:len(materia)])
		
		self.pbImprimirGrilla.setEnabled(True)
	
	def centraString(self, texto, tamanio):
		espacioIn = int((tamanio - len(texto)) / 2)
		espacioFi = tamanio - espacioIn - len(texto)

		result = ""

		for espIn in range(0,espacioIn):
			result = result +" "

		result = result + texto

		for espIn in range(0,espacioFi):
			result = result +" "
	
		return result

	def replica(self, texto, veces):
		result = ""
		for x in range(0, veces):
			result = result + texto
		return result

	def imprimeGrilla(self):

		td = 25

		lensList = [7,td,td,td,td,td]
		diasList = ["HORAS", "LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES"]
		
		inicioT = "<table border=""2"" cellspacing=0 style=""width:50%"" rules=all>"

		header = "<tr border=1>" 
	
		hora11 = "<tr>"
		hora12 = "<tr>"
		hora13 = "<tr>"
		hora14 = "<tr>"

		hora21 = "<tr>"
		hora22 = "<tr>"
		hora23 = "<tr>"
		hora24 = "<tr>"

		hora31 = "<tr>"
		hora32 = "<tr>"
		hora33 = "<tr>"
		hora34 = "<tr>"

		hora41 = "<tr>"
		hora42 = "<tr>"
		hora43 = "<tr>"
		hora44 = "<tr>"


		for pr in range(0,6):
			header = header + "<th style=""font-size:120%;"">" + diasList[pr] + "</th>"
		
		header = header + "</tr>"
				
			  
		for pr in range(0,6):

			if pr == 0:
				hora11 = hora11 + "<th rowspan=2 valign=""middle"">" + "PRIMERA HORA" + "</th>"
				hora21 = hora21 + "<th rowspan=2 valign=""middle"">" + "SEGUNDA HORA" + "</th>"
				hora31 = hora31 + "<th rowspan=2 valign=""middle"">" + "TERCERA HORA" + "</th>"
				hora41 = hora41 + "<th rowspan=2 valign=""middle"">" + "CUARTA HORA" + "</th>"
	
				

			else:
				hora11 = hora11 + "<td align=""center"">" + self.grillaMate[0][pr-1] + "</td>"
				hora12 = hora12 + "<td align=""center"">" + self.grillaProf[0][pr-1] + "</td>"
				
				hora21 = hora21 + "<td align=""center"">" + self.grillaMate[1][pr-1] + "</td>"
				hora22 = hora22 + "<td align=""center"">" + self.grillaProf[1][pr-1] + "</td>"
				
				hora31 = hora31 + "<td align=""center"">" + self.grillaMate[2][pr-1] + "</td>"
				hora32 = hora32 + "<td align=""center"">" + self.grillaProf[2][pr-1] + "</td>"
				
				hora41 = hora41 + "<td align=""center"">" + self.grillaMate[3][pr-1] + "</td>"
				hora42 = hora42 + "<td align=""center"">" + self.grillaProf[3][pr-1] + "</td>"
				
		grupoA = "<tbody align=""center"" valign=""top"" bgcolor = ""#dce0e0"">"
		grupoAfin = "</tbody>"

		grupoB = "<tbody align=""center"" valign=""top"" >"
		grupoBfin = "</tbody>"

		hora11 = hora11 + "</tr>"
		hora12 = hora12 + "</tr>"
		
		hora21 = hora21 + "</tr>"
		hora22 = hora22 + "</tr>"
		
		hora31 = hora31 + "</tr>"
		hora32 = hora32 + "</tr>"
		
		hora41 = hora41 + "</tr>"
		hora42 = hora42 + "</tr> </table>"

		
		titulo = ("<caption style=""font-size:150%;"">HORARIOS DEL TURNO " + self.cboxTurno.currentText() + " - AÑO: " + self.cboxAnio.currentText() + 
			" - NIVEL: " + self.cboxNivel.currentText() + " - CURSO: " + self.cboxCurso.currentText() +
			"</caption>")

		colgroup = "<colgroup> <col span=""1"" style=""width: 15%;""> <col span=""1"" style=""width: 70%;""> <col span=""1"" style=""width: 15%;""> </colgroup>"
		
		archivo = self.nombreArchivo()
		print(pathlib.Path().absolute())

		pathAbsolute = str(pathlib.Path().absolute()) 
		
		try:
			archivoObj = open(pathAbsolute + self.pathFile + archivo[0],"w")
			archivoXLS = open(pathAbsolute + self.pathFile + archivo[2],"w")
			
			archivoObj.write(inicioT + "\n")
			archivoObj.write(colgroup + "\n")
			archivoObj.write(titulo + "\n")
			archivoObj.write(header + "\n")

			archivoObj.write(grupoA + "\n")

			archivoObj.write(hora11 + "\n")
			archivoObj.write(hora12 + "\n")
			
			archivoObj.write(grupoAfin + "\n")
			archivoObj.write(grupoB + "\n")

			archivoObj.write(hora21 + "\n")
			archivoObj.write(hora22 + "\n")
			
			archivoObj.write(grupoBfin + "\n")
			archivoObj.write(grupoA + "\n")

			archivoObj.write(hora31 + "\n")
			archivoObj.write(hora32 + "\n")
			
			archivoObj.write(grupoAfin + "\n")
			archivoObj.write(grupoB + "\n")

			archivoObj.write(hora41 + "\n")
			archivoObj.write(hora42 + "\n")
			archivoObj.write(archivo[1])

			archivoObj.write(grupoBfin + "\n")

			archivoXLS.write(inicioT + "\n")
			archivoXLS.write(colgroup + "\n")
			archivoXLS.write(titulo + "\n")
			archivoXLS.write(header + "\n")

			archivoXLS.write(grupoA + "\n")

			archivoXLS.write(hora11 + "\n")
			archivoXLS.write(hora12 + "\n")
			
			archivoXLS.write(grupoAfin + "\n")
			archivoXLS.write(grupoB + "\n")

			archivoXLS.write(hora21 + "\n")
			archivoXLS.write(hora22 + "\n")
			
			archivoXLS.write(grupoBfin + "\n")
			archivoXLS.write(grupoA + "\n")

			archivoXLS.write(hora31 + "\n")
			archivoXLS.write(hora32 + "\n")
			
			archivoXLS.write(grupoAfin + "\n")
			archivoXLS.write(grupoB + "\n")

			archivoXLS.write(hora41 + "\n")
			archivoXLS.write(hora42 + "\n")
			archivoXLS.write(archivo[1])

			archivoXLS.write(grupoBfin + "\n")

			archivoXLS.close()
			archivoObj.close()
			try:
				os.startfile(pathAbsolute + self.pathFile + archivo[0]) #, "print")
			except:
				QMessageBox.information(self, "ADVERTENCIA", "No posee aplicacion asociada al tipo de archivo HTML" +
					"\nNo se puede visualizar" +
					"\nSe abrirá carpeta contenedora")
				os.startfile(pathAbsolute + self.pathFile)

		except FileNotFoundError:
			respuesta = QMessageBox.critical(self, "ERROR", "No se encuentra la carpeta " + self.pathFile + "\ndonde dejar el archivo de impresion" +
				"\nDesea crearla?", QMessageBox.Yes | QMessageBox.No)

			if respuesta == QMessageBox.Yes:
				path = Path(pathAbsolute + self.pathFile)
				path.mkdir(parents=True)
		

		#self.imprimeArchivo(archivo)
		

	def nombreArchivo(self):
		
		date = QDateTime.currentDateTime().date()
		time = QDateTime.currentDateTime().time()
		
		anio = str(date.year())
		mes = ("0" + str(date.month()))[-2:] #de -2 al final
		dia = ("0" + str(date.day()))[-2:]

		hora = ("0" + str(time.hour()))[-2:]
		minu = ("0" + str(time.minute()))[-2:]

		diaHora = (anio + mes + dia + "-" + 
			self.cboxAnio.currentText() + 
			self.cboxTurno.currentText()[0:2] + 
			self.cboxNivel.currentText() +
			self.cboxCurso.currentText())
		archivo = "PRT" + diaHora + ".html"
		archivoXLS =  "PRT" + diaHora + ".xls"
		fechaCompleta = "Fecha: " + dia + "/" + mes + "/" + anio + "-" + hora + ":" + minu
			
		return archivo, fechaCompleta, archivoXLS

"""		
app=QApplication(sys.argv)

# Crear un objeto de la clase
ventana=VentanaMuestraGrilla()
# Mostrar ventana
ventana.show()

# Ejecutar la aplicacion
app.exec_()
"""