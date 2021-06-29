#print(grillaProf)
dicGrillaProf = [{"lunes":"","martes":"","miercoles":"","jueves":"","viernes":""},
		{"lunes":"","martes":"","miercoles":"","jueves":"","viernes":""},
		{"lunes":"","martes":"","miercoles":"","jueves":"","viernes":""},
		{"lunes":"","martes":"","miercoles":"","jueves":"","viernes":""}]

dicGrillaProf[0] = {"lunes":"Frank"}
dicGrillaProf[3] = {"jueves":"Pepito"}
dicGrillaProf[2]["lunes"] = "esteban"

#dicParte = dicGrillaProf[0]

grillaProf = []
grillaMate = []


for x in range(0,3):
	grillaProf.append("")
	grillaMate.append("")
	for y in range(0,4):
		grillaProf.append("")
		grillaMate.append("")

def centraString(texto, tamanio):
	espacioIn = int((tamanio - len(texto)) / 2)
	espacioFi = tamanio - espacioIn - len(texto)

	result = ""

	for espIn in range(0,espacioIn):
		result = result +" "

	result = result + texto

	for espIn in range(0,espacioFi):
		result = result +" "
	
	return result

def replica(texto, veces):
	result = ""
	for x in range(0, veces):
		result = result + texto
	return result

td = 20

lensList = [7,td,td,td,td,td]
diasList = ["HORAS", "LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES"]
cuadro = {"recuadoH":"-", "recuadroV":"|", "vertice":"."}

header1 = cuadro["vertice"] 
header2 = cuadro["recuadroV"]
header3 = cuadro["vertice"]

hora11 = cuadro["recuadroV"]
hora12 = cuadro["recuadroV"]
hora13 = cuadro["recuadroV"]
hora14 = cuadro["recuadroV"]

hora21 = cuadro["recuadroV"]
hora22 = cuadro["recuadroV"]
hora23 = cuadro["recuadroV"]
hora24 = cuadro["recuadroV"]

hora31 = cuadro["recuadroV"]
hora32 = cuadro["recuadroV"]
hora33 = cuadro["recuadroV"]
hora34 = cuadro["recuadroV"]

hora41 = cuadro["recuadroV"]
hora42 = cuadro["recuadroV"]
hora43 = cuadro["recuadroV"]
hora44 = cuadro["recuadroV"]


for pr in range(0,6):
	header1 = header1 + replica(cuadro["recuadoH"], lensList[pr]) + cuadro["vertice"]
	header2 = header2 + centraString(diasList[pr], lensList[pr]) + cuadro["recuadroV"]
	
	hora11 = hora11 + centraString(diasList[pr], lensList[pr]) + cuadro["recuadroV"]  
	hora14 = hora14 + centraString(diasList[pr], lensList[pr]) + cuadro["recuadroV"]  

	hora21 = hora21 + centraString(diasList[pr], lensList[pr]) + cuadro["recuadroV"]  
	hora24 = hora24 + centraString(diasList[pr], lensList[pr]) + cuadro["recuadroV"]  

	hora31 = hora31 + centraString(diasList[pr], lensList[pr]) + cuadro["recuadroV"]  
	hora34 = hora34 + centraString(diasList[pr], lensList[pr]) + cuadro["recuadroV"]  

	hora41 = hora41 + centraString(diasList[pr], lensList[pr]) + cuadro["recuadroV"]  
	hora44 = hora44 + centraString(diasList[pr], lensList[pr]) + cuadro["recuadroV"]  


	if pr == 0:
		hora12 = hora12 + centraString("PRIMERA", lensList[pr]) 
		hora13 = hora13 + centraString("HORA", lensList[pr]) 

		hora22 = hora22 + centraString("SEGUNDA", lensList[pr]) 
		hora23 = hora13
	
		hora32 = hora32 + centraString("TERCERA", lensList[pr]) 
		hora33 = hora13
	
		hora42 = hora42 + centraString("CUARTA", lensList[pr]) 
		hora43 = hora13
	else:
		hora12 = hora12 + centraString(diasList[pr], lensList[pr]) + cuadro["recuadroV"]  
		hora13 = hora13 + centraString(diasList[pr], lensList[pr]) + cuadro["recuadroV"]  

		hora22 = hora22 + centraString(diasList[pr], lensList[pr]) + cuadro["recuadroV"]  
		hora23 = hora23 + centraString(diasList[pr], lensList[pr]) + cuadro["recuadroV"]  
	
		hora32 = hora32 + centraString(diasList[pr], lensList[pr]) + cuadro["recuadroV"]  
		hora33 = hora33 + centraString(diasList[pr], lensList[pr]) + cuadro["recuadroV"]  
	
		hora42 = hora42 + centraString(diasList[pr], lensList[pr]) + cuadro["recuadroV"]  
		hora43 = hora43 + centraString(diasList[pr], lensList[pr]) + cuadro["recuadroV"]  
	







print(header1)
print(header2)
print(header1)

print(hora11)
print(hora12)
print(hora13)
print(hora14)

print(header1)

print(hora21)
print(hora22)
print(hora23)
print(hora24)

print(header1)

print(hora21)
print(hora32)
print(hora33)
print(hora34)

print(header1)

print(hora41)
print(hora42)
print(hora43)
print(hora44)

print(header1)