
class DocenteMaterias:

	materias = []
	disponibilidad = []
	
	def __init__(self, *args):
		self.disponibilidad = []
		self.dni = args[0][0]
		self.apellido = args[0][1]
		self.nombre = args[0][2]
		self.fechaIngreso = args[0][3]
		nivel = args[0][4]
		

	########## GETTERS

	def getDNI(self):
		return self.dni

	def getApellido(self):
		return self.apellido

	def getNombre(self):
		return self.nombre

	def getFechaIngreso():
		return self.fechaIngreso

	def getMaterias(self):
		return self.materias

	def getDisponibilidad(self):
		return self.disponibilidad

	########## SETTERS

	def setMaterias(self, args):
		self.materias = args

	def setDisponibilidad(self, args):
		self.disponibilidad = args

	######### ACCESOS A LA BBDD

	def deshabilitarDocente(self):
		self.borrado = "1"
		Model().deshabilitaDocente(self)