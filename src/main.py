import tkinter as tk
from tkinter import ttk, messagebox, font
from tkinter.simpledialog import askstring
import mysql.connector
import os
import pandas as pd
from sqlalchemy import create_engine
from conexion_bd import conectar_bd
import matplotlib.pyplot as plt
from operaciones_crud import (
    agregar_encuesta,
    
    actualizar_encuesta,
    eliminar_encuesta,
    
)
from exportar_a_excel import exportar_a_excel
from visualizar_datos import grafico_consumo_edad

class EncuestasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Encuestas")
        self.root.geometry("1200x800")
        self.root.configure(bg="#1E1E1E")
        
        # Configurar estilo
        self.setup_styles()
        
        # Crear notebook (sistema de pestañas)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Crear las diferentes pestañas
        self.create_input_tab()
        self.create_view_tab()
        self.create_edit_tab()
        self.create_analysis_tab()
        
    def setup_styles(self):
        # Configurar estilos personalizados
        style = ttk.Style()
        style.theme_use('default')
        
        # Configurar estilo para el notebook
        style.configure('TNotebook', background="#1E1E1E")
        style.configure('TNotebook.Tab', padding=[20, 10], font=('Helvetica', 10, 'bold'))
        
        # Configurar estilo para los frames
        style.configure('Card.TFrame', background="#2E2E2E")
        
        # Configurar estilo para las etiquetas
        style.configure('White.TLabel', background="#2E2E2E", foreground="white", font=('Helvetica', 10))
        
        # Configurar estilo para los botones
        style.configure('Accent.TButton', font=('Helvetica', 10, 'bold'))
        
    def create_input_tab(self):
        input_frame = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(input_frame, text='Nueva Encuesta')
        
        # Crear un frame con scroll para el formulario
        canvas = tk.Canvas(input_frame, bg="#2E2E2E")
        scrollbar = ttk.Scrollbar(input_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Card.TFrame')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Campos del formulario
        self.form_fields = {}
        fields = [
            ("Edad:", "entry"),
            ("Sexo:", "entry"),
            ("Bebidas por Semana:", "entry"),
            ("Cervezas por Semana:", "entry"),
            ("Bebidas Fin de Semana:", "entry"),
            ("Bebidas Destiladas por Semana:", "entry"),
            ("Vinos por Semana:", "entry"),
            ("Pérdidas de Control:", "entry"),
            ("Diversión Dependencia Alcohol:", "combobox", ["SI", "NO"]),
            ("Problemas Digestivos:", "combobox", ["SI", "NO"]),
            ("Tensión Alta:", "combobox", ["SI", "NO"]),
            ("Dolores de Cabeza:", "combobox", ["SI", "NO"])
        ]
        
        for i, field in enumerate(fields):
            label = ttk.Label(scrollable_frame, text=field[0], style='White.TLabel')
            label.grid(row=i, column=0, padx=10, pady=5, sticky="e")
            
            if field[1] == "entry":
                widget = ttk.Entry(scrollable_frame, width=30)
            else:  # combobox
                widget = ttk.Combobox(scrollable_frame, values=field[2], width=27)
                widget.set('')
            
            widget.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            self.form_fields[field[0]] = widget
        
        # Botón de guardar
        save_button = ttk.Button(
            scrollable_frame,
            text="Guardar Encuesta",
            command=self.save_survey,
            style='Accent.TButton'
        )
        save_button.grid(row=len(fields), column=0, columnspan=2, pady=20)
        
        # Empaquetar todo
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)
        
    def create_view_tab(self):
        view_frame = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(view_frame, text='Ver Encuestas')
        
        # Filtros superiores
        filter_frame = ttk.Frame(view_frame, style='Card.TFrame')
        filter_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(filter_frame, text="Filtrar por Sexo:", style='White.TLabel').pack(side='left', padx=5)
        self.filter_sex = ttk.Entry(filter_frame, width=10)
        self.filter_sex.pack(side='left', padx=5)
        
        ttk.Button(
            filter_frame,
            text="Aplicar Filtro",
            command=self.apply_filter,
            style='Accent.TButton'
        ).pack(side='left', padx=5)
        
        ttk.Button(
            filter_frame,
            text="Exportar Filtrado",
            command=self.export_filtered,
            style='Accent.TButton'
        ).pack(side='left', padx=5)
        
        # Tabla de resultados
        self.tree = ttk.Treeview(view_frame, show='headings')
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Configurar columnas
        columns = ["ID", "Edad", "Sexo", "Bebidas/Sem", "Cervezas/Sem", "Bebidas Fin/Sem",
                  "Destiladas/Sem", "Vinos/Sem", "Pérdidas Control", "Diversión",
                  "Prob. Digestivos", "Tensión", "Dolor Cabeza"]
        self.tree['columns'] = columns
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=90)
        
        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(view_frame, orient='vertical', command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)
        
    def create_edit_tab(self):
        edit_frame = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(edit_frame, text='Editar/Eliminar')
        
        # Frame para actualizar
        update_frame = ttk.LabelFrame(edit_frame, text="Actualizar Encuesta", style='Card.TFrame')
        update_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(update_frame, text="ID:", style='White.TLabel').pack(side='left', padx=5)
        self.update_id = ttk.Entry(update_frame, width=10)
        self.update_id.pack(side='left', padx=5)
        
        ttk.Label(update_frame, text="Campo:", style='White.TLabel').pack(side='left', padx=5)
        self.update_field = ttk.Entry(update_frame, width=20)
        self.update_field.pack(side='left', padx=5)
        
        ttk.Label(update_frame, text="Nuevo Valor:", style='White.TLabel').pack(side='left', padx=5)
        self.update_value = ttk.Entry(update_frame, width=20)
        self.update_value.pack(side='left', padx=5)
        
        ttk.Button(
            update_frame,
            text="Actualizar",
            command=self.update_survey,
            style='Accent.TButton'
        ).pack(side='left', padx=5)
        
        # Frame para eliminar
        delete_frame = ttk.LabelFrame(edit_frame, text="Eliminar Encuesta", style='Card.TFrame')
        delete_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(delete_frame, text="ID:", style='White.TLabel').pack(side='left', padx=5)
        self.delete_id = ttk.Entry(delete_frame, width=10)
        self.delete_id.pack(side='left', padx=5)
        
        ttk.Button(
            delete_frame,
            text="Eliminar",
            command=self.delete_survey,
            style='Accent.TButton'
        ).pack(side='left', padx=5)
        
    def create_analysis_tab(self):
        analysis_frame = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(analysis_frame, text='Análisis')
        
        # Botones para diferentes tipos de análisis
        ttk.Button(
            analysis_frame,
            text="Generar Gráfico de Consumo por Edad",
            command=self.create_graph,
            style='Accent.TButton'
        ).pack(pady=10)
        
        ttk.Button(
            analysis_frame,
            text="Exportar Todo a Excel",
            command=self.export_all,
            style='Accent.TButton'
        ).pack(pady=10)
        
    def save_survey(self):
        try:
            data = {
                'edad': int(self.form_fields['Edad:'].get()),
                'sexo': self.form_fields['Sexo:'].get(),
                'bebidas_semana': int(self.form_fields['Bebidas por Semana:'].get()),
                'cervezas_semana': int(self.form_fields['Cervezas por Semana:'].get()),
                'bebidas_fin_semana': int(self.form_fields['Bebidas Fin de Semana:'].get()),
                'bebidas_destiladas_semana': int(self.form_fields['Bebidas Destiladas por Semana:'].get()),
                'vinos_semana': int(self.form_fields['Vinos por Semana:'].get()),
                'perdidas_control': int(self.form_fields['Pérdidas de Control:'].get()),
                'diversion_dependencia': self.form_fields['Diversión Dependencia Alcohol:'].get(),
                'problemas_digestivos': self.form_fields['Problemas Digestivos:'].get(),
                'tension_alta': self.form_fields['Tensión Alta:'].get(),
                'dolor_cabeza': self.form_fields['Dolores de Cabeza:'].get()
            }

            print("Datos a agregar:", data)  # Imprimir los datos para depurar

            agregar_encuesta(**data)
            messagebox.showinfo("Éxito", "Encuesta guardada correctamente")
            self.clear_form()
            self.refresh_view()

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    
    def apply_filter(self):
        sexo = self.filter_sex.get()
        self.refresh_view(sexo)
    
    def export_filtered(self):
        sexo = self.filter_sex.get()
        if sexo:
            engine = create_engine("mysql+mysqlconnector://root:campusfp@localhost/ENCUESTAS")
            query = "SELECT * FROM ENCUESTA WHERE Sexo = %s"
            df = pd.read_sql(query, engine, params=(sexo,))
            
            directory = os.path.join(os.getcwd(), 'Excel Generado')
            if not os.path.exists(directory):
                os.makedirs(directory)
            
            filepath = os.path.join(directory, f'encuestas_exportadas_{sexo}.xlsx')
            df.to_excel(filepath, index=False)
            engine.dispose()
            
            messagebox.showinfo("Éxito", f"Datos exportados a {filepath}")
    
    def update_survey(self):
        try:
            id_encuesta = int(self.update_id.get())
            columna = self.update_field.get()
            nuevo_valor = self.update_value.get()
            
            actualizar_encuesta(id_encuesta, columna, nuevo_valor)
            messagebox.showinfo("Éxito", "Encuesta actualizada correctamente")
            self.refresh_view()
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def delete_survey(self):
        try:
            # Obtener el ID de la encuesta a eliminar
            id_encuesta = int(self.delete_id.get())
            
            # Llamar a la función para eliminar la encuesta
            eliminar_encuesta(id_encuesta)
            
            # Mostrar mensaje de éxito con el ID de la encuesta eliminada
            messagebox.showinfo("Éxito", f"Encuesta con ID {id_encuesta} eliminada correctamente")
            
            # Actualizar la vista
            self.refresh_view()
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    
    def create_graph(self):
        grafico_consumo_edad()
    
    def export_all(self):
        exportar_a_excel()
    
    def clear_form(self):
        for field in self.form_fields.values():
            if isinstance(field, ttk.Entry):
                field.delete(0, 'end')
            else:  # Combobox
                field.set('')
    
    def refresh_view(self, sexo=None):
        # Limpiar tabla actual
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener y mostrar datos
        db = conectar_bd()
        cursor = db.cursor()
        
        if sexo:
            cursor.execute("SELECT * FROM ENCUESTA WHERE Sexo = %s", (sexo,))
        else:
            cursor.execute("SELECT * FROM ENCUESTA")
            
        for row in cursor.fetchall():
            self.tree.insert('', 'end', values=row)
        
        db.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = EncuestasApp(root)
    root.mainloop()