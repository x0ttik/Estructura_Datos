import tkinter as tk
from tkinter import messagebox, ttk
import heapq
from datetime import datetime, timedelta
from collections import deque

class Paciente:
    def __init__(self, id_paciente, nombre, prioridad=0, hora_llegada=None):
        self.id_paciente = id_paciente
        self.nombre = nombre
        self.prioridad = prioridad
        self.hora_llegada = hora_llegada or datetime.now()
        self.hora_atencion = None

class Departamento:
    def __init__(self, nombre):
        self.nombre = nombre
        self.cola_prioridad = []
        self.cola_normal = deque()
        self.pacientes_atendidos = []
        
    def agregar_paciente(self, paciente):
        if paciente.prioridad > 0:
            heapq.heappush(self.cola_prioridad, (-paciente.prioridad, paciente.hora_llegada, paciente))
        else:
            self.cola_normal.append(paciente)
            
    def siguiente_paciente(self):
        if self.cola_prioridad:
            _, _, paciente = heapq.heappop(self.cola_prioridad)
            return paciente
        elif self.cola_normal:
            return self.cola_normal.popleft()
        return None
        
    def ver_siguiente(self):
        if self.cola_prioridad:
            return self.cola_prioridad[0][2]
        elif self.cola_normal:
            return self.cola_normal[0]
        return None
        
    def esta_vacia(self):
        return len(self.cola_prioridad) == 0 and len(self.cola_normal) == 0

class SistemaGestionMedica:
    def __init__(self):
        self.departamentos = {
            'urgencias': Departamento('urgencias'),
            'consulta_general': Departamento('consulta general'),
            'pediatria': Departamento('pediatria')
        }
        self.reservas = {}
        self.contador_pacientes = 1
        
    def registrar_paciente(self, nombre, departamento, prioridad=0):
        paciente = Paciente(self.contador_pacientes, nombre, prioridad)
        self.departamentos[departamento].agregar_paciente(paciente)
        self.contador_pacientes += 1
        return paciente.id_paciente
        
    def atender_paciente(self, departamento):
        if departamento not in self.departamentos:
            return None
            
        depto = self.departamentos[departamento]
        if depto.esta_vacia():
            return None
            
        paciente = depto.siguiente_paciente()
        paciente.hora_atencion = datetime.now()
        depto.pacientes_atendidos.append(paciente)
        return paciente
        
    def ver_proximo_paciente(self, departamento):
        if departamento not in self.departamentos:
            return None
        return self.departamentos[departamento].ver_siguiente()
        
    def calcular_tiempo_espera_promedio(self, departamento):
        if departamento not in self.departamentos:
            return 0
            
        depto = self.departamentos[departamento]
        if not depto.pacientes_atendidos:
            return 0
            
        total_tiempo = 0
        for paciente in depto.pacientes_atendidos:
            if paciente.hora_atencion:
                tiempo_espera = (paciente.hora_atencion - paciente.hora_llegada).total_seconds() / 60
                total_tiempo += tiempo_espera
                
        return total_tiempo / len(depto.pacientes_atendidos)

