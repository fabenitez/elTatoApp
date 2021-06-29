from datetime import date
from datetime import datetime
from PyQt5.QtCore import QDate, Qt

class Fechas():

	def lmeses(self): 
		"""
		Devuelve lista de meses en español
		"""
		meses=("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Cctubre", "Noviembre", "Diciembre")
		return meses

	def aFecha(self, strFecha):
		"""
		Devuelve un objeto date a partir de una fecha en string
		en formato AAAAMMDD
		""" 
		anio= int(int(strFecha)/10000)
		mes= int((int(strFecha)-(anio*10000))/100)
		dia= int(strFecha)-((anio*10000)+(mes*100))
		#print(anio, mes, dia)
		return QDate(anio, mes, dia)

	
	