import pandas as pd
import numpy as np

# Dataset de empleados para consultoría
empleados = pd.DataFrame({
    'empleado_id': ['E001', 'E002', 'E003', 'E004', 'E005', 'E006', 'E007', 'E008'],
    'nombre': ['Ana García', 'Carlos López', 'María Rodriguez', 'Juan Pérez', 
               'Laura Martín', 'Pedro Sánchez', 'Sofia Hernández', 'Diego Torres'],
    'departamento': ['Consultoría', 'IT', 'Consultoría', 'Finanzas', 'IT', 'Consultoría', 'Finanzas', 'IT'],
    'salario': [65000, 70000, 62000, 75000, 68000, 67000, 72000, 69000],
    'antiguedad': [3, 5, 2, 7, 4, 6, 3, 1],
    'evaluacion': [8.5, 9.2, 7.8, 9.0, 8.8, 8.2, 9.1, 7.5],
    'ciudad': ['Madrid', 'Barcelona', 'Madrid', 'Valencia', 'Barcelona', 'Madrid', 'Valencia', 'Barcelona']
})

# Configurar índice personalizado
empleados.set_index('empleado_id', inplace=True)
print(empleados.head())

# TODO: Usando loc, selecciona:
# 1. Empleados E002, E004, E006
# 2. Solo las columnas: nombre, departamento, salario
# Tu solución aquí:
filtro_de_empleados = empleados.loc[['E002','E004','E006'],
                                    ['nombre','departamento','salario']]

print("Empleados filtrados")
print(filtro_de_empleados)

# TODO: Encuentra empleados que:
# 1. Trabajen en Madrid O Barcelona
# 2. Tengan evaluación >= 8.0
# 3. Muestren solo: nombre, ciudad, evaluacion, salario
# Tu solución aquí:

empleados.loc[
    (empleados['ciudad'].isnin(['Madrid','Barcelona'])) &
    (empleados['evaluacion'] >= 8.0)
    ,["nombre","ciudad","evaluacion","salario"]
]

# TODO: Usando iloc:
# 1. Selecciona los últimos 3 empleados
# 2. Solo las primeras 4 columnas
# Tu solución aquí:

ultimos_empleados = empleados.iloc[-3:,:4]
print("ultimos 3 empleados")
print(ultimos_empleados)