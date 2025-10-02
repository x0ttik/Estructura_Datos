import tkinter as tk
from tkinter import messagebox
import heapq
from datetime import datetime
from collections import deque

class Paciente:
    def __init__(self, id_paciente, nombre, departamento, prioridad=0, hora_llegada=None):
        self.id_paciente = id_paciente
        self.nombre = nombre
        self.departamento = departamento
        self.prioridad = prioridad
        self.hora_llegada = hora_llegada or datetime.now()
        self.hora_atencion = None

class SistemaGestionMedica:
    def __init__(self):
        self.cola_prioridad = []
        self.cola_normal = deque()
        self.pacientes_atendidos = []
        self.contador_pacientes = 1
        
    def registrar_paciente(self, nombre, departamento, prioridad=0):
        paciente = Paciente(self.contador_pacientes, nombre, departamento, prioridad)
        
        if paciente.prioridad > 0:
            heapq.heappush(self.cola_prioridad, (-paciente.prioridad, paciente.hora_llegada, paciente))
        else:
            self.cola_normal.append(paciente)
        
        self.contador_pacientes += 1
        return paciente.id_paciente
        
    def atender_siguiente(self):
        if self.cola_prioridad:
            _, _, paciente = heapq.heappop(self.cola_prioridad)
            paciente.hora_atencion = datetime.now()
            self.pacientes_atendidos.append(paciente)
            return paciente
        elif self.cola_normal:
            paciente = self.cola_normal.popleft()
            paciente.hora_atencion = datetime.now()
            self.pacientes_atendidos.append(paciente)
            return paciente
        return None
    
    def hay_pacientes(self):
        return len(self.cola_prioridad) > 0 or len(self.cola_normal) > 0
    
    def contar_en_espera(self):
        return len(self.cola_prioridad) + len(self.cola_normal)
    

# FRONT-END


sistema = SistemaGestionMedica() # Crear el sistema médico

# Funciones 

def registrar():
    
    nombre = entrada_nombre.get()
    departamento = seleccion_departamento.get()
    prioridad = seleccion_prioridad.get()
    
    
    if nombre == "": # Verificar que ingresaron un nombre
        messagebox.showwarning("Advertencia", "Favor de ingresar el nombre del paciente")
        return
    
    # Registrar el paciente
    id_paciente = sistema.registrar_paciente(nombre, departamento, prioridad)
    
    # Mensaje info paciente 
    prioridad_texto = ["Normal", "Urgente", "Emergencia"][prioridad]
    mensaje = f"Paciente #{id_paciente}: {nombre}\nDepartamento: {departamento}\nPrioridad: {prioridad_texto}\n\nRegistrado correctamente"
    messagebox.showinfo("Registro Exitoso", mensaje)
    
    entrada_nombre.delete(0, tk.END) # Actualizamos la caja vacia
    
    
    actualizar_contador() # Actualizar el contador

# Función para atender el siguiente paciente (sin elegir departamento)
def atender():
    paciente = sistema.atender_siguiente()  # Atender al siguiente paciente de la cola general

    
    if paciente:
        prioridad_texto = ["Normal", "Urgente", "Emergencia"][paciente.prioridad]
        messagebox.showinfo("Atendiendo", 
                            f"Paciente #{paciente.id_paciente}: {paciente.nombre}\n"
                            f"Departamento: {paciente.departamento}\n"
                            f"Prioridad: {prioridad_texto}")
        actualizar_contador()
    else:
        messagebox.showinfo("Vacío", "No hay pacientes en espera")

# Función para ver el reporte
def ver_reporte():
    atendidos = len(sistema.pacientes_atendidos)
    en_espera = sistema.contar_en_espera()
    
    # INFO REPORTE
    texto = f"REPORTE GENERAL\n\n"
    texto += f"Pacientes atendidos: {atendidos}\n"
    texto += f"Pacientes en espera: {en_espera}\n\n"
    
    if atendidos > 0:
        texto += "Últimos 5 atendidos:\n"
        ultimos = sistema.pacientes_atendidos[-5:]
        for p in reversed(ultimos):
            prioridad_texto = ["Normal", "Urgente", "Emergencia"][p.prioridad]
            texto += f"  • {p.nombre} - {p.departamento} ({prioridad_texto})\n"
    
    messagebox.showinfo("Reporte", texto)