# Aquí empieza la interfaz gráfica
class InterfazMedica:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Sistema de Gestión Médica")
        self.ventana.geometry("600x500")
        
        # Crear el sistema médico
        self.sistema = SistemaGestionMedica()
        
        # Título principal
        titulo = tk.Label(ventana, text="Sistema de Gestión Médica", 
                        font=("Arial", 16, "bold"), bg="lightblue")
        titulo.pack(pady=10, fill="x")
        
        # Frame para registrar pacientes
        frame_registro = tk.LabelFrame(ventana, text="Registrar Paciente", 
                                    font=("Arial", 12, "bold"), padx=10, pady=10)
        frame_registro.pack(padx=10, pady=10, fill="x")
        
        # Nombre del paciente
        tk.Label(frame_registro, text="Nombre:").grid(row=0, column=0, sticky="w", pady=5)
        self.entrada_nombre = tk.Entry(frame_registro, width=30)
        self.entrada_nombre.grid(row=0, column=1, pady=5)
        
        # Departamento
        tk.Label(frame_registro, text="Departamento:").grid(row=1, column=0, sticky="w", pady=5)
        self.combo_departamento = ttk.Combobox(frame_registro, width=28, state="readonly")
        self.combo_departamento['values'] = ('urgencias', 'consulta_general', 'pediatria')
        self.combo_departamento.current(0)
        self.combo_departamento.grid(row=1, column=1, pady=5)
        
        # Prioridad
        tk.Label(frame_registro, text="Prioridad:").grid(row=2, column=0, sticky="w", pady=5)
        self.combo_prioridad = ttk.Combobox(frame_registro, width=28, state="readonly")
        self.combo_prioridad['values'] = ('0 - Normal', '1 - Urgente', '2 - Emergencia')
        self.combo_prioridad.current(0)
        self.combo_prioridad.grid(row=2, column=1, pady=5)
        
        # Botón registrar
        btn_registrar = tk.Button(frame_registro, text="Registrar Paciente", 
                                bg="green", fg="white", command=self.registrar_paciente)
        btn_registrar.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Frame para atender pacientes
        frame_atencion = tk.LabelFrame(ventana, text="Atender Paciente", 
                                    font=("Arial", 12, "bold"), padx=10, pady=10)
        frame_atencion.pack(padx=10, pady=10, fill="x")
        
        tk.Label(frame_atencion, text="Departamento:").grid(row=0, column=0, sticky="w", pady=5)
        self.combo_dept_atencion = ttk.Combobox(frame_atencion, width=28, state="readonly")
        self.combo_dept_atencion['values'] = ('urgencias', 'consulta_general', 'pediatria')
        self.combo_dept_atencion.current(0)
        self.combo_dept_atencion.grid(row=0, column=1, pady=5)
        
        btn_atender = tk.Button(frame_atencion, text="Atender Siguiente", 
                            bg="blue", fg="white", command=self.atender_paciente)
        btn_atender.grid(row=1, column=0, pady=5, padx=5)
        
        btn_ver_siguiente = tk.Button(frame_atencion, text="Ver Siguiente", 
                                    bg="orange", fg="white", command=self.ver_siguiente)
        btn_ver_siguiente.grid(row=1, column=1, pady=5, padx=5)
        
        # Botón para ver reporte
        btn_reporte = tk.Button(ventana, text="Ver Reporte de Eficiencia", 
                            bg="purple", fg="white", command=self.ver_reporte)
        btn_reporte.pack(pady=10)
        
        # Área de texto para mostrar información
        self.texto_info = tk.Text(ventana, height=10, width=70)
        self.texto_info.pack(padx=10, pady=10)
        
    def registrar_paciente(self):
        # Obtener los datos de los campos
        nombre = self.entrada_nombre.get()
        departamento = self.combo_departamento.get()
        prioridad_texto = self.combo_prioridad.get()
        prioridad = int(prioridad_texto[0])  # Tomar el primer caracter que es el número
        
        # Validar que el nombre no esté vacío
        if not nombre:
            messagebox.showwarning("Advertencia", "Por favor ingrese el nombre del paciente")
            return
            
        # Registrar en el sistema
        id_paciente = self.sistema.registrar_paciente(nombre, departamento, prioridad)
        
        # Mostrar mensaje de confirmación
        messagebox.showinfo("Éxito", f"Paciente {nombre} registrado con ID: {id_paciente}")
        
        # Limpiar el campo de nombre
        self.entrada_nombre.delete(0, tk.END)
        
        # Actualizar el área de texto
        self.actualizar_info(f"✓ Paciente registrado: {nombre} en {departamento}")
        
    def atender_paciente(self):
        departamento = self.combo_dept_atencion.get()
        paciente = self.sistema.atender_paciente(departamento)
        
        if paciente:
            messagebox.showinfo("Atención", f"Atendiendo a: {paciente.nombre}")
            self.actualizar_info(f"✓ Paciente atendido: {paciente.nombre} de {departamento}")
        else:
            messagebox.showinfo("Información", f"No hay pacientes en espera en {departamento}")
            
    def ver_siguiente(self):
        departamento = self.combo_dept_atencion.get()
        paciente = self.sistema.ver_proximo_paciente(departamento)
        
        if paciente:
            messagebox.showinfo("Siguiente Paciente", 
                            f"Siguiente en {departamento}:\n{paciente.nombre}")
        else:
            messagebox.showinfo("Información", f"No hay pacientes en {departamento}")
            
    def ver_reporte(self):
        # Limpiar el área de texto
        self.texto_info.delete(1.0, tk.END)
        
        # Crear el reporte
        self.texto_info.insert(tk.END, "=== REPORTE DE EFICIENCIA ===\n\n")
        
        for nombre_depto, depto in self.sistema.departamentos.items():
            tiempo_promedio = self.sistema.calcular_tiempo_espera_promedio(nombre_depto)
            pacientes_atendidos = len(depto.pacientes_atendidos)
            pacientes_en_espera = len(depto.cola_prioridad) + len(depto.cola_normal)
            
            self.texto_info.insert(tk.END, f"Departamento: {nombre_depto.upper()}\n")
            self.texto_info.insert(tk.END, f"  - Pacientes atendidos: {pacientes_atendidos}\n")
            self.texto_info.insert(tk.END, f"  - Pacientes en espera: {pacientes_en_espera}\n")
            self.texto_info.insert(tk.END, f"  - Tiempo promedio: {tiempo_promedio:.2f} min\n\n")
            
    def actualizar_info(self, mensaje):
        self.texto_info.insert(tk.END, mensaje + "\n")
        self.texto_info.see(tk.END)  # Auto-scroll al final

# Crear la ventana principal
if __name__ == "__main__":
    ventana = tk.Tk()
    app = InterfazMedica(ventana)
    ventana.mainloop()