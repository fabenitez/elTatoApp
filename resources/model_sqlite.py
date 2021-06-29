import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QTableWidgetItem
from PyQt5 import uic
from PyQt5.QtCore import QDate, Qt
from resources.docente import Docente
from resources.docenteMaterias import DocenteMaterias
import pathlib
from pathlib import Path


class Model:
	"""
	*******************************************
	* Modelo de datos para una BBDD sqlite    *
	*******************************************
	"""
	def __init__(self):
		pathAbsolute = str(pathlib.Path().absolute())
		self.db_file = pathAbsolute + "\\resources\\tatoDB.db"

	def open_db(self):
		self.connection = sqlite3.connect(self.db_file)
		self.cursor=self.connection.cursor()
	
	def close_db(self):
		self.connection.close()

	########### Métodos que acceden a tabla users #############################

	def insertUsuario(self, datos):
		self.open_db()
		self.cursor.execute("INSERT INTO users VALUES(?,?,?,?)", (datos))
		self.connection.commit()
		self.close_db()

	def updateUsuario(self, datos):
		self.open_db()
		self.cursor.execute("UPDATE users SET password=?, acceso=?, vto=? WHERE user=?", (datos))
		self.connection.commit()
		self.close_db()

	def updatePassword(self, datos):
		self.open_db()
		self.cursor.execute("UPDATE users SET password=?, vto=? WHERE user=?", (datos))
		self.connection.commit()
		self.close_db()

	def eliminaUsuario(self, dato):
		self.open_db()
		self.cursor.execute("DELETE FROM users WHERE user='"+dato+"'")
		self.connection.commit()
		self.close_db()

	def selectUsuario(self, dato):
		self.open_db()
		self.cursor.execute("SELECT user, password, acceso, vto FROM users WHERE user LIKE '%" + dato + "%'")
		usuarios=self.cursor.fetchall()
		self.connection.commit()
		self.close_db()
		return usuarios

	def selectUsuarioExacto(self, dato):
		self.open_db()
		self.cursor.execute("SELECT user, password, acceso, vto FROM users WHERE user LIKE '" + dato + "'")
		usuarios=self.cursor.fetchall()
		self.connection.commit()
		self.close_db()
		return usuarios

	def selectUsuarioPass(self, datos):
		self.open_db()
		self.cursor.execute("SELECT user, password, acceso, vto FROM users WHERE user=? AND password=?", (datos))
		usuarios=self.cursor.fetchall()
		self.connection.commit()
		self.close_db()
		return usuarios

	########### Métodos relacionados a la tabla profesor #############################

	def nuevoDocente(self, docente):
		self.open_db()
		self.cursor.execute("INSERT INTO profesor VALUES('"+ docente.getDNI()
			+ "','" + docente.getApellido() 
			+ "','" + docente.getNombre() 
			+ "','" + docente.getDomicilio() 
			+ "','" + docente.getLocalidad()  
			+ "','" + docente.getCodigoPostal() 
			+ "','" + docente.getFechaIngreso() 
			+ "','" + docente.getEMail() 
			+ "', 0)") 
		self.connection.commit()
		self.close_db()

	def selectBusquedaDocente(self, dato):
		self.open_db()
		self.cursor.execute("SELECT dni, apellido, nombre FROM profesor "
			+"WHERE borrado = 0 AND (dni LIKE '%" + dato 
			+"%' OR apellido LIKE '%" + dato 
			+"%' OR nombre LIKE '%" + dato + "%')")

		docentes=self.cursor.fetchall()
		self.connection.commit()
		self.close_db()
		return docentes

	def selectDocenteExacto(self, dni):
		self.open_db()
		self.cursor.execute("SELECT * FROM profesor WHERE dni LIKE '" + dni + "'")
		resultQuery = self.cursor.fetchall()
		docente = Docente(resultQuery[0])
		self.connection.commit()
		self.close_db()
		return docente

	def listaDocenteMateriasNivel(self, anio, turno, nivel):
		self.open_db()
		docenteList = []
		self.cursor.execute("SELECT DISTINCT p.dni, p.apellido, p.nombre, p.fecha_ingreso, m.nivel "+
			"FROM profesor p " +
			"LEFT JOIN profesor_materia pm ON p.dni = pm.dni " +
			"LEFT JOIN materia m ON pm.id_materia = m.id_materia " +
			"LEFT JOIN dispon_profesor dp ON p.dni = dp.dni " +
			"WHERE m.nivel = " + nivel +
			" AND turno = '" + turno + 
			"' AND anio = '" + anio + 
			"' ORDER BY fecha_ingreso")
		resultQuery = self.cursor.fetchall()
		for registro in resultQuery:
			docenteList.append(DocenteMaterias(registro))
		self.connection.commit()
		self.close_db()
		return docenteList

	def traeMateriasProfesorNivel(self, dni, nivel):
		self.open_db()
		self.cursor.execute("SELECT m.id_materia, m.materia, m.hscatedra " +
			"FROM profesor p " +
			"LEFT JOIN profesor_materia pm ON p.dni = pm.dni " +
			"LEFT JOIN materia m ON pm.id_materia = m.id_materia " +
			"WHERE m.nivel = " + nivel +
			" AND p.dni = '" + dni + "'")
		materiaList = self.cursor.fetchall()
		self.connection.commit()
		self.close_db()
		return materiaList


	def verificaDocente(self, dni):
		self.open_db()
		self.cursor.execute("SELECT * FROM profesor WHERE dni LIKE '" + dni + "'")
		resultQuery = self.cursor.fetchall()
		self.connection.commit()
		self.close_db()
		return resultQuery

	def habilitaDocente(self, dni):
		self.open_db()
		self.cursor.execute("UPDATE profesor SET borrado = 0 WHERE dni='"+ dni +"'")
		self.connection.commit()
		self.close_db()

	def actualizaDocente(self, docente):
		self.open_db()
		self.cursor.execute("UPDATE profesor SET dni = '"+ docente.getDNI()
			+"', apellido='"+ docente.getApellido()	
			+"', nombre='"+ docente.getNombre()
			+"', domicilio='"+ docente.getDomicilio()
			+"', localidad='"+ docente.getLocalidad()	
			+"', cod_postal='"+ docente.getCodigoPostal()	
			+"', fecha_ingreso='"+ docente.getFechaIngreso()
			+"', email='"+ docente.getEMail()
			+"' WHERE dni='"+ docente.getClaveActualizacion()+"'")
		self.connection.commit()
		self.close_db()

	def deshabilitaDocente(self, dni):
		self.open_db()
		self.cursor.execute("UPDATE profesor SET borrado = 1 WHERE dni='"+ dni +"'")
		self.connection.commit()
		self.close_db()

	def guardaDisponibilidad(self, args):
		self.open_db()
		for registro in args:
			self.cursor.execute("INSERT INTO dispon_profesor (dni, anio, turno, dia, hora) VALUES (?,?,?,?,?)", (registro)) 
		self.connection.commit()
		self.close_db()

	def verificaDispo(self, datos):
		self.open_db()
		self.cursor.execute("SELECT dia, hora FROM dispon_profesor WHERE dni = ? AND anio = ? AND turno = ?", (datos))
		resultQuery = self.cursor.fetchall()
		self.connection.commit()
		self.close_db()
		return resultQuery

	def selectTelefonoDocente(self, dni):
		self.open_db()
		self.cursor.execute("SELECT nro_tele, tipo FROM telefono_profesor WHERE dni = '" + dni + "'")
		resultQuery = self.cursor.fetchall()
		self.connection.commit()
		self.close_db()
		return resultQuery

	def agregaTelefonoDocente(self, dni, telefono, aclaracion):
		self.open_db()
		self.cursor.execute("INSERT INTO telefono_profesor (dni, nro_tele, tipo) VALUES ('" + dni + "', '" + telefono + "','" + aclaracion + "')" )
		self.connection.commit()
		self.close_db()


	def eliminaTelefono(self, dni, telefono):
		self.open_db()
		self.cursor.execute("DELETE FROM telefono_profesor WHERE dni = '" + dni 
			+ "' AND nro_tele = '" + telefono + "'")
		resultQuery = self.cursor.fetchall()
		print(resultQuery)
		self.connection.commit()
		self.close_db()
		return resultQuery

	def selectMateriaDocente(self, dni):
		self.open_db()
		self.cursor.execute("SELECT m.id_materia, m.materia, m.nivel FROM profesor_materia pm INNER JOIN materia m ON pm.id_materia = m.id_materia WHERE pm.dni = " + dni + " ORDER BY m.materia")
		resultQuery = self.cursor.fetchall()
		self.connection.commit()
		self.close_db()
		return resultQuery

	def selectMateriaNoDocente(self, dni):
		self.open_db()
		self.cursor.execute("SELECT m.id_materia, m.materia, m.nivel FROM materia m WHERE m.id_materia not in (SELECT id_materia FROM profesor_materia WHERE dni = '" + dni + "') ORDER BY m.materia")
		resultQuery = self.cursor.fetchall()
		self.connection.commit()
		self.close_db()
		return resultQuery


	def desvinculaDocenteMateria(self, dni, id_materia):
		self.open_db()
		self.cursor.execute("DELETE FROM profesor_materia WHERE dni = '" + dni + "' AND id_materia = " + str(id_materia) )
		self.connection.commit()
		self.close_db()
		

	def vinculaDocenteMateria(self, dni, id_materia):
		self.open_db()
		self.cursor.execute("INSERT INTO profesor_materia (dni, id_materia) VALUES ('" + dni + "', " + str(id_materia) + ")" )
		self.connection.commit()
		self.close_db()

	########### Métodos vinculado a la tabla materia #############################

	def selectMaterias(self):
		self.open_db()
		self.cursor.execute("SELECT * FROM materia ORDER BY materia")
		resultQuery = self.cursor.fetchall()
		self.connection.commit()
		self.close_db()
		return resultQuery

	def agregaMateria(self, datos):
		self.open_db()
		self.cursor.execute("INSERT INTO materia (materia, nivel, hscatedra) VALUES (?,?,?)", (datos))
		self.connection.commit()
		self.close_db()

	def selectMateriaExacta(self, datos):
		self.open_db()
		self.cursor.execute("SELECT * FROM materia WHERE materia = '" + datos[0] + "' AND nivel = "+ datos[1] +" AND hscatedra = " + datos[2])
		resultQuery = self.cursor.fetchall()
		self.connection.commit()
		self.close_db()
		return resultQuery

	def selectMateriasPorNombreLike(self, nombre):
		self.open_db()
		self.cursor.execute("SELECT * FROM materia WHERE materia LIKE '%" + nombre + "%'" )
		resultQuery = self.cursor.fetchall()
		self.connection.commit()
		self.close_db()
		return resultQuery

	def actualizaMateria(self, materia):
		self.open_db()
		self.cursor.execute("UPDATE materia SET materia = '" + materia[1] 
			+ "', nivel = " + materia[2] 
			+ ", hscatedra = " + materia[3] 
			+ " WHERE id_materia ="+ str(materia[0]) )
		self.connection.commit()
		self.close_db()

	########### Métodos vinculado a CURSOS #############################

	def traeConfigCursos(self, anio):
		self.open_db()
		self.cursor.execute("SELECT cursos FROM cursos " +
			 "WHERE anio = '" + anio + "'")
		resultQuery = self.cursor.fetchall()
		self.connection.commit()
		self.close_db()
		return resultQuery

	def configuraCursos(self, anio, turno, nivel, cursos):
		self.open_db()
		self.cursor.execute("UPDATE cursos SET cursos = '" + cursos 
			+ "' WHERE turno = '" + turno
			+ "' AND nivel = " + nivel
			+ " AND anio = '" + anio + "'")
		self.connection.commit()
		self.close_db()

	def traeCursos(self, anio, turno, nivel):
		self.open_db()
		self.cursor = self.cursor.execute("SELECT cursos FROM cursos " +
			"WHERE turno = '" + turno + "' " +
			"AND nivel = " + nivel +
			" AND anio = '" + anio + "'")
		resultQuery = self.cursor.fetchall()
		self.connection.commit()
		self.close_db()
		return resultQuery

	def generaConfigCursos(self, anio):
		self.open_db()
		self.cursor = self.cursor.execute("INSERT INTO cursos  " +
			"VALUES ('" + anio + "', 'MAÑANA', 1, '000')," +
			"('" + anio + "', 'MAÑANA', 2, '000')," +
			"('" + anio + "', 'MAÑANA', 3, '000')," +
			"('" + anio + "', 'TARDE', 1, '000')," +
			"('" + anio + "', 'TARDE', 2, '000')," +
			"('" + anio + "', 'TARDE', 3, '000')" )
		self.connection.commit()
		self.cursor.execute("SELECT cursos FROM cursos " +
			 "WHERE anio = '" + anio + "'")
		resultQuery = self.cursor.fetchall()
		self.connection.commit()
		self.close_db()
		return resultQuery


	########### Métodos vinculado a la GRILLA #############################

	def cantMateriasNivel(self, nivel):
		self.open_db()
		self.cursor = self.cursor.execute("SELECT count(*) FROM materia m WHERE nivel = " + nivel)
		resultQuery = self.cursor.fetchall()
		self.connection.commit()
		self.close_db()
		return resultQuery

	def cantMateriasConProfesores(self, nivel):
		self.open_db()
		self.cursor = self.cursor.execute("SELECT count(DISTINCT m.materia) from materia m " +
			"LEFT JOIN profesor_materia pm ON pm.id_materia=m.id_materia " +
			"LEFT JOIN profesor p  ON p.dni=pm.dni " +
			"WHERE p.borrado = 0 AND m.nivel = " + nivel)
		resultQuery = self.cursor.fetchall()
		self.connection.commit()
		self.close_db()
		return resultQuery

	def disponibilidadDia(self, datos):
		self.open_db()
		self.cursor = self.cursor.execute("SELECT dp.dia, dp.hora from materia m " +
			"inner join profesor_materia pm on m.id_materia = pm.id_materia " +
			"inner join dispon_profesor dp on pm.dni = dp.dni " +
			"where dp.anio='" + datos[0] + "' " +
			"and dp.turno='" + datos[1] + "' " +
			"and m. nivel = " + datos[2] + " " +
			"and dp.utilizada = 0 " +
			"group by dp.dia, dp.hora " +
			"order by count(m.id_materia) ")
		resultQuery = self.cursor.fetchall()
		self.connection.commit()
		self.close_db()
		return resultQuery

	def disponiblidadUtilizada(self, datos):
		self.open_db()
		self.cursor = self.cursor.execute("SELECT * from dispon_profesor dp " +
			"where dp.anio = '" + datos[0] + "' " +
			"and dp.turno = '" + datos[1] + "' " +
			"and dp.dia = '" + datos[2] + "' " + 
			"and dp.hora = '" + datos[3] + "' " +
			"and dp.curso = '" + datos[4] + "' " +
			"and dp.utilizada = 1 ")
		resultQuery = self.cursor.fetchall()
		self.connection.commit()
		self.close_db()
		return resultQuery

	def materiasProfesoresAlgoritmo(self, anio, turno, dia, hora, nivel, curso):
		self.open_db()
		self.cursor = self.cursor.execute("SELECT m.id_materia, m.materia, m.hscatedra, pm.dni, p.apellido, p.nombre  " +
			"from materia m " +
			"inner join profesor_materia pm " +
			"	on m.id_materia = pm.id_materia " +
			"inner join dispon_profesor dp " +
			"	on pm.dni = dp.dni " +
			"inner join profesor p " +
			"	on dp.dni = p.dni " +
			"inner join (select disp.dni, count(dni) as tot_dispo from dispon_profesor disp "
			"		where utilizada = 0 " +
			"		and anio = '" + anio + "' " +
			"		and turno ='" + turno + "' " +
			"		group by dni) as dispos " +
			"	on p.dni = dispos.dni " +
			"inner join (select dni, count(id_materia) as mat_dar from profesor_materia " +
			"		group by dni) as matsXdar " +
			"	on pm.dni = matsXdar.dni " +
			"where m.nivel = " + nivel + " "
			"and dp.anio ='" + anio + "' "
			"and dp.turno ='" + turno + "' "
			"and dp.dia ='" + dia + "' "
			"and dp.hora='" + hora + "' "
			"and dp.utilizada = 0 "
			"and dispos.tot_dispo >= m.hscatedra "
			"and m.id_materia not in ( select DISTINCT id_materia from dispon_profesor dp "
			"		where dp.anio='" + anio + "' "
			"		and dp.turno='" + turno + "' "
			"		and dp.curso='" + curso + "' "
			"		and dp.utilizada = 1) "
			"order by m.hscatedra DESC, matsXdar.mat_dar, p.fecha_ingreso")
		resultQuery = self.cursor.fetchall()
		self.connection.commit()
		self.close_db()
		return resultQuery
		
	def profesorDiaExacto(self, datos):
		self.open_db()
		self.cursor = self.cursor.execute("select * from dispon_profesor dp " +
			"where dni = '" + datos[0] + "' " +
			"and dp.anio ='" + datos[1] + "' " +
			"and dp.turno ='" + datos[2] + "' " +
			"and dp.dia ='" + datos[3] + "' " +
			"and dp.hora ='" + datos[4] + "' " +
			"and dp.utilizada = 0 ")
		resultQuery = self.cursor.fetchall()
		self.connection.commit()
		self.close_db()
		return resultQuery

	def dispoProfesorNoDia(self, datos):
		self.open_db()
		self.cursor = self.cursor.execute("select DISTINCT dp.* from dispon_profesor dp " +
			"inner join (SELECT dp.anio, dp.turno, dp.dia, dp.hora, count(m.id_materia) as tot_m from materia m " +
			"	inner join profesor_materia pm on m.id_materia = pm.id_materia " +
			"	inner join dispon_profesor dp on pm.dni = dp.dni " +
			"	where dp.anio='" + datos[1] + "' " +
			"	and dp.turno='" + datos[2] + "' " +
			"	and m. nivel = " + datos[4] + " " +
			"	and dp.utilizada = 0 " +
			"	group by dp.dia, dp.hora " +
			"	order by count(dp.dni)) as scon " +
			"on dp.anio = scon.anio " +
			"and dp.turno = scon.turno " +
			"and dp.dia = scon.dia " +		
			"where dni = '" + datos[0] + "' " +
			"and dp.anio='" + datos[1] + "' " +
			"and dp.turno ='" + datos[2] + "' " +
			"and dp.dia not like '" + datos[3] + "' " +
			"and dp.utilizada = 0 " +
			"order by tot_m")
		resultQuery = self.cursor.fetchall()
		self.connection.commit()
		self.close_db()
		return resultQuery



	def quitarDisponibilidad(self, datos):
		self.open_db()
		self.cursor = self.cursor.execute("UPDATE dispon_profesor " +
			"set utilizada = 1, id_materia = " + datos[5] + ", curso = '" + datos[6] + "' "
			"where dni = '" + datos[0] + "' " +
			"and anio='" + datos[1] + "' " +
			"and turno='" + datos[2] + "' " +
			"and dia = '" + datos[3] + "' " +
			"and hora = '" + datos[4] + "' " +
			"and utilizada = 0")
		self.connection.commit()
		self.close_db()

	def dispoLibre(self, datos):
		self.open_db()
		self.cursor = self.cursor.execute("select * from dispon_profesor dp "
			"where dp.anio='" + datos[0] + "' " +
			"and dp.turno='" + datos[1] + "' " +
			"and dp.dia ='" + datos[2] + "' " +
			"and dp.hora = '" + datos[3] + "' " +
			"and dp.curso = '" + datos[4] + "' " +
			"and dp.utilizada = 1")
		resultQuery = self.cursor.fetchall()
		self.connection.commit()
		self.close_db()
		if len(resultQuery) > 0:
			return False
		else: 
			return True

	def materiaTomada(self, datos):
		self.open_db()
		self.cursor = self.cursor.execute("select * from dispon_profesor dp " +
			"where dp.anio='" + datos[0] + "' " + 
			"and dp.turno='" + datos[1] + "' " +
			"and dp.id_materia = " + datos[2] + " " +
			"and dp.utilizada = 1")
		resultQuery = self.cursor.fetchall()
		self.connection.commit()
		self.close_db()
		return resultQuery

	def vuelveAtrasModificaciones(self, datos):
		self.open_db()
		self.cursor = self.cursor.execute("UPDATE dispon_profesor " +
			"set utilizada = 0, id_materia = NULL, curso = NULL " + 
			"where dni = '" + datos[0] + "' " + 
			"and anio ='" + datos[1] + "' " +
			"and turno ='" + datos[2] + "' " +
			"and dia ='" + datos[3] + "' " 
			"and hora ='" + datos[4] + "'")
		self.connection.commit()
		self.close_db()

	def guardaPreGrilla(self, datos):
		self.open_db()
		self.cursor = self.cursor.execute("INSERT INTO pre_grilla values" + 
			"('" + datos[0] + 
			"', " + str(datos[6]) + 
			", '" + datos[1] + 
			"', '" + datos[2] + 
			"', " + str(datos[3]) + 
			", '" + datos[4] + 
			"', '" + str(datos[5]) +
			"', '" + datos[7] + "')")
		self.connection.commit()
		self.close_db()

	def eliminarPreGrilla(self, datos):
		self.open_db()
		self.cursor = self.cursor.execute("DELETE FROM pre_grilla WHERE " + 
			"dni = '" + datos[0] + "' " +
			"and anio = '" + datos[1] + "' " +
			"and turno = '" + datos[2] + "' " + 
			"and dia = '" + datos[3] + "' " + 
			"and hora = '" + datos[4] + "'")
		self.connection.commit()
		self.close_db()

	def limpiaPreGrilla(self):
		self.open_db()
		self.cursor = self.cursor.execute("DELETE FROM pre_grilla ")
		self.connection.commit()
		self.close_db()

		#[otrodni, self.anio, self.turno, dia_o, str(horaMat)])

	def guardaGrilla(self):
		self.open_db()
		self.cursor = self.cursor.execute("INSERT INTO grilla SELECT * FROM pre_grilla")
		self.connection.commit()
		self.close_db()

	def diaTomado(self, anio, turno, dia, hora, curso):
		self.open_db()
		self.cursor = self.cursor.execute("select * from dispon_profesor dp " +
			"where dp.anio = '" + anio + "' " + 
			"and dp.turno = '" + turno + "' " +
			"and dp.dia = '" + dia + "' " +
			"and dp.hora = '" + hora + "' " +
			"and dp.curso = '" + curso + "' " +
			"and dp.utilizada = 1")
		resultQuery = self.cursor.fetchall()
		self.connection.commit()
		self.close_db()
		return resultQuery

	def dispoProfesorAnioTurno(self, dni, anio, turno, curso):
		self.open_db()
		self.cursor = self.cursor.execute("select DISTINCT dp.* from dispon_profesor dp " +
			"inner join (select anio, turno, dia, hora " +
			"	from dispon_profesor " +
			"	where anio = '" + anio + "' " +
			"	and turno = '" + turno + "' " +
			"	and utilizada=1 " +
			"	and curso = '" + curso + "') as disp " +
			"	on dp.anio = disp.anio and dp.turno = disp.turno " +
			"where dni = '" + dni + "' " +
			"and dp.anio ='" + anio + "' " +
			"and dp.turno ='" + turno + "' " +
			"and dp.dia <> disp.dia " +
			"and dp.hora <> disp.hora " +
			"and dp.utilizada = 0")
		resultQuery = self.cursor.fetchall()
		self.connection.commit()
		self.close_db()
		return resultQuery

	def liberaTodasDispos(self, datos):
		self.open_db()
		self.cursor = self.cursor.execute("update dispon_profesor set utilizada = 0, id_materia = NULL, curso = NULL " +
			"where anio = '" + datos[0] + "' " +
			"and turno = '" + datos[1] + "' " +
			"and curso = '" + datos[3] + "' " +
			"and id_materia in(select id_materia " +
			"	from materia " +
			"	where nivel = " + datos[2] + ")")
		resultQuery = self.cursor.fetchall()
		self.connection.commit()
		self.close_db()
		return resultQuery


	def grillaCreada(self, anio, turno, nivel, curso):

		self.open_db()
		self.cursor = self.cursor.execute("select * from grilla  " +
			"where anio='" + anio + "' " + 
			"and turno='" + turno + "' " +
			"and nivel = " + nivel + " " +
			"and curso = '" + curso + "'")
		resultQuery = self.cursor.fetchall()
		self.connection.commit()
		self.close_db()
		return resultQuery

	def traeAniosGrilla(self):
		self.open_db()
		self.cursor = self.cursor.execute("select DISTINCT anio from grilla")
		resultQuery = self.cursor.fetchall()
		self.connection.commit()
		self.close_db()
		return resultQuery

	def selectPreGrilla(self):
		self.open_db()
		self.cursor = self.cursor.execute("select * from pre_grilla")
		resultQuery = self.cursor.fetchall()
		self.connection.commit()
		self.close_db()
		return resultQuery


	def traeTurnosGrilla(self, anio):
		self.open_db()
		self.cursor = self.cursor.execute("select DISTINCT turno from grilla " +
			"where anio ='" + anio + "'")
		resultQuery = self.cursor.fetchall()
		self.connection.commit()
		self.close_db()
		return resultQuery

	def traeNivelesGrilla(self, anio, turno):
		self.open_db()
		self.cursor = self.cursor.execute("select DISTINCT nivel from grilla " +
			"where anio ='" + anio + "' " +
			"and turno ='" + turno + "'")
		resultQuery = self.cursor.fetchall()
		self.connection.commit()
		self.close_db()
		return resultQuery
		
	def traeCursosGrilla(self, anio, turno, nivel):
		self.open_db()
		self.cursor = self.cursor.execute("select DISTINCT curso from grilla " +
			"where anio ='" + anio + "' " +
			"and turno ='" + turno + "' " +
			"and nivel =" + nivel + "")
		resultQuery = self.cursor.fetchall()
		self.connection.commit()
		self.close_db()
		return resultQuery

	def traeGrillaCreada(self, anio, turno, nivel, curso):
		self.open_db()
		self.cursor = self.cursor.execute("select * from grilla " +
			"where anio ='" + anio + "' " +
			"and turno ='" + turno + "' " +
			"and nivel =" + nivel + " " +
			"and curso = '" + curso + "'")
		resultQuery = self.cursor.fetchall()
		self.connection.commit()
		self.close_db()
		return resultQuery

	def traeProfesor(self, dni):
		self.open_db()
		self.cursor = self.cursor.execute("select apellido, nombre from profesor " +
			"where dni ='" + dni + "' ")
		resultQuery = self.cursor.fetchall()
		self.connection.commit()
		self.close_db()
		return resultQuery

	def traeMateria(self, id_materia):
		self.open_db()
		self.cursor = self.cursor.execute("select materia from materia " +
			"where id_materia =" + str(id_materia))
		resultQuery = self.cursor.fetchall()
		self.connection.commit()
		self.close_db()
		return resultQuery



"""
conn=Model()
usuarios=conn.selectUsuario('feli')
print(usuarios)
"""

