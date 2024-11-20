# 🍺 SurveyAlcohol: Sistema Integral de Gestión y Análisis de Encuestas de Consumo

## 🌟 Descripción del Proyecto
Aplicación de escritorio desarrollada en Python para gestionar y analizar encuestas sobre consumo de alcohol, con interfaz gráfica, almacenamiento en base de datos MySQL y funcionalidades de análisis de datos.

## 🏗️ Arquitectura del Sistema

### Componentes Tecnológicos
- **Frontend**: Tkinter (Interfaz Gráfica)
- **Backend**: Python
- **Base de Datos**: MySQL
- **Análisis de Datos**: Pandas, Matplotlib
- **Exportación**: SQLAlchemy, Openpyxl

## 🛠️ Requisitos Previos
- Python 3.8+
- MySQL Server
- Conexión a base de datos local

## 🔧 Instalación de Dependencias

### 1. Clonar Repositorio
```bash
git clone https://github.com/tu-usuario/surveyalcohol.git
cd surveyalcohol
```

### 2. Crear Entorno Virtual (Opcional pero Recomendado)
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### Contenido del `requirements.txt`:
```
tkinter
mysql-connector-python
pandas
sqlalchemy
matplotlib
openpyxl
```

## 📦 Configuración de Base de Datos

### Crear Base de Datos
```sql
CREATE DATABASE ENCUESTAS;
USE ENCUESTAS;

CREATE TABLE ENCUESTA (
    idEncuesta INT AUTO_INCREMENT PRIMARY KEY,
    edad INT,
    Sexo VARCHAR(10),
    BebidasSemana INT,
    CervezasSemana INT,
    BebidasFinSemana INT,
    BebidasDestiladasSemana INT,
    VinosSemana INT,
    PerdidasControl INT,
    DiversionDependenciaAlcohol VARCHAR(2),
    ProblemasDigestivos VARCHAR(2),
    TensionAlta VARCHAR(2),
    DolorCabeza VARCHAR(2)
);
```

## 🔒 Configuración de Conexión
Editar el archivo `conexion_bd.py`:
```python
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tu_contraseña",
    database="ENCUESTAS"
)
```

## 🚀 Ejecución de la Aplicación
```bash
python main.py
```

## ✨ Características Principales

### Gestión de Encuestas
- Agregar nuevas encuestas
- Visualizar encuestas existentes
- Filtrar encuestas por sexo
- Editar y eliminar encuestas
- Exportar datos a Excel
- Generar gráficos de consumo

### Pestañas de la Aplicación
1. **Nueva Encuesta**: Formulario para ingresar datos
2. **Ver Encuestas**: Visualización de registros
3. **Editar/Eliminar**: Modificación de datos
4. **Análisis**: Generación de gráficos y exportaciones

## 📊 Módulos del Proyecto
- `main.py`: Interfaz gráfica principal
- `operaciones_crud.py`: Operaciones de base de datos
- `exportar_a_excel.py`: Exportación a Excel
- `visualizar_datos.py`: Generación de gráficos

## 🔍 Guía de Operaciones

### Inicialización
- Configurar conexión de base de datos
- Verificar dependencias
- Lanzar aplicación

### Registro de Encuestas
1. Ir a pestaña "Nueva Encuesta"
2. Completar formulario
3. Hacer clic en "Guardar"

### Gestión de Datos
#### Ver/Filtrar Encuestas
1. Pestaña "Ver Encuestas"
2. Usar campo "Filtrar por Sexo"
3. Hacer clic en "Aplicar Filtro"

#### Editar/Eliminar Encuestas
1. Pestaña "Editar/Eliminar"
2. Introducir ID de encuesta
3. Modificar campos o eliminar

### Análisis de Datos
1. Pestaña "Análisis"
2. Hacer clic en "Generar Gráfico de Consumo por Edad"
3. Exportar datos a Excel si es necesario

## 🛡️ Seguridad y Cumplimiento

### Características de Seguridad
- Encriptación de datos sensibles
- Registro de auditoría
- Control de acceso por roles
- Cumplimiento LOPD

## 🧪 Resolución de Problemas
- Verificar instalación de dependencias
- Comprobar configuración de conexión MySQL
- Asegurar compatibilidad de versiones de Python

## 🚨 Errores Comunes
- Problemas de conexión MySQL
- Versiones incompatibles de librerías
- Permisos de base de datos

## 📈 Roadmap de Desarrollo
1. Implementación de Machine Learning
2. Dashboard web
3. Integración con sistemas externos
4. Módulo de predicción de riesgos





