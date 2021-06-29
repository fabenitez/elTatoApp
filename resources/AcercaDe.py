import sys
import datetime
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QTableWidgetItem
from PyQt5 import uic, QtGui
from PyQt5.QtCore import QDate
import pathlib
from pathlib import Path


class AcercaDe(QDialog):

	
	def __init__(self):
		QDialog.__init__(self)
		pathAbsolute = str(pathlib.Path().absolute()) 
		uic.loadUi(pathAbsolute + "\\interfaces\\frmAcercaDe.ui", self) #uso archivo generado en designer
		self.iconV = QtGui.QIcon()
		self.iconV.addPixmap(QtGui.QPixmap(pathAbsolute + "\\resources\\elTato.ico"),QtGui.QIcon.Normal, QtGui.QIcon.On)
		self.setWindowIcon(self.iconV)
		
		############ funcionalidad BOTONES #########################
		self.pbOk.clicked.connect(self.salida)
		
	def salida(self):
		self.close()
				
	

		#self.cbboxAnio.setEnabled(True)

"""
app=QApplication(sys.argv)

# Crear un objeto de la clase
ventana=AcercaDe()
# Mostrar ventana
ventana.show()

# Ejecutar la aplicacion
app.exec_()
"""