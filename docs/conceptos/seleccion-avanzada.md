# Selección Avanzada con loc e iloc

## Introducción

Los métodos `loc` e `iloc` son herramientas poderosas en Pandas que permiten selección precisa de datos. Mientras que `loc` utiliza etiquetas (labels), `iloc` utiliza posiciones numéricas. Dominar estas técnicas es crucial para manipular datos de manera eficiente en análisis de consultoría.

## 🎯 Objetivos de esta Sección

- Dominar la diferencia entre `loc` e `iloc`
- Aplicar selección avanzada con condiciones complejas
- Combinar selección de filas y columnas simultáneamente
- Utilizar estas técnicas en casos prácticos de consultoría

## Datos de Ejemplo

```python
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
```

## Método loc - Selección por Etiquetas

### Selección Básica con loc

```python
# Seleccionar un empleado específico
empleado_e003 = empleados.loc['E003']
print("Empleado E003:")
print(empleado_e003)
```

### Selección de Múltiples Filas

```python
# Múltiples empleados específicos
empleados_especificos = empleados.loc[['E001', 'E003', 'E005']]
print("Empleados específicos:")
print(empleados_especificos)
```

### Selección de Rangos

```python
# Rango de empleados (por índice)
rango_empleados = empleados.loc['E002':'E005']
print("Empleados E002 a E005:")
print(rango_empleados)
```

### Selección de Columnas Específicas

```python
# Empleado específico, columnas específicas
info_basica = empleados.loc['E001', ['nombre', 'departamento', 'salario']]
print("Información básica de E001:")
print(info_basica)
```

### Selección de Múltiples Filas y Columnas

```python
# Múltiples empleados, múltiples columnas
subset = empleados.loc[['E001', 'E003', 'E005'], ['nombre', 'salario', 'evaluacion']]
print("Subset específico:")
print(subset)
```

## Método iloc - Selección por Posición

### Selección Básica con iloc

```python
# Primer empleado (posición 0)
primer_empleado = empleados.iloc[0]
print("Primer empleado:")
print(primer_empleado)
```

### Selección por Rangos de Posición

```python
# Primeros 3 empleados
primeros_tres = empleados.iloc[0:3]
print("Primeros 3 empleados:")
print(primeros_tres)
```

### Selección de Columnas por Posición

```python
# Empleado en posición 1, columnas 0, 2, 3
empleado_cols = empleados.iloc[1, [0, 2, 3]]
print("Empleado posición 1, columnas específicas:")
print(empleado_cols)
```

### Selección de Subconjuntos

```python
# Filas 1-3, columnas 1-4
subconjunto = empleados.iloc[1:4, 1:5]
print("Subconjunto por posiciones:")
print(subconjunto)
```

## Selección Condicional Avanzada

### Usando loc con Condiciones Booleanas

```python
# Empleados de consultoría con salario alto
consultores_alto_salario = empleados.loc[
    (empleados['departamento'] == 'Consultoría') & 
    (empleados['salario'] > 65000)
]
print("Consultores con salario alto:")
print(consultores_alto_salario)
```

### Selección Condicional de Columnas Específicas

```python
# Solo mostrar información relevante de empleados con alta evaluación
alta_evaluacion = empleados.loc[
    empleados['evaluacion'] > 8.5, 
    ['nombre', 'departamento', 'evaluacion', 'salario']
]
print("Empleados con alta evaluación:")
print(alta_evaluacion)
```

### Combinando Múltiples Condiciones

```python
# Empleados senior (antigüedad > 4) con buen rendimiento (evaluación > 8.0)
empleados_senior = empleados.loc[
    (empleados['antiguedad'] > 4) & 
    (empleados['evaluacion'] > 8.0),
    ['nombre', 'antiguedad', 'evaluacion', 'salario']
]
print("Empleados senior con buen rendimiento:")
print(empleados_senior)
```

## Técnicas Avanzadas de Selección

### Uso de isin() con loc

```python
# Empleados de departamentos específicos en ciudades específicas
dept_ciudades = empleados.loc[
    empleados['departamento'].isin(['Consultoría', 'IT']) & 
    empleados['ciudad'].isin(['Madrid', 'Barcelona']),
    ['nombre', 'departamento', 'ciudad', 'salario']
]
print("Empleados de dept. específicos en ciudades principales:")
print(dept_ciudades)
```

### Selección con Funciones Lambda

```python
# Empleados con salario por encima de la mediana de su departamento
salario_mediano = empleados.groupby('departamento')['salario'].median()

empleados_sobre_mediana = empleados.loc[
    empleados.apply(
        lambda row: row['salario'] > salario_mediano[row['departamento']], 
        axis=1
    )
]
print("Empleados con salario sobre la mediana de su departamento:")
print(empleados_sobre_mediana[['nombre', 'departamento', 'salario']])
```

### Selección Dinámica con Variables

```python
# Definir criterios dinámicamente
departamento_objetivo = 'Consultoría'
salario_minimo = 63000
evaluacion_minima = 8.0

criterios_dinamicos = (
    (empleados['departamento'] == departamento_objetivo) &
    (empleados['salario'] >= salario_minimo) &
    (empleados['evaluacion'] >= evaluacion_minima)
)

empleados_objetivo = empleados.loc[criterios_dinamicos]
print(f"Empleados de {departamento_objetivo} que cumplen criterios:")
print(empleados_objetivo)
```

## Casos Prácticos en Consultoría

### Caso 1: Análisis de Compensación por Departamento