# Función para actualizar el contador en pantalla
def actualizar_contador():
    contador_esperando = sistema.contar_en_espera()
    contador_atendidos = len(sistema.pacientes_atendidos)
    etiqueta_contador.config(text=f"En espera: {contador_esperando} | Atendidos: {contador_atendidos}")


ventana = tk.Tk() # Creamos la ventana principal 
ventana.title("Sistema Médico")
ventana.geometry("450x550")
ventana.config(bg="lightblue")

# Titulo
etiqueta_principal = tk.Label(ventana, text="SISTEMA MÉDICO", 
                            font=("Arial", 16, "bold"), bg="lightblue")
etiqueta_principal.pack(pady=10)

# Contador de pacientes
etiqueta_contador = tk.Label(ventana, text="En espera: 0 | Atendidos: 0", 
                            font=("Arial", 11), bg="yellow", fg="black")
etiqueta_contador.pack(pady=5)

# Subventana 1

etiqueta_titulo1 = tk.Label(ventana, text="REGISTRAR PACIENTE", 
                            font=("Arial", 14, "bold"), bg="lightblue")
etiqueta_titulo1.pack(pady=10)

# Nombre del paciente
etiqueta_nombre = tk.Label(ventana, text="Nombre del paciente:", 
                        font=("Arial", 11), bg="lightblue")
etiqueta_nombre.pack(pady=5)

entrada_nombre = tk.Entry(ventana, font=("Arial", 11), width=30)
entrada_nombre.pack(pady=5)

# Departamento
etiqueta_dept = tk.Label(ventana, text="Departamento:", 
                        font=("Arial", 11), bg="lightblue")
etiqueta_dept.pack(pady=5)

seleccion_departamento = tk.StringVar(value="urgencias")

seleccion_urgencia = tk.Radiobutton(ventana, text="Urgencias", 
                                variable=seleccion_departamento, value="urgencias",
                                font=("Arial", 10), bg="lightblue")
seleccion_urgencia.pack()

seleccion_consulta = tk.Radiobutton(ventana, text="Consulta General", 
                                variable=seleccion_departamento, value="consulta_general",
                                font=("Arial", 10), bg="lightblue")
seleccion_consulta.pack()

seleccion_pediatria = tk.Radiobutton(ventana, text="Pediatría", 
                                variable=seleccion_departamento, value="pediatria",
                                font=("Arial", 10), bg="lightblue")
seleccion_pediatria.pack()


# Seleccionar prioridad
etiqueta_prioridad = tk.Label(ventana, text="Prioridad:", 
                            font=("Arial", 11), bg="lightblue")
etiqueta_prioridad.pack(pady=5)

seleccion_prioridad = tk.IntVar(value=0)

seleccion_consulta = tk.Radiobutton(ventana, text="Consulta", 
                            variable=seleccion_prioridad, value=0,
                            font=("Arial", 10), bg="lightblue")
seleccion_consulta.pack()

seleccion_emergencia = tk.Radiobutton(ventana, text="Emergencia", 
                                variable=seleccion_prioridad, value=2,
                                font=("Arial", 10), bg="lightblue")
seleccion_emergencia.pack()

# Botón para registrar
boton_registrar = tk.Button(ventana, text="REGISTRAR", 
                            font=("Arial", 12, "bold"), bg="green", fg="white",
                            command=registrar, width=20)
boton_registrar.pack(pady=15)

# Línea separadora
separador = tk.Label(ventana, text="─" * 50, bg="lightblue")
separador.pack()

# Subventana 2

etiqueta_titulo2 = tk.Label(ventana, text="ATENDER PACIENTE", 
                            font=("Arial", 14, "bold"), bg="lightblue")
etiqueta_titulo2.pack(pady=10)

etiqueta_info = tk.Label(ventana, text="(Emergencias tienen prioridad)", 
                        font=("Arial", 9), bg="lightblue", fg="darkblue")
etiqueta_info.pack(pady=5)

boton_atender = tk.Button(ventana, text="ATENDER SIGUIENTE", 
                        font=("Arial", 12, "bold"), bg="blue", fg="white",
                        command=atender, width=20, height=2)
boton_atender.pack(pady=10)

# Botón para ver reporte
boton_reporte = tk.Button(ventana, text="VER REPORTE", 
                        font=("Arial", 12, "bold"), bg="orange", fg="white",
                        command=ver_reporte, width=20)
boton_reporte.pack(pady=10)

# Iniciar la ventana
ventana.mainloop()