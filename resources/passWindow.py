from tkinter import *

class PassWindow(Tk):
	"""docstring for PassWindow"""
	
	def __init__(self, arg):
		super(PassWindow, self).__init__()
		self.arg = arg
		

passWindow=Tk()
passWindow.title("Ingreso")
#passWindow.overrideredirect(1)
passWindow.resizable(0,0)
#passWindow.attributes("-toolwindow",1) solo el boton cerrar

passFrame=Frame(passWindow)
passFrame.config(bd=10)

tituloLabel=Label(passFrame, text="Ingrese Usuario y Contraseña")
tituloLabel.grid(row=0, columnspan=2, padx=30, pady=10)
usuarioLabel=Label(passFrame, text="Usuario :")
usuarioLabel.grid(row=1, column=0, sticky="e", padx=10, pady=10)
usuarioEntry=Entry(passFrame) # para deshabilitar , state=DISABLED)
usuarioEntry.grid(row=1, column=1, padx=10, pady=10)
passLabel=Label(passFrame, text="Contraseña :")
passLabel.grid(row=2, column=0, sticky="e", padx=10, pady=10)
passEntry=Entry(passFrame)
passEntry.grid(row=2, column=1, padx=10, pady=10)
passEntry.config(show="*")
passFrame.pack()

# ------------- FRAME INFERIOR -----------

botonFrame=Frame(passWindow)
botonFrame.pack(padx=20, pady=20)

ingresoButton=Button(botonFrame, text="Ingresar", width=10) 
ingresoButton.pack()

passWindow.mainloop()