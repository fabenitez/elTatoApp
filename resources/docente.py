
class Docente:

	def __init__(self, *args):

		self.dni = args[0][0]
		self.apellido = args[0][1]
		self.nombre = args[0][2]
		self.domicilio = args[0][3]
		self.localidad = args[0][4]
		self.codPostal = args[0][5]
		self.fechaIngreso = args[0][6]
		self.eMail = args[0][7]
		self.borrado = args[0][8]
		self.claveActualizacion = args[0][0]

	########## GETTERS

	def getDNI(self):
		return self.dni

	def getApellido(self):
		return self.apellido

	def getNombre(self):
		return self.nombre

	def getDomicilio(self):
		return self.domicilio

	def getLocalidad(self):
		return self.localidad

	def getCodigoPostal(self):
		return self.codPostal

	def getFechaIngreso(self):
		return self.fechaIngreso

	def getEMail(self):
		return self.eMail

	def getBorrado(self):
		return self.borrado

	def getClaveActualizacion(self):
		return self.claveActualizacion

	########## SETTERS

	def setDNI(self, dni):
		self.dni = dni

	def setApellido(self, apellido):
		self.apellido = apellido

	def setNombre(self, nombre):
		self.nombre = nombre

	def setDomicilio(self, domicilio):
		self.domicilio = domicilio

	def setLocalidad(self, localidad):
		self.localidad = localidad

	def setCodigoPostal(self, codPostal):
		self.codPostal = codPostal

	def setFechaIngreso(self, fechaIngreso):
		self.fechaIngreso = fechaIngreso

	def setEMail(self, eMail):
		self.eMail = eMail

	def setClaveActualizacion(self, claveActualizacion):
		self.claveActualizacion = claveActualizacion

	######### ACCESOS A LA BBDD

	def deshabilitarDocente(self):
		self.borrado = "1"
		Model().deshabilitaDocente(self)