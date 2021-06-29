# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dlgSeleccionMateria.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QMessageBox
from resources.model_sqlite import Model




class SeleccionMateria(QDialog):

    dni = ""
    

    def __init__(self, *args):
        QDialog.__init__(self)
        self.setupUi(self)
        self.dni = args[0][0]
        
    def setupUi(self, SeleccionMateria):
        SeleccionMateria.setObjectName("dlgSeleccionMateria")
        SeleccionMateria.resize(297, 241)
        SeleccionMateria.setMinimumSize(QtCore.QSize(297, 241))
        SeleccionMateria.setMaximumSize(QtCore.QSize(297, 241))

        self.twMateriasSelecc = QtWidgets.QTableWidget(SeleccionMateria)
        self.twMateriasSelecc.setGeometry(QtCore.QRect(20, 20, 256, 201))
        self.twMateriasSelecc.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.twMateriasSelecc.setColumnCount(1)
        self.twMateriasSelecc.setObjectName("twMateriasSelecc")
        self.twMateriasSelecc.setRowCount(0)

        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)

        self.twMateriasSelecc.setHorizontalHeaderItem(0, item)

        self.retranslateUi(SeleccionMateria)
        QtCore.QMetaObject.connectSlotsByName(SeleccionMateria)

        ####################### SETEO Y FUNCIONALIDADES AGREGADAS
        self.twMateriasSelecc.setColumnWidth(0,255) #ancho de la columna de la tabla
        self.twMateriasSelecc.itemClicked.connect(self.agregaMateria)
        self.cargaMaterias()

    def retranslateUi(self, dlgSeleccionMateria):
        _translate = QtCore.QCoreApplication.translate
        dlgSeleccionMateria.setWindowTitle(_translate("dlgSeleccionMateria", "Seleccione Materia"))
        item = self.twMateriasSelecc.horizontalHeaderItem(0)
        item.setText(_translate("dlgSeleccionMateria", "Materias Disponibles"))

    ################ FUNCIONALIDAD AGREGADA

    def cargaMaterias(self):
        self.materias=Model().selectMaterias()
        self.twMateriasSelecc.setRowCount(len(self.materias))
        fila = 0
        for dato in self.materias:
            self.twMateriasSelecc.setItem(fila, 0, QTableWidgetItem(dato[1])) #columna Materias
            fila += 1

    def agregaMateria(self):

        try:
            if self.twMateriasSelecc.currentRow() > -1:
                id_materia = self.materias[self.twMateriasSelecc.currentRow()][0]
                Model().vinculaDocenteMateria(self.dni, id_materia)
                self.close()

        except sqlite3.IntegrityError:
            QMessageBox.information(self, "Error en Vinculacion de Materia", "Materia ya vinculada al docente")
            self.close()

    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dni = "26534852"
    SeleccionMateria = SeleccionMateria(dni)
    SeleccionMateria.show()
    sys.exit(app.exec_())
