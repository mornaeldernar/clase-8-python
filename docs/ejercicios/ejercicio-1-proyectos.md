# Ejercicio 1: Análisis Avanzado de Proyectos

## Objetivo
Aplicar técnicas de filtrado avanzado, creación de columnas y manejo de valores faltantes en un dataset real de proyectos de consultoría.

## Dataset
Utilizar el archivo `datos/proyectos_completo.csv`

## Parte A: Filtrado y Selección Avanzada (30 minutos)

### Ejercicio A1: Filtros Complejos
```python
import pandas as pd
import numpy as np

# Cargar datos
proyectos = pd.read_csv('datos/proyectos_completo.csv')

# TODO: Realizar los siguientes filtros:
# 1. Proyectos que están "En Progreso" Y tienen presupuesto > 150,000
# 2. Proyectos de las regiones Norte o Sur CON satisfacción >= 8.0
# 3. Proyectos que NO están "Completado" Y tienen más de 6 personas en el equipo

# Tu código aquí:
```

### Ejercicio A2: Uso de isin() y query()
```python
# TODO: 
# 1. Usar isin() para encontrar proyectos de tipos específicos
# 2. Usar query() para replicar uno de los filtros anteriores
# 3. Comparar el rendimiento de ambos métodos

# Tu código aquí:
```

### Ejercicio A3: Selección con loc
```python
# TODO: 
# 1. Seleccionar proyectos P001, P005, P010 con columnas específicas
# 2. Usar loc para filtrar y seleccionar simultáneamente
# 3. Crear un subconjunto para análisis de proyectos de alto presupuesto

# Tu código aquí:
```

## Parte B: Transformación de Datos (30 minutos)

### Ejercicio B1: Creación de Métricas
```python
# TODO: Crear las siguientes columnas:
# 1. 'eficiencia_presupuesto': (presupuesto - gastado) / presupuesto * 100
# 2. 'desviacion_horas': (horas_reales - horas_planificadas) / horas_planificadas * 100
# 3. 'duracion_real_dias': diferencia entre fecha_fin_real y fecha_inicio
# 4. 'estado_presupuesto': 'Bajo Presupuesto', 'Sobre Presupuesto', 'Sin Datos'

# Tu código aquí:
```

### Ejercicio B2: Categorización Avanzada
```python
# TODO: Crear una función que categorice proyectos según:
# - Tamaño (basado en presupuesto y equipo)
# - Riesgo (basado en desviaciones y estado)
# - Prioridad (basado en satisfacción y cliente)

def categorizar_proyecto(row):
    # Tu implementación aquí
    pass

# proyectos['categoria'] = proyectos.apply(categorizar_proyecto, axis=1)
```

### Ejercicio B3: Transformaciones Temporales
```python
# TODO: 
# 1. Extraer mes y trimestre de fecha_inicio
# 2. Calcular días desde el inicio hasta hoy
# 3. Identificar proyectos que van con retraso vs planificación

# Tu código aquí:
```

## Parte C: Manejo de Valores Faltantes (30 minutos)

### Ejercicio C1: Detección y Análisis
```python
# TODO:
# 1. Identificar patrones de valores faltantes
# 2. Calcular porcentaje de completitud por columna
# 3. Analizar si hay correlación entre valores faltantes

# Tu código aquí:
```

### Ejercicio C2: Estrategias de Imputación
```python
# TODO: 
# 1. Para 'gastado': imputar usando regresión basada en presupuesto y horas
# 2. Para 'satisfaccion': imputar por grupos de estado y región
# 3. Para 'fecha_fin_real': usar fecha_fin_planificada cuando sea lógico

# Tu código aquí:
```

### Ejercicio C3: Validación de Imputaciones
```python
# TODO:
# 1. Comparar distribuciones antes/después de imputación
# 2. Verificar que las imputaciones son plausibles
# 3. Calcular métricas de calidad de imputación

# Tu código aquí:
```

## Parte D: Análisis Integrado (30 minutos)

### Ejercicio D1: Pipeline Completo
```python
# TODO: Crear una función que:
# 1. Limpie y transforme los datos
# 2. Maneje valores faltantes
# 3. Cree métricas de negocio
# 4. Genere un reporte de calidad

def procesar_proyectos(df_raw):
    # Tu implementación aquí
    pass
```

### Ejercicio D2: Insights de Negocio
```python
# TODO: Responder con código:
# 1. ¿Qué región tiene mejor eficiencia de presupuesto?
# 2. ¿Hay correlación entre tamaño de equipo y satisfacción?
# 3. ¿Qué tipo de proyecto tiene mayor variabilidad en costos?

# Tu análisis aquí:
```

## Soluciones Esperadas

### Parte A - Ejemplo de Solución
```python
# A1: Filtros complejos
# 1. En progreso con presupuesto alto
filtro_1 = proyectos[
    (proyectos['estado'] == 'En Progreso') & 
    (proyectos['presupuesto'] > 150000)
]

# 2. Norte/Sur con alta satisfacción
filtro_2 = proyectos[
    proyectos['region'].isin(['Norte', 'Sur']) & 
    (proyectos['satisfaccion'] >= 8.0)
]

# 3. No completados con equipos grandes
filtro_3 = proyectos[
    ~(proyectos['estado'] == 'Completado') & 
    (proyectos['equipo_size'] > 6)
]
```

## Criterios de Evaluación

### Excelente (90-100%)
- ✅ Todos los filtros funcionan correctamente
- ✅ Transformaciones son eficientes y bien documentadas
- ✅ Manejo robusto de valores faltantes
- ✅ Código limpio y reutilizable
- ✅ Insights de negocio relevantes

### Bueno (80-89%)
- ✅ La mayoría de ejercicios completados correctamente
- ✅ Algunas optimizaciones o casos edge no considerados
- ✅ Documentación básica presente

### Suficiente (70-79%)
- ✅ Ejercicios básicos completados
- ⚠️ Algunos errores en lógica compleja
- ⚠️ Falta documentación o explicaciones

### Necesita Mejora (<70%)
- ❌ Errores frecuentes en sintaxis o lógica
- ❌ No completa ejercicios principales
- ❌ Falta comprensión de conceptos clave

## Tiempo Estimado
**Total: 2 horas**
- Parte A: 30 minutos
- Parte B: 30 minutos  
- Parte C: 30 minutos
- Parte D: 30 minutos

## Recursos Adicionales
- [Documentación de Pandas - Filtrado](https://pandas.pydata.org/docs/user_guide/indexing.html)
- [Guía de Imputación](https://scikit-learn.org/stable/modules/impute.html)
- [Mejores Prácticas - Transformación de Datos](https://pandas.pydata.org/docs/user_guide/cookbook.html)