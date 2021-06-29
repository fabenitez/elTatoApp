#
# CLASE PassValid creada por Francisco Benitez
# Para gestionar la creacion de password y logins (pines tambien)
class ValidPassword:

	#tipos de seguridad de passwords
	WEAK_PASS = 0 					#normal
	MEDIUM_PASS = 1					#alfanumerica
	HARD_PASS = 2					#alfanumerica con caracter especial
	
	#simbolos obligatorios
	__symbolsAccepted = "&%.$@#" 	#cualquiera de estos simbolos son obligatorios en la pass


	def __init__(self, minChars,typePass):

		if minChars > 0 or minChars <= 25: #limites a la longitud de la pass
			self.__minChars = minChars
		else:
			self.__minChars = 4
			print("Set Default pass length: 4 chars")

		if typePass < self.WEAK_PASS or typePass > self.HARD_PASS:
			self.__typePass = self.WEAK_PASS
			print("Set default type pass: WEAK_PASS")
		else:
			self.__typePass = typePass

		self.__password = ""

			

	def __alphanumeric(self, password):		# debe ser alfanumerica
		txt=tuple(password)

		alpha=False
		numbe=False

		for postxt in txt:
			if postxt.isalnum():
				alpha=True
			if postxt.isnumeric():
				numbe=True
		if alpha and numbe:
			return True
		else:
			return False

		
	def __symbols(self, password):			# debe ser alfanumerica con mayusculas, minusculas y simbolos
		
		if self.__alphanumeric(password):
			txt=tuple(password)
			symbols=tuple(self.__symbolsAccepted)

			upper=False
			lower=False
			symbo=False

			for postxt in txt:
				if postxt.isupper():
					upper = True
				if postxt.islower():
					lower = True
				for possym in symbols:
					if possym == postxt:
						symbo=True
			if upper and lower and symbo:
				return True
			else:
				return False

	def __passWEAK(self, password):
		if len(password) >= self.__minChars: # debe tener la cantidad minima de caracteres
			return True
		else:
			return False

	def __passMEDIUM(self,password):
		if len(password) >= self.__minChars and self.__alphanumeric(password):
			return True
		else:
			return False

	def __passHARD(self, password):
		if self.__passMEDIUM(password) and self.__symbols(password):
			return True
		else:
			return False

	def validatePassword(self, password):
		"""
		Funcion que recibe el password y determina si tiene
		la seguridad seteada:
		WEAK_PASS | MEDIUM_PASS | HARD_PASS
		"""
		if (self.__typePass == self.WEAK_PASS and self.__passWEAK(password)) or (self.__typePass == self.MEDIUM_PASS and self.__passMEDIUM(password)) or (self.__typePass == self.HARD_PASS and self.__passHARD(password)):
			self.__password = password
			return True
		else:
			return False



	def clearAll(self):
		self.leUsuario.setText("")
		self.lePassword.setText("")


	def getConfig(self):
		print("Tipo de Password: ",self.__typePass, " Cantidad minima de caracteres: ",self.__minChars)



"""
logger=Logger(6,Logger.MEDIUM_PASS)

logger.validatePassword("Tella.s")
logger.getConfig()
print(logger.getPassword())
"""