```python
# Analizar empleados de IT con compensación competitiva
empleados_it = empleados.loc[empleados['departamento'] == 'IT']

# Calcular percentiles de salario
p25_it = empleados_it['salario'].quantile(0.25)
p75_it = empleados_it['salario'].quantile(0.75)

# Empleados de IT en percentil alto
it_alto_salario = empleados.loc[
    (empleados['departamento'] == 'IT') & 
    (empleados['salario'] >= p75_it),
    ['nombre', 'salario', 'evaluacion', 'antiguedad']
]

print("Empleados de IT en percentil alto de salario:")
print(it_alto_salario)
print(f"Percentil 75 de IT: {p75_it}")
```

### Caso 2: Identificación de Talento de Alto Potencial

```python
# Definir criterios de alto potencial
alto_potencial = empleados.loc[
    (empleados['evaluacion'] >= 8.5) & 
    (empleados['antiguedad'] >= 2) & 
    (empleados['antiguedad'] <= 5),  # No muy senior, no muy junior
    ['nombre', 'departamento', 'evaluacion', 'antiguedad', 'salario']
]

print("Empleados de alto potencial:")
print(alto_potencial)
```

### Caso 3: Análisis Geográfico de Recursos

```python
# Distribución de departamentos por ciudad
for ciudad in empleados['ciudad'].unique():
    empleados_ciudad = empleados.loc[empleados['ciudad'] == ciudad]
    print(f"\n--- {ciudad} ---")
    print(empleados_ciudad[['nombre', 'departamento', 'salario']].sort_values('salario', ascending=False))
```

### Caso 4: Benchmarking Salarial

```python
# Comparar salarios por años de experiencia
experiencia_alta = empleados.loc[empleados['antiguedad'] >= 5]
experiencia_media = empleados.loc[
    (empleados['antiguedad'] >= 3) & (empleados['antiguedad'] < 5)
]
experiencia_baja = empleados.loc[empleados['antiguedad'] < 3]

print("Salario promedio por nivel de experiencia:")
print(f"Alta (5+ años): {experiencia_alta['salario'].mean():.0f}")
print(f"Media (3-4 años): {experiencia_media['salario'].mean():.0f}")
print(f"Baja (<3 años): {experiencia_baja['salario'].mean():.0f}")
```

## Selección con Índices Multijerárquicos

```python
# Crear un índice multijerárquico para análisis más complejo
empleados_multi = empleados.reset_index().set_index(['departamento', 'ciudad'])

print("Estructura con índice multijerárquico:")
print(empleados_multi.head())
```

### Selección en Índices Multijerárquicos

```python
# Seleccionar todos los empleados de Consultoría
consultoria = empleados_multi.loc['Consultoría']
print("Todos los empleados de Consultoría:")
print(consultoria)

# Seleccionar empleados de IT en Barcelona
it_barcelona = empleados_multi.loc[('IT', 'Barcelona')]
print("\nEmpleados de IT en Barcelona:")
print(it_barcelona)
```

## Modificación de Datos con loc e iloc

### Actualización de Valores Específicos

```python
# Actualizar salario de un empleado específico
empleados_copia = empleados.copy()
empleados_copia.loc['E001', 'salario'] = 70000

print("Salario actualizado para E001:")
print(empleados_copia.loc['E001', 'salario'])
```

### Actualización Condicional

```python
# Bonus del 10% para empleados con evaluación > 9.0
empleados_copia.loc[empleados_copia['evaluacion'] > 9.0, 'salario'] *= 1.10

print("Empleados con bonus (evaluación > 9.0):")
high_performers = empleados_copia.loc[empleados_copia['evaluacion'] > 9.0]
print(high_performers[['nombre', 'evaluacion', 'salario']])
```

## Ejercicios Prácticos

### Ejercicio 1: Selección Específica
```python
# TODO: Usando loc, selecciona:
# 1. Empleados E002, E004, E006
# 2. Solo las columnas: nombre, departamento, salario
# Tu solución aquí:
```

### Ejercicio 2: Selección Condicional
```python
# TODO: Encuentra empleados que:
# 1. Trabajen en Madrid O Barcelona
# 2. Tengan evaluación >= 8.0
# 3. Muestren solo: nombre, ciudad, evaluacion, salario
# Tu solución aquí:
```

### Ejercicio 3: Análisis con iloc
```python
# TODO: Usando iloc:
# 1. Selecciona los últimos 3 empleados
# 2. Solo las primeras 4 columnas
# Tu solución aquí:
```

## Mejores Prácticas

!!! tip "Consejos para Selección Eficiente"
    1. **loc para etiquetas**: Usa cuando trabajas con índices significativos
    2. **iloc para posiciones**: Útil para análisis exploratorio o muestreo
    3. **Combina con condiciones**: Para filtrado avanzado
    4. **Copia antes de modificar**: `df.copy()` para preservar datos originales
    5. **Verifica tipos**: Asegúrate de que las condiciones devuelvan booleanos

### Comparación de Rendimiento

```python
# Para datasets grandes, considera el rendimiento
import time

# Método 1: Filtrado tradicional
start = time.time()
resultado1 = empleados[empleados['departamento'] == 'Consultoría']
tiempo1 = time.time() - start

# Método 2: Usando loc
start = time.time()
resultado2 = empleados.loc[empleados['departamento'] == 'Consultoría']
tiempo2 = time.time() - start

print(f"Filtrado tradicional: {tiempo1:.6f}s")
print(f"Usando loc: {tiempo2:.6f}s")
```

## Resumen

La selección avanzada con `loc` e `iloc` te permite:

- ✅ Acceso preciso a datos específicos
- ✅ Filtrado complejo con múltiples condiciones
- ✅ Selección simultánea de filas y columnas
- ✅ Modificación eficiente de datos
- ✅ Análisis segmentado por criterios específicos

**Próximo paso**: Continúa con [Creación de Columnas](../transformacion/creacion-columnas.md) para aprender a generar nuevas variables a partir de los datos existentes.