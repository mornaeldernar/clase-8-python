import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Crear datos de encuestas de satisfacción
np.random.seed(42)

# Generar respuestas de encuesta con valores faltantes realistas
encuestas = []
for i in range(1, 151):
    cliente_id = f'C{i:03d}'
    empresa = np.random.choice(['Empresa A', 'Empresa B', 'Empresa C', 'Empresa D', 'Empresa E'])
    
    # Introducir faltantes de manera realista
    p_general = np.random.choice([1, 2, 3, 4, 5, np.nan], p=[0.05, 0.10, 0.20, 0.35, 0.25, 0.05])
    
    # Algunas personas no responden ciertas preguntas
    skip_prob = 0.12 if pd.notna(p_general) and p_general <= 3 else 0.05  # Los insatisfechos tienden a saltar más preguntas
    
    # Ajustar probabilidades para que sumen 1
    base_probs_com = np.array([0.08, 0.12, 0.25, 0.35, 0.15])
    base_probs_com = base_probs_com * (1 - skip_prob)
    probs_com = np.append(base_probs_com, skip_prob)
    
    base_probs_tiempo = np.array([0.15, 0.20, 0.25, 0.25, 0.10])
    base_probs_tiempo = base_probs_tiempo * (1 - skip_prob)
    probs_tiempo = np.append(base_probs_tiempo, skip_prob)
    
    base_probs_calidad = np.array([0.05, 0.10, 0.20, 0.40, 0.20])
    base_probs_calidad = base_probs_calidad * (1 - skip_prob)
    probs_calidad = np.append(base_probs_calidad, skip_prob)
    
    comunicacion = np.random.choice([1, 2, 3, 4, 5, np.nan], p=probs_com)
    tiempo_respuesta = np.random.choice([1, 2, 3, 4, 5, np.nan], p=probs_tiempo)
    calidad_servicio = np.random.choice([1, 2, 3, 4, 5, np.nan], p=probs_calidad)
    
    # Preguntas demográficas - algunos prefieren no responder
    tamaño_empresa = np.random.choice(['Pequeña', 'Mediana', 'Grande', 'Enterprise', ''], p=[0.30, 0.30, 0.25, 0.12, 0.03])
    industria = np.random.choice(['Tech', 'Finance', 'Healthcare', 'Manufacturing', 'Retail', ''], p=[0.20, 0.18, 0.15, 0.20, 0.22, 0.05])
    
    # Comentarios - muchos los dejan vacíos
    comentarios_opciones = [
        'Excelente servicio, muy satisfecho',
        'Buena experiencia en general',
        'El tiempo de respuesta podría mejorar',
        'Muy profesionales y efectivos',
        'Regular, esperaba más',
        'Superó mis expectativas',
        'Buen trabajo pero caro',
        'Rápidos y eficientes',
        '',  # Vacío
        np.nan  # NaN
    ]
    comentario = np.random.choice(comentarios_opciones, p=[0.15, 0.15, 0.10, 0.12, 0.08, 0.10, 0.05, 0.08, 0.12, 0.05])
    
    # Recomendaría - correlacionado con satisfacción general
    if pd.isna(p_general):
        recomendaria = np.nan
    elif p_general >= 4:
        recomendaria = np.random.choice(['Sí', 'Tal vez', 'No', ''], p=[0.75, 0.15, 0.05, 0.05])
    elif p_general >= 3:
        recomendaria = np.random.choice(['Sí', 'Tal vez', 'No', ''], p=[0.40, 0.35, 0.20, 0.05])
    else:
        recomendaria = np.random.choice(['Sí', 'Tal vez', 'No', ''], p=[0.10, 0.25, 0.60, 0.05])
    
    encuestas.append({
        'cliente_id': cliente_id,
        'empresa': empresa,
        'puntuacion_general': p_general,
        'comunicacion': comunicacion,
        'tiempo_respuesta': tiempo_respuesta,
        'calidad_servicio': calidad_servicio,
        'recomendaria': recomendaria,
        'tamaño_empresa': tamaño_empresa if tamaño_empresa != '' else np.nan,
        'industria': industria if industria != '' else np.nan,
        'comentarios': comentario,
        'fecha_encuesta': pd.Timestamp('2024-01-01') + pd.Timedelta(days=np.random.randint(0, 365))
    })

df_encuestas = pd.DataFrame(encuestas)

# Guardar en Excel con formato
with pd.ExcelWriter('datos/encuestas_satisfaccion.xlsx', engine='openpyxl') as writer:
    df_encuestas.to_excel(writer, sheet_name='Respuestas', index=False)
    
    # Crear hoja de metadatos
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

print('Archivo encuestas_satisfaccion.xlsx creado exitosamente')

# Crear datos de tiempos y gastos
gastos_data = []
proyectos = ['P001', 'P002', 'P003', 'P004', 'P005', 'P006', 'P007', 'P008', 'P009', 'P010']

for proyecto in proyectos:
    # Cada proyecto tiene múltiples entradas de gastos
    n_entradas = np.random.randint(8, 15)
    
    for i in range(n_entradas):
        fecha_gasto = pd.Timestamp('2024-01-01') + pd.Timedelta(days=np.random.randint(0, 300))
        
        # Diferentes tipos de gastos
        categoria = np.random.choice(['Personal', 'Viajes', 'Materiales', 'Software', 'Consultores'])
        
        if categoria == 'Personal':
            concepto = np.random.choice(['Salarios', 'Bonificaciones', 'Formación'])
            monto = np.random.normal(8000, 2000)
        elif categoria == 'Viajes':
            concepto = np.random.choice(['Vuelos', 'Hoteles', 'Comidas', 'Transporte'])
            monto = np.random.normal(1500, 500)
        elif categoria == 'Materiales':
            concepto = np.random.choice(['Equipos', 'Suministros', 'Hardware'])
            monto = np.random.normal(3000, 1000)
        elif categoria == 'Software':
            concepto = np.random.choice(['Licencias', 'Herramientas', 'Plataformas'])
            monto = np.random.normal(2500, 800)
        else:  # Consultores
            concepto = np.random.choice(['Externos', 'Especialistas', 'Subcontratistas'])
            monto = np.random.normal(12000, 4000)
        
        monto = max(100, monto)  # Mínimo 100
        
        # Algunos gastos sin aprobar (sin fecha de aprobación)
        fecha_aprobacion = fecha_gasto + pd.Timedelta(days=np.random.randint(1, 10)) if np.random.random() > 0.15 else np.nan
        
        gastos_data.append({
            'proyecto_id': proyecto,
            'fecha_gasto': fecha_gasto,
            'categoria': categoria,
            'concepto': concepto,
            'monto': round(monto, 2),
            'moneda': 'EUR',
            'fecha_aprobacion': fecha_aprobacion,
            'aprobado_por': np.random.choice(['Manager A', 'Manager B', 'Manager C', '']) if pd.notna(fecha_aprobacion) else '',
            'notas': np.random.choice(['', 'Urgente', 'Revisar', 'OK', np.nan], p=[0.60, 0.10, 0.05, 0.20, 0.05])
        })

df_gastos = pd.DataFrame(gastos_data)

# Guardar gastos en Excel con múltiples hojas
with pd.ExcelWriter('datos/tiempos_gastos.xlsx', engine='openpyxl') as writer:
    # Hoja principal con todos los gastos
    df_gastos.to_excel(writer, sheet_name='Gastos_Detallados', index=False)
    
    # Hoja resumen por proyecto
    resumen = df_gastos.groupby('proyecto_id').agg({
        'monto': 'sum',
        'fecha_gasto': 'count',
        'fecha_aprobacion': lambda x: x.notna().sum()
    }).round(2)
    resumen.columns = ['Total_Gastado', 'Num_Transacciones', 'Transacciones_Aprobadas']
    resumen.to_excel(writer, sheet_name='Resumen_Proyectos')
    
    # Hoja resumen por categoría
    resumen_cat = df_gastos.groupby('categoria').agg({
        'monto': 'sum',
        'fecha_gasto': 'count'
    }).round(2)
    resumen_cat.columns = ['Total_Categoria', 'Num_Gastos']
    resumen_cat.to_excel(writer, sheet_name='Resumen_Categorias')

print('Archivo tiempos_gastos.xlsx creado exitosamente')