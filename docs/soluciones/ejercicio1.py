import pandas as pd
import numpy as np

# Datos de ejemplo: proyectos de consultoría
proyectos = pd.DataFrame({
    'proyecto_id': ['P001', 'P002', 'P003', 'P004', 'P005', 'P006'],
    'cliente': ['Empresa A', 'Empresa B', 'Empresa A', 'Empresa C', 'Empresa B', 'Empresa D'],
    'presupuesto': [50000, 75000, 30000, 120000, 45000, 90000],
    'duracion_dias': [30, 45, 20, 60, 25, 50],
    'estado': ['Completado', 'En Progreso', 'Completado', 'Retrasado', 'En Progreso', 'Completado'],
    'region': ['Norte', 'Sur', 'Norte', 'Centro', 'Sur', 'Norte']
})

#print(proyectos)

filtro_presupuesto = proyectos['presupuesto'] > 60000
filtro_estado = proyectos['estado'].isin(['En Progreso','Retrasado'])
filtro_presupuesto_Y_estado = filtro_presupuesto & filtro_estado


print("Proyectos filtrados con presupuesto mayor a 60,000 y en estado 'En Progreso' o 'Retrasado'")
print(proyectos[filtro_presupuesto_Y_estado])

# ejercicio 3: filtrado con negación
filtro_no_completados = proyectos['estado'] == 'Completado'
filtro_no_sur = proyectos['region'] == 'Sur'
filtro_combinado_negacion = ~filtro_no_completados & ~filtro_no_sur
print("Proyectos que no están Completados y no son de la región Sur:")
print(proyectos[filtro_combinado_negacion])