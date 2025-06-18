# Función apply() - Transformaciones Personalizadas

## Introducción

La función `apply()` es una de las herramientas más poderosas y flexibles de Pandas. Permite aplicar funciones personalizadas a filas, columnas o elementos individuales, lo que la convierte en esencial para transformaciones complejas que no se pueden lograr con operaciones vectorizadas básicas.

## 🎯 Objetivos de esta Sección

- Dominar el uso de `apply()` en diferentes contextos
- Crear funciones personalizadas para transformaciones específicas
- Optimizar el rendimiento de transformaciones complejas
- Aplicar `apply()` a casos prácticos de consultoría
- Entender cuándo usar `apply()` vs. alternativas más eficientes

## Conceptos Fundamentales

### ¿Qué es apply()?

`apply()` permite ejecutar una función a lo largo de un eje del DataFrame o Serie:
- **axis=0 o axis='index'**: Aplica función a cada columna
- **axis=1 o axis='columns'**: Aplica función a cada fila

```python
import pandas as pd
import numpy as np

# Dataset de ejemplo: análisis de proyectos
proyectos = pd.DataFrame({
    'proyecto_id': ['P001', 'P002', 'P003', 'P004', 'P005'],
    'presupuesto': [100000, 150000, 80000, 200000, 120000],
    'gastado': [85000, 160000, 75000, 180000, 130000],
    'horas_planificadas': [500, 750, 400, 1000, 600],
    'horas_reales': [520, 800, 380, 1100, 650],
    'equipo_size': [5, 8, 4, 10, 6],
    'cliente_tipo': ['Grande', 'Enterprise', 'Pequeño', 'Enterprise', 'Mediano']
})

print("Dataset de proyectos:")
print(proyectos)
```

## Apply() con Funciones Simples

### Aplicar Funciones Built-in

```python
# Aplicar función a una columna
proyectos['presupuesto_log'] = proyectos['presupuesto'].apply(np.log)

# Aplicar función matemática
proyectos['eficiencia_horas'] = proyectos['horas_planificadas'].apply(lambda x: x / 8)  # días

print("Aplicación de funciones simples:")
print(proyectos[['proyecto_id', 'presupuesto', 'presupuesto_log', 'eficiencia_horas']])
```

### Funciones Lambda

```python
# Clasificar proyectos por tamaño de presupuesto
proyectos['categoria_presupuesto'] = proyectos['presupuesto'].apply(
    lambda x: 'Alto' if x > 150000 else 'Medio' if x > 100000 else 'Bajo'
)

# Calcular variación porcentual
proyectos['variacion_horas_pct'] = proyectos.apply(
    lambda row: ((row['horas_reales'] - row['horas_planificadas']) / row['horas_planificadas']) * 100,
    axis=1
)

print("Aplicación de funciones lambda:")
print(proyectos[['proyecto_id', 'categoria_presupuesto', 'variacion_horas_pct']])
```

## Apply() con Funciones Personalizadas

### Funciones para Análisis de Una Columna

```python
def evaluar_desempeño_presupuesto(gastado, presupuesto):
    """Evalúa el desempeño del manejo de presupuesto."""
    variacion = ((gastado - presupuesto) / presupuesto) * 100
    
    if variacion <= -10:
        return 'Excelente'
    elif variacion <= 0:
        return 'Bueno'
    elif variacion <= 10:
        return 'Aceptable'
    else:
        return 'Problemático'

# Aplicar usando lambda para pasar múltiples columnas
proyectos['desempeño_presupuesto'] = proyectos.apply(
    lambda row: evaluar_desempeño_presupuesto(row['gastado'], row['presupuesto']),
    axis=1
)

print("Evaluación de desempeño de presupuesto:")
print(proyectos[['proyecto_id', 'presupuesto', 'gastado', 'desempeño_presupuesto']])
```

### Funciones para Análisis Complejo de Filas

```python
def calcular_metricas_proyecto(row):
    """Calcula métricas comprehensivas para un proyecto."""
    # Eficiencia de presupuesto
    eficiencia_presupuesto = (row['presupuesto'] - row['gastado']) / row['presupuesto']
    
    # Productividad del equipo (presupuesto por persona por hora)
    productividad = row['presupuesto'] / (row['equipo_size'] * row['horas_planificadas'])
    
    # Score de riesgo basado en múltiples factores
    riesgo_presupuesto = 1 if row['gastado'] > row['presupuesto'] else 0
    riesgo_tiempo = 1 if row['horas_reales'] > row['horas_planificadas'] * 1.1 else 0
    riesgo_tamaño = 1 if row['equipo_size'] > 8 else 0
    
    score_riesgo = riesgo_presupuesto + riesgo_tiempo + riesgo_tamaño
    
    return pd.Series({
        'eficiencia_presupuesto': eficiencia_presupuesto,
        'productividad': productividad,
        'score_riesgo': score_riesgo
    })

# Aplicar función que retorna Serie (crea múltiples columnas)
metricas = proyectos.apply(calcular_metricas_proyecto, axis=1)
proyectos_extendido = pd.concat([proyectos, metricas], axis=1)

print("Métricas calculadas con apply:")
print(proyectos_extendido[['proyecto_id', 'eficiencia_presupuesto', 'productividad', 'score_riesgo']])
```

## Apply() Avanzado

### Aplicación a Grupos con GroupBy

```python
def estadisticas_grupo(grupo):
    """Calcula estadísticas personalizadas para un grupo."""
    return pd.Series({
        'proyectos_count': len(grupo),
        'presupuesto_promedio': grupo['presupuesto'].mean(),
        'eficiencia_promedio': grupo['eficiencia_presupuesto'].mean(),
        'proyectos_riesgo': (grupo['score_riesgo'] > 1).sum(),
        'productividad_max': grupo['productividad'].max()
    })

# Aplicar por tipo de cliente
estadisticas_cliente = proyectos_extendido.groupby('cliente_tipo').apply(estadisticas_grupo)

print("Estadísticas por tipo de cliente:")
print(estadisticas_cliente)
```

### Apply() con Funciones que Acceden a Todo el DataFrame

```python
def calcular_ranking_relativo(row, df_completo):
    """Calcula ranking relativo del proyecto dentro del dataset."""
    # Ranking de presupuesto
    ranking_presupuesto = (df_completo['presupuesto'] <= row['presupuesto']).sum()
    total_proyectos = len(df_completo)
    percentil_presupuesto = (ranking_presupuesto / total_proyectos) * 100
    
    return percentil_presupuesto

# Aplicar función que necesita acceso al DataFrame completo
proyectos_extendido['percentil_presupuesto'] = proyectos_extendido.apply(
    lambda row: calcular_ranking_relativo(row, proyectos_extendido),
    axis=1
)

print("Ranking relativo de proyectos:")
print(proyectos_extendido[['proyecto_id', 'presupuesto', 'percentil_presupuesto']])
```

## Casos Prácticos en Consultoría

### Caso 1: Sistema de Scoring de Clientes

```python
# Dataset de clientes para scoring
clientes = pd.DataFrame({
    'cliente_id': ['C001', 'C002', 'C003', 'C004', 'C005'],
    'ingresos_anuales': [5000000, 2000000, 10000000, 1500000, 7500000],
    'empleados': [50, 25, 150, 20, 100],
    'proyectos_anteriores': [3, 1, 8, 0, 5],
    'satisfaccion_promedio': [8.5, 7.2, 9.1, 0, 8.8],  # 0 = sin datos
    'industria': ['Tech', 'Retail', 'Finance', 'Startup', 'Manufacturing'],
    'region': ['Norte', 'Sur', 'Centro', 'Norte', 'Sur'],
    'tiempo_pago_dias': [30, 45, 25, 60, 35]
})

def calcular_score_cliente(row):
    """Calcula score comprehensivo del cliente para priorización."""
    score = 0
    
    # Score por tamaño (ingresos anuales)
    if row['ingresos_anuales'] >= 5000000:
        score += 25
    elif row['ingresos_anuales'] >= 2000000:
        score += 15
    else:
        score += 5
    
    # Score por número de empleados
    if row['empleados'] >= 100:
        score += 20
    elif row['empleados'] >= 50:
        score += 15
    elif row['empleados'] >= 25:
        score += 10
    else:
        score += 5
    
    # Score por historial
    score += min(row['proyectos_anteriores'] * 5, 25)  # Max 25 puntos
    
    # Score por satisfacción
    if row['satisfaccion_promedio'] > 0:  # Tiene datos
        if row['satisfaccion_promedio'] >= 9:
            score += 20
        elif row['satisfaccion_promedio'] >= 8:
            score += 15
        elif row['satisfaccion_promedio'] >= 7:
            score += 10
        else:
            score += 5
    else:
        score += 7  # Score neutral para nuevos clientes
    
    # Penalización por pago lento
    if row['tiempo_pago_dias'] > 45:
        score -= 10
    elif row['tiempo_pago_dias'] > 35:
        score -= 5
    
    return min(score, 100)  # Máximo 100

clientes['cliente_score'] = clientes.apply(calcular_score_cliente, axis=1)

def clasificar_cliente(score):
    """Clasifica cliente basado en score."""
    if score >= 80:
        return 'Premium'
    elif score >= 60:
        return 'Alto Valor'
    elif score >= 40:
        return 'Estándar'
    else:
        return 'Básico'

clientes['clasificacion'] = clientes['cliente_score'].apply(clasificar_cliente)

print("Sistema de scoring de clientes:")
print(clientes[['cliente_id', 'cliente_score', 'clasificacion']])
```

### Caso 2: Análisis de Riesgo de Proyectos

```python
def analizar_riesgo_proyecto(row):
    """Análisis comprehensivo de riesgo de proyecto."""
    factores_riesgo = []
    puntuacion_riesgo = 0
    
    # Riesgo por presupuesto
    if row['presupuesto'] > 150000:
        factores_riesgo.append('Presupuesto Alto')
        puntuacion_riesgo += 2
    
    # Riesgo por tamaño de equipo
    if row['equipo_size'] > 8:
        factores_riesgo.append('Equipo Grande')
        puntuacion_riesgo += 1
    elif row['equipo_size'] < 4:
        factores_riesgo.append('Equipo Pequeño')
        puntuacion_riesgo += 1
    
    # Riesgo por cliente
    if row['cliente_tipo'] == 'Enterprise':
        factores_riesgo.append('Cliente Enterprise')
        puntuacion_riesgo += 1
    
    # Riesgo por sobrecosto actual
    if row['gastado'] > row['presupuesto']:
        factores_riesgo.append('Sobrecosto')
        puntuacion_riesgo += 3
    
    # Riesgo por desviación temporal
    if row['horas_reales'] > row['horas_planificadas'] * 1.2:
        factores_riesgo.append('Desviación Temporal')
        puntuacion_riesgo += 2
    
    # Determinar nivel de riesgo
    if puntuacion_riesgo >= 6:
        nivel_riesgo = 'Alto'
    elif puntuacion_riesgo >= 3:
        nivel_riesgo = 'Medio'
    else:
        nivel_riesgo = 'Bajo'
    
    return pd.Series({
        'factores_riesgo': ', '.join(factores_riesgo) if factores_riesgo else 'Ninguno',
        'puntuacion_riesgo': puntuacion_riesgo,
        'nivel_riesgo': nivel_riesgo
    })

# Aplicar análisis de riesgo
analisis_riesgo = proyectos_extendido.apply(analizar_riesgo_proyecto, axis=1)
proyectos_con_riesgo = pd.concat([proyectos_extendido, analisis_riesgo], axis=1)

print("Análisis de riesgo de proyectos:")
print(proyectos_con_riesgo[['proyecto_id', 'factores_riesgo', 'puntuacion_riesgo', 'nivel_riesgo']])
```

### Caso 3: Recomendaciones Automáticas

```python
def generar_recomendaciones(row):
    """Genera recomendaciones automáticas basadas en métricas del proyecto."""
    recomendaciones = []
    
    # Recomendaciones por eficiencia de presupuesto
    if row['eficiencia_presupuesto'] < 0:
        if abs(row['eficiencia_presupuesto']) > 0.1:
            recomendaciones.append("URGENTE: Revisar control de gastos")
        else:
            recomendaciones.append("Monitorear gastos de cerca")
    elif row['eficiencia_presupuesto'] > 0.2:
        recomendaciones.append("Considerar reasignar presupuesto excedente")
    
    # Recomendaciones por productividad
    if row['productividad'] < 15:  # Umbral bajo
        recomendaciones.append("Evaluar eficiencia del equipo")
    elif row['productividad'] > 50:  # Umbral alto
        recomendaciones.append("Equipo altamente eficiente - replicar prácticas")
    
    # Recomendaciones por riesgo
    if row['nivel_riesgo'] == 'Alto':
        recomendaciones.append("Implementar plan de mitigación inmediato")
    elif row['nivel_riesgo'] == 'Medio':
        recomendaciones.append("Aumentar frecuencia de revisiones")
    
    # Recomendaciones por desviación temporal
    variacion_horas = (row['horas_reales'] - row['horas_planificadas']) / row['horas_planificadas']
    if variacion_horas > 0.15:
        recomendaciones.append("Revisar planificación de tiempo")
    elif variacion_horas < -0.15:
        recomendaciones.append("Proyecto adelantado - considerar adelantar entregables")
    
    return '; '.join(recomendaciones) if recomendaciones else 'Sin recomendaciones especiales'

proyectos_con_riesgo['recomendaciones'] = proyectos_con_riesgo.apply(generar_recomendaciones, axis=1)

print("Recomendaciones automáticas:")
for idx, row in proyectos_con_riesgo.iterrows():
    print(f"\n{row['proyecto_id']}: {row['recomendaciones']}")
```

## Optimización y Alternativas

### Cuándo NO usar apply()

```python
# ❌ Evitar apply() para operaciones simples que se pueden vectorizar
# Lento
proyectos['presupuesto_doble_lento'] = proyectos['presupuesto'].apply(lambda x: x * 2)

# ✅ Mejor - operación vectorizada
proyectos['presupuesto_doble_rapido'] = proyectos['presupuesto'] * 2

# ❌ Evitar apply() para operaciones que Pandas ya tiene optimizadas
# Lento
proyectos['presupuesto_sqrt_lento'] = proyectos['presupuesto'].apply(np.sqrt)

# ✅ Mejor - usar método directo
proyectos['presupuesto_sqrt_rapido'] = np.sqrt(proyectos['presupuesto'])
```

### Alternativas Más Eficientes

```python
# Para condiciones simples, usar np.where es más rápido
# Lento con apply
proyectos['categoria_lenta'] = proyectos['presupuesto'].apply(
    lambda x: 'Alto' if x > 150000 else 'Bajo'
)

# Rápido con np.where
proyectos['categoria_rapida'] = np.where(
    proyectos['presupuesto'] > 150000, 'Alto', 'Bajo'
)

# Para transformaciones por grupo, usar transform
# Menos eficiente
proyectos['presupuesto_promedio_grupo_lento'] = proyectos.groupby('cliente_tipo').apply(
    lambda x: x['presupuesto'].mean()
)

# Más eficiente
proyectos['presupuesto_promedio_grupo_rapido'] = proyectos.groupby('cliente_tipo')['presupuesto'].transform('mean')
```

## Ejercicios Prácticos

### Ejercicio 1: Función de Evaluación Personalizada
```python
# TODO: Crea una función que evalúe la "salud" general del proyecto
# Considerando: eficiencia de presupuesto, desviación temporal, y tamaño del equipo
# Debe retornar un score de 0-100 y una clasificación (Excelente, Bueno, Regular, Problemático)

def evaluar_salud_proyecto(row):
    # Tu implementación aquí
    pass

# proyectos['salud_score'], proyectos['salud_clasificacion'] = zip(*proyectos.apply(evaluar_salud_proyecto, axis=1))
```

### Ejercicio 2: Sistema de Alertas
```python
# TODO: Crea una función que genere alertas automáticas
# Debe identificar: sobrecostos, retrasos significativos, equipos sobrecargados
# Retorna lista de alertas para cada proyecto

def generar_alertas_proyecto(row):
    # Tu implementación aquí
    pass

# proyectos['alertas'] = proyectos.apply(generar_alertas_proyecto, axis=1)
```

### Ejercicio 3: Análisis Comparativo
```python
# TODO: Crea una función que compare cada proyecto con el promedio del grupo
# Debe considerar su tipo de cliente y generar insights comparativos

def analizar_comparativo(row, df_completo):
    # Tu implementación aquí
    pass

# proyectos['analisis_comparativo'] = proyectos.apply(lambda row: analizar_comparativo(row, proyectos), axis=1)
```

## Mejores Prácticas

!!! tip "Consejos para Usar apply() Eficientemente"
    1. **Usa apply() solo cuando sea necesario**: Para lógica compleja que no se puede vectorizar
    2. **Considera el rendimiento**: apply() es más lento que operaciones vectorizadas
    3. **Funciones puras**: Evita efectos secundarios en las funciones aplicadas
    4. **Documentación clara**: Explica qué hace cada función personalizada
    5. **Testing**: Prueba funciones con casos edge antes de aplicar masivamente

### Plantilla para Funciones apply()

```python
def funcion_template(row):
    """
    Descripción clara de qué hace la función.
    
    Args:
        row: Fila del DataFrame con las columnas: col1, col2, col3
        
    Returns:
        resultado: Descripción del resultado
        
    Example:
        >>> resultado = df.apply(funcion_template, axis=1)
    """
    try:
        # Validaciones de entrada
        if pd.isna(row['columna_importante']):
            return valor_por_defecto
        
        # Lógica principal
        resultado = calcular_algo(row)
        
        # Validaciones de salida
        if not isinstance(resultado, tipo_esperado):
            return valor_por_defecto
            
        return resultado
        
    except Exception as e:
        print(f"Error procesando fila {row.name}: {e}")
        return valor_por_defecto
```

## Resumen

La función `apply()` te permite:

- ✅ Implementar lógica compleja personalizada
- ✅ Crear métricas y scores sofisticados
- ✅ Generar insights automáticos
- ✅ Procesar datos de manera flexible
- ✅ Integrar múltiples condiciones y cálculos

**Próximo paso**: Continúa con [Detección de Valores Faltantes](../limpieza/deteccion-valores-faltantes.md) para aprender a identificar y manejar datos incompletos.