import sys
import datetime
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QTableWidgetItem
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtCore import QDate
from resources.model_sqlite import Model
from resources.docenteMaterias import DocenteMaterias
import pathlib
from pathlib import Path



class VentanaCreaGrilla(QDialog):
	

	dicDias = {"lunes":0, "martes":1, "miercoles":2, "jueves":3, "viernes":4}

	def __init__(self):
		QDialog.__init__(self)
		pathAbsolute = str(pathlib.Path().absolute()) 
		uic.loadUi(pathAbsolute + "\\interfaces\\dlgCreaGrilla.ui", self) #uso archivo generado en designer
		self.iconV = QtGui.QIcon()
		self.iconV.addPixmap(QtGui.QPixmap(pathAbsolute + "\\resources\\elTato.ico"),QtGui.QIcon.Normal, QtGui.QIcon.On)
		self.setWindowIcon(self.iconV)
		
		############ ajuste de objetos en la primer visualizacion
		self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
		anio_inicio = QDate.currentDate().year() - 1
		aniosList = [str(anio_inicio), str(anio_inicio + 1), str(anio_inicio + 2)]
		self.cboxAnio.addItems(aniosList)
		turnosList = ["MAÑANA","TARDE"]
		self.cboxTurno.addItems(turnosList)
		nivelesList = ["1","2","3"]
		self.cboxNivel.addItems(nivelesList)
		self.cargaCursos()
		self.pbGuardaGrilla.setEnabled(False)

		self.listLblMate = [[self.lblMateriaL1, self.lblMateriaM1, self.lblMateriaX1, self.lblMateriaJ1, self.lblMateriaV1],
		[self.lblMateriaL2, self.lblMateriaM2, self.lblMateriaX2, self.lblMateriaJ2, self.lblMateriaV2],
		[self.lblMateriaL3, self.lblMateriaM3, self.lblMateriaX3, self.lblMateriaJ3, self.lblMateriaV3],
		[self.lblMateriaL4, self.lblMateriaM4, self.lblMateriaX4, self.lblMateriaJ4, self.lblMateriaV4]]

		self.listLblProf = [[self.lblProfesorL1, self.lblProfesorM1, self.lblProfesorX1, self.lblProfesorJ1, self.lblProfesorV1],
		[self.lblProfesorL2, self.lblProfesorM2, self.lblProfesorX2, self.lblProfesorJ2, self.lblProfesorV2],
		[self.lblProfesorL3, self.lblProfesorM3, self.lblProfesorX3, self.lblProfesorJ3, self.lblProfesorV3],
		[self.lblProfesorL4, self.lblProfesorM4, self.lblProfesorX4, self.lblProfesorJ4, self.lblProfesorV4]]

		self.grillaProf = [["","","","",""],["","","","",""],["","","","",""],["","","","",""]]
		self.grillaMate = [["","","","",""],["","","","",""],["","","","",""],["","","","",""]]
		self.limpiarGrilla()
				
								
		############ funcionalidad BOTONES #########################
		self.pbGeneraGrilla.clicked.connect(self.generaGrilla)
		self.pbGuardaGrilla.clicked.connect(self.guardaGrilla)
		self.pbAbandonar.clicked.connect(self.abandona)
		self.cboxAnio.currentIndexChanged.connect(self.cargaCursos)
		self.cboxTurno.currentIndexChanged.connect(self.cargaCursos)
		self.cboxNivel.currentIndexChanged.connect(self.cargaCursos)
		
	
	def abandona(self, evnt):

		if len(Model().selectPreGrilla()) > 0:
			respuesta = QMessageBox.question(self, "Advertencia", "Si abandona perderá los cambios\nDesea Salir?? ", QMessageBox.Yes | QMessageBox.No)
			if  respuesta==QMessageBox.Yes:
				Model().limpiaPreGrilla()
				Model().liberaTodasDispos([self.anio, self.turno, self.nivel, self.curso])
				self.close()
			else:
				evnt.ignore()
		else:	
			self.close()
		
	def limpiarGrilla(self):

		for x in range(0,4):
			for y in range(0,5):
				self.listLblProf[x][y].setText("")
				self.listLblMate[x][y].setText("")
		self.cboxAnio.setEnabled(True)
		self.cboxTurno.setEnabled(True)
		self.cboxNivel.setEnabled(True)
		self.cboxCurso.setEnabled(True)
		self.pbGeneraGrilla.setEnabled(True)
		self.pbGuardaGrilla.setEnabled(False)

	def cargaCursos(self):

		self.cboxCurso.clear()
		self.turno = self.cboxTurno.currentText()
		self.nivel = self.cboxNivel.currentText()
		self.anio = self.cboxAnio.currentText()
		cursos = Model().traeCursos(self.anio, self.turno, self.nivel)

		cursoPos = 0
		cursosList = []
		for fila in cursos:
			for columna in fila:
				for dato in columna:
					if dato == "1" and cursoPos == 0:
						cursosList = ["A"]
					elif dato == "1" and cursoPos == 1:
						cursosList.append("B")
					elif dato == "1" and cursoPos == 2:		
						cursosList.append("C")
					cursoPos += 1

		self.cboxCurso.addItems(cursosList)
		if self.cboxCurso.count() == 0:
			self.pbGeneraGrilla.setEnabled(False)
		else:
			self.pbGeneraGrilla.setEnabled(True)


	def generaGrilla(self):

		self.anio = self.cboxAnio.currentText()
		self.turno = self.cboxTurno.currentText()
		self.nivel = self.cboxNivel.currentText()
		self.curso = self.cboxCurso.currentText()

		if len(Model().grillaCreada(self.anio, self.turno, self.nivel, self.curso)) > 0:
			QMessageBox.information(self, "Advertencia", "Ya existe grilla para " + 
				"\nAÑO   : " + self.anio + 
				"\nTURNO : " + self.turno +
				"\nNIVEL : " + self.nivel +
				"\nCURSO : " + self.curso)

		else:
			self.algoritmoGrilla()
		

	def algoritmoGrilla(self):

		cantMateriasNivel = Model().cantMateriasNivel(self.nivel)
		cantProfesores = Model().cantMateriasConProfesores(self.nivel)

		if cantProfesores != cantMateriasNivel:
			QMessageBox.information(self, "Advertencia", "Faltan Docentes para cubrir las materias del nivel " + self.nivel)		

		"""
		traigo listado de cantidad de materias que puedo dictar x dia, ordenando las cantidades de menor a mayor,
		se entiende que tengo menos posibilidades de repartir materias a profesores y debo aprovecharlas.
		dia, hora, cantidad_de_materias  
		"""

		dispoDia = Model().disponibilidadDia([self.anio, self.turno, self.nivel]) #de menor a mayor cantidad de materias de ese nivel por dia
		print("dispoDia :", dispoDia)
		#dp.dia, dp.hora, count(m.id_materia)
		

		if len(dispoDia) < 1:
			QMessageBox.information(self, "Advertencia", "No hay docentes disponibles para ninguna materia en las opciones elegidas " + self.nivel)
		else:
			for cantMaterias in dispoDia:
				print(" cantMaterias:........ ",cantMaterias)
				dia = cantMaterias[0]
				hora = cantMaterias[1]
				if len(Model().disponiblidadUtilizada([self.anio, self.turno, dia, hora, self.curso])) == 0: 
					materias = Model().materiasProfesoresAlgoritmo(self.anio, self.turno, dia, hora, self.nivel, self.curso) #materias del dia desde mayor a menor carga horaria
					print("materias************",materias)
					if len(materias) > 0:
						#print(materias) # m.id_materia, m.materia, m.hscatedra, pm.dni, nombre
						dispTomadas = []
						id_materia = materias[0][0]
						materiadesc = materias[0][1]
						hscatedra = materias[0][2]
						matdni = materias[0][3]
						apellido = materias[0][4]
						nombre = materias[0][5]

						self.tomarMateria([matdni, self.anio, self.turno, self.nivel, dia, hora, str(id_materia), self.curso, apellido, nombre, materiadesc])
						dispTomadas.append([matdni, self.anio, self.turno, dia, hora, id_materia])
												
						if hscatedra >= 2:
							horaMat = int(hora)
							hsItera = hscatedra - 1
					
							while hsItera > 0:
								hantes = horaMat - 1
								hdespues = horaMat + 1

								tot_hs = 0
								for hsxdia in dispTomadas: #cuento las hs tomadas ese dia
									if hsxdia[3] == dia:
										tot_hs += 1


								if (tot_hs < 2) and len(Model().profesorDiaExacto([matdni, self.anio, self.turno, dia, str(hantes)])) > 0 and Model().dispoLibre([self.anio, self.turno, dia, str(hantes),self.curso]):
								
									horaMat = hantes
									dispTomadas.append([matdni, self.anio, self.turno, dia, str(horaMat), id_materia])
									self.tomarMateria([matdni, self.anio, self.turno, self.nivel, dia, str(horaMat), str(id_materia), self.curso, apellido, nombre, materiadesc])
									hsItera -= 1
							 
								elif (tot_hs < 2) and len(Model().profesorDiaExacto([matdni, self.anio, self.turno, dia, str(hdespues)])) > 0 and Model().dispoLibre([self.anio, self.turno, dia, str(hdespues),self.curso]):
								
									horaMat = hdespues 
									dispTomadas.append([matdni, self.anio, self.turno, dia, str(horaMat), id_materia])
									self.tomarMateria([matdni, self.anio, self.turno, self.nivel, dia, str(horaMat), str(id_materia), self.curso, apellido, nombre, materiadesc])
									hsItera -= 1
							
								else:
									print("Busca otro dia ******************")
									otroDia = Model().dispoProfesorNoDia([matdni, self.anio, self.turno, dia, self.nivel, self.curso])
									totdias = len(otroDia)
									if totdias > 0:
										limite = totdias
										for oDia in otroDia:
											print(oDia)
											dia_o = oDia[3]
											horaMat = int(oDia[4])
											diaTomado = Model().diaTomado(self.anio, self.turno, dia_o, str(horaMat), self.curso) #trae datos si el dia esta tomado

											if len(diaTomado) == 0 and hsItera > 0 and Model().dispoLibre([self.anio, self.turno, dia_o, str(horaMat),self.curso]):
												#cargo grilla para ser impresa mas tarde
												dispTomadas.append([matdni, self.anio, self.turno, dia_o, str(horaMat), id_materia])
												self.tomarMateria([matdni, self.anio, self.turno, self.nivel, dia_o, str(horaMat), str(id_materia), self.curso, apellido, nombre, materiadesc])
												hsItera -= 1

											elif len(diaTomado) > 0 and limite == 1: #si el dia esta tomado y es la ultima posibilidad
												print(diaTomado)
												otrodni = diaTomado[0][0] #quien lo tiene tomado
												print("tomado por : ", diaTomado)
												dispoOtro = Model().dispoProfesorAnioTurno(otrodni, self.anio, self.turno, self.curso) #paso dni del otro profesor que tiene tomado el dia
												if len(dispoOtro) > 0: #si el otro profesor tiene otro dia hago enroque
													print("otro profesor tiene dispo: ", dispoOtro)
													for dispoOtroRow in dispoOtro:
														count = len(dispoOtro)
														dia_Otro = dispoOtroRow[3]
														hora_Otro = dispoOtroRow[4]
														
														if Model().dispoLibre([self.anio, self.turno, dia_Otro, str(hora_Otro),self.curso]):
															Model().vuelveAtrasModificaciones([otrodni, self.anio, self.turno, dia_o, str(horaMat)]) #devuelvo disponibilidad al otro profe sobre ese dia
															Model().eliminarPreGrilla([otrodni, self.anio, self.turno, dia_o, str(horaMat)])

															nombreCompleto = Model().traeProfesor(otrodni) # prof.apellido, prof.nombre
															apellidoO = nombreCompleto[0][0]
															nombreO = nombreCompleto[0][1]
															mateResult = Model().traeMateria(str(diaTomado[0][6])) 
															materiaO = mateResult[0][0]
													
															self.tomarMateria([otrodni, self.anio, self.turno, self.nivel, dia_Otro, str(hora_Otro), str(diaTomado[0][6]), self.curso, apellidoO, nombreO, materiaO])
													
															nombreCompleto = Model().traeProfesor(matdni) # prof.apellido, prof.nombre
															apellidoO = nombreCompleto[0][0]
															nombreO = nombreCompleto[0][1]
															mateResult = Model().traeMateria(str(id_materia)) 
															materiaO = mateResult[0][0]
													
															self.tomarMateria([matdni, self.anio, self.turno, self.nivel, dia_o, str(horaMat), str(id_materia), self.curso, apellidoO, nombreO, materiaO])
														else:
															if count == 0:
																print("el otro profesor no tiene disponibilidad en este curso")

														count -=1
												
											limite -=1
									hsItera -= 1
													

								
			if len(Model().selectPreGrilla()) == 0:
				QMessageBox.information(self, "Advertencia", "Se generó grilla vacia " + 
				"\nAÑO   : " + self.anio + 
				"\nTURNO : " + self.turno +
				"\nNIVEL : " + self.nivel +
				"\nCURSO : " + self.curso)
			else:
				self.imprimirGrilla()
				self.cboxAnio.setEnabled(False)
				self.cboxTurno.setEnabled(False)
				self.cboxNivel.setEnabled(False)
				self.cboxCurso.setEnabled(False)
				self.pbGeneraGrilla.setEnabled(False)
				self.pbGuardaGrilla.setEnabled(True)


	def tomarMateria(self, datos):

		dni = datos[0]
		anio = datos[1]
		turno = datos[2]
		nivel = datos[3]
		dia = datos[4]
		hora = datos[5]
		id_materia = datos[6]
		curso = datos[7]
		apellido = datos[8]
		nombre = datos[9]
		materiadesc = datos[10]

		Model().guardaPreGrilla([dni, anio, turno, nivel, dia, hora, id_materia, curso])
		Model().quitarDisponibilidad([dni, anio, turno, dia, hora, id_materia, curso])
		self.cargaGrilla(dia, hora, apellido, nombre, materiadesc)						


	def cargaGrilla(self, dia, hora, apellido, nombre, materia):
		print(dia, hora, apellido, nombre, materia)

		self.grillaProf[int(hora)-1][self.dicDias[dia]] = apellido + "\n" + nombre[0:25]
		self.grillaMate[int(hora)-1][self.dicDias[dia]] = materia[0:25]+"\n"+materia[25:len(materia)]


	def imprimirGrilla(self):
		for x in range(0,4):
			for y in range(0,5):
				self.listLblProf[x][y].setText(self.grillaProf[x][y])
				self.listLblMate[x][y].setText(self.grillaMate[x][y])
						
	def guardaGrilla(self):
		
		Model().guardaGrilla()
		Model().limpiaPreGrilla()
		self.limpiarGrilla()

"""			
app=QApplication(sys.argv)

# Crear un objeto de la clase
ventana=VentanaCreaGrilla()
# Mostrar ventana
ventana.show()

# Ejecutar la aplicacion
app.exec_()
"""