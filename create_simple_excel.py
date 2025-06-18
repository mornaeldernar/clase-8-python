import pandas as pd
import numpy as np

# Crear datos de encuestas de satisfacción
np.random.seed(42)

encuestas = []
for i in range(1, 151):
    cliente_id = f'C{i:03d}'
    empresa = np.random.choice(['Empresa A', 'Empresa B', 'Empresa C', 'Empresa D', 'Empresa E'])
    
    # Generar puntuaciones con algunos valores faltantes
    puntuacion_general = np.random.choice([1, 2, 3, 4, 5]) if np.random.random() > 0.08 else np.nan
    comunicacion = np.random.choice([1, 2, 3, 4, 5]) if np.random.random() > 0.12 else np.nan
    tiempo_respuesta = np.random.choice([1, 2, 3, 4, 5]) if np.random.random() > 0.10 else np.nan
    calidad_servicio = np.random.choice([1, 2, 3, 4, 5]) if np.random.random() > 0.06 else np.nan
    
    # Recomendaría - correlacionado con satisfacción
    if pd.notna(puntuacion_general):
        if puntuacion_general >= 4:
            recomendaria = np.random.choice(['Sí', 'Tal vez', 'No'], p=[0.75, 0.20, 0.05])
        elif puntuacion_general >= 3:
            recomendaria = np.random.choice(['Sí', 'Tal vez', 'No'], p=[0.40, 0.40, 0.20])
        else:
            recomendaria = np.random.choice(['Sí', 'Tal vez', 'No'], p=[0.15, 0.25, 0.60])
    else:
        recomendaria = np.nan
    
    # Algunos campos demográficos faltantes
    tamaño_empresa = np.random.choice(['Pequeña', 'Mediana', 'Grande', 'Enterprise']) if np.random.random() > 0.05 else np.nan
    industria = np.random.choice(['Tech', 'Finance', 'Healthcare', 'Manufacturing', 'Retail']) if np.random.random() > 0.08 else np.nan
    
    # Comentarios - muchos vacíos
    comentarios_list = [
        'Excelente servicio',
        'Buena experiencia',
        'Podría mejorar',
        'Muy profesionales',
        'Regular',
        'Superó expectativas'
    ]
    comentario = np.random.choice(comentarios_list) if np.random.random() > 0.40 else ''
    if comentario == '' and np.random.random() > 0.7:
        comentario = np.nan
    
    encuestas.append({
        'cliente_id': cliente_id,
        'empresa': empresa,
        'puntuacion_general': puntuacion_general,
        'comunicacion': comunicacion,
        'tiempo_respuesta': tiempo_respuesta,
        'calidad_servicio': calidad_servicio,
        'recomendaria': recomendaria,
        'tamaño_empresa': tamaño_empresa,
        'industria': industria,
        'comentarios': comentario,
        'fecha_encuesta': pd.Timestamp('2024-01-01') + pd.Timedelta(days=np.random.randint(0, 365))
    })

df_encuestas = pd.DataFrame(encuestas)

# Guardar en Excel
with pd.ExcelWriter('datos/encuestas_satisfaccion.xlsx', engine='openpyxl') as writer:
    df_encuestas.to_excel(writer, sheet_name='Respuestas', index=False)
    
    # Metadata
    metadata = pd.DataFrame({
        'Campo': ['puntuacion_general', 'comunicacion', 'tiempo_respuesta', 'calidad_servicio'],
        'Escala': ['1-5 (1=Muy Malo, 5=Excelente)'] * 4,
        'Descripción': [
            'Satisfacción general con el servicio',
            'Calidad de la comunicación del equipo',
            'Satisfacción con tiempos de respuesta',
            'Calidad técnica del servicio prestado'
        ]
    })
    metadata.to_excel(writer, sheet_name='Metadata', index=False)

print('Archivo encuestas_satisfaccion.xlsx creado')

# Crear datos de gastos
gastos_data = []
proyectos = ['P001', 'P002', 'P003', 'P004', 'P005', 'P006', 'P007', 'P008', 'P009', 'P010']

for proyecto in proyectos:
    n_entradas = np.random.randint(8, 15)
    
    for i in range(n_entradas):
        fecha_gasto = pd.Timestamp('2024-01-01') + pd.Timedelta(days=np.random.randint(0, 300))
        categoria = np.random.choice(['Personal', 'Viajes', 'Materiales', 'Software', 'Consultores'])
        
        # Montos según categoría
        if categoria == 'Personal':
            monto = np.random.normal(8000, 2000)
            concepto = np.random.choice(['Salarios', 'Bonificaciones', 'Formación'])
        elif categoria == 'Viajes':
            monto = np.random.normal(1500, 500)
            concepto = np.random.choice(['Vuelos', 'Hoteles', 'Comidas'])
        elif categoria == 'Materiales':
            monto = np.random.normal(3000, 1000)
            concepto = np.random.choice(['Equipos', 'Suministros'])
        elif categoria == 'Software':
            monto = np.random.normal(2500, 800)
            concepto = np.random.choice(['Licencias', 'Herramientas'])
        else:
            monto = np.random.normal(12000, 4000)
            concepto = np.random.choice(['Externos', 'Especialistas'])
        
        monto = max(100, round(monto, 2))
        
        # Algunos sin aprobar
        fecha_aprobacion = fecha_gasto + pd.Timedelta(days=np.random.randint(1, 10)) if np.random.random() > 0.15 else np.nan
        aprobado_por = np.random.choice(['Manager A', 'Manager B', 'Manager C']) if pd.notna(fecha_aprobacion) else ''
        
        gastos_data.append({
            'proyecto_id': proyecto,
            'fecha_gasto': fecha_gasto,
            'categoria': categoria,
            'concepto': concepto,
            'monto': monto,
            'moneda': 'EUR',
            'fecha_aprobacion': fecha_aprobacion,
            'aprobado_por': aprobado_por,
            'notas': np.random.choice(['', 'Urgente', 'OK', np.nan], p=[0.60, 0.15, 0.20, 0.05])
        })

df_gastos = pd.DataFrame(gastos_data)

# Guardar gastos
with pd.ExcelWriter('datos/tiempos_gastos.xlsx', engine='openpyxl') as writer:
    df_gastos.to_excel(writer, sheet_name='Gastos_Detallados', index=False)
    
    # Resumen por proyecto
    resumen = df_gastos.groupby('proyecto_id').agg({
        'monto': 'sum',
        'fecha_gasto': 'count',
        'fecha_aprobacion': lambda x: x.notna().sum()
    }).round(2)
    resumen.columns = ['Total_Gastado', 'Num_Transacciones', 'Transacciones_Aprobadas']
    resumen.to_excel(writer, sheet_name='Resumen_Proyectos')

print('Archivo tiempos_gastos.xlsx creado')