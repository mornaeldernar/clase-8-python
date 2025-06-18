# Filtrado y Selección Avanzada de Datos

## Introducción

El filtrado avanzado en Pandas te permite extraer subconjuntos específicos de datos utilizando condiciones complejas. Esta capacidad es fundamental para el análisis de datos en consultoría, donde necesitas identificar patrones específicos, segmentos de clientes, o proyectos que cumplan criterios particulares.

## 🎯 Objetivos de esta Sección

- Dominar el filtrado con múltiples condiciones
- Utilizar operadores lógicos (AND, OR, NOT)
- Aplicar el método `isin()` para filtros con múltiples valores
- Combinar diferentes técnicas de filtrado

## Filtrado con Múltiples Condiciones

### Operadores Lógicos Básicos

```python
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

print(proyectos)
```

### Operador AND (&)

Para proyectos que cumplan **ambas** condiciones:

```python
# Proyectos con presupuesto mayor a 50,000 Y duración menor a 50 días
filtro_and = proyectos[(proyectos['presupuesto'] > 50000) & 
                       (proyectos['duracion_dias'] < 50)]

print("Proyectos con presupuesto alto y duración corta:")
print(filtro_and)
```

!!! warning "Uso de Paréntesis"
    Es **obligatorio** usar paréntesis en cada condición cuando combines con operadores lógicos (`&`, `|`, `~`).

### Operador OR (|)

Para proyectos que cumplan **cualquiera** de las condiciones:

```python
# Proyectos retrasados O con presupuesto muy alto
filtro_or = proyectos[(proyectos['estado'] == 'Retrasado') | 
                      (proyectos['presupuesto'] > 100000)]

print("Proyectos retrasados o de alto presupuesto:")
print(filtro_or)
```

### Operador NOT (~)

Para **negar** una condición:

```python
# Proyectos que NO están completados
filtro_not = proyectos[~(proyectos['estado'] == 'Completado')]

print("Proyectos no completados:")
print(filtro_not)
```

## Método isin() para Múltiples Valores

### Uso Básico de isin()

Muy útil cuando quieres filtrar por múltiples valores específicos:

```python
# Proyectos de regiones específicas
regiones_interes = ['Norte', 'Sur']
filtro_regiones = proyectos[proyectos['region'].isin(regiones_interes)]

print("Proyectos de Norte y Sur:")
print(filtro_regiones)
```

### Combinando isin() con Otras Condiciones

```python
# Proyectos de ciertas regiones Y con presupuesto alto
filtro_complejo = proyectos[
    proyectos['region'].isin(['Norte', 'Centro']) & 
    (proyectos['presupuesto'] > 60000)
]

print("Proyectos de Norte/Centro con presupuesto alto:")
print(filtro_complejo)
```

### Uso Inverso de isin()

```python
# Proyectos que NO son de la región Norte
filtro_no_norte = proyectos[~proyectos['region'].isin(['Norte'])]

print("Proyectos fuera de la región Norte:")
print(filtro_no_norte)
```

## Método query() - Sintaxis Alternativa

Pandas ofrece el método `query()` que permite usar una sintaxis más legible, similar a SQL:

```python
# Sintaxis tradicional
filtro_tradicional = proyectos[
    (proyectos['presupuesto'] > 50000) & 
    (proyectos['duracion_dias'] < 50)
]

# Usando query() - más legible
filtro_query = proyectos.query('presupuesto > 50000 and duracion_dias < 50')

print("Ambos métodos producen el mismo resultado:")
print(filtro_query.equals(filtro_tradicional))
```

### Ventajas del Método query()

```python
# Consultas complejas más legibles
filtro_complejo_query = proyectos.query(
    'presupuesto > 40000 and '
    'estado in ["En Progreso", "Retrasado"] and '
    'region != "Centro"'
)

print("Filtro complejo con query():")
print(filtro_complejo_query)
```

## Casos Prácticos en Consultoría

### Caso 1: Identificación de Proyectos de Riesgo

```python
# Proyectos que requieren atención especial
proyectos_riesgo = proyectos[
    (proyectos['estado'] == 'Retrasado') |
    ((proyectos['presupuesto'] > 80000) & (proyectos['duracion_dias'] > 40))
]

print("Proyectos de riesgo:")
print(proyectos_riesgo[['proyecto_id', 'cliente', 'estado', 'presupuesto']])
```

### Caso 2: Análisis por Cliente Estratégico

```python
# Clientes con múltiples proyectos activos
clientes_estrategicos = ['Empresa A', 'Empresa B']

proyectos_estrategicos = proyectos[
    proyectos['cliente'].isin(clientes_estrategicos) & 
    (proyectos['estado'] != 'Completado')
]

print("Proyectos activos de clientes estratégicos:")
print(proyectos_estrategicos)
```

### Caso 3: Filtrado por Rangos de Presupuesto

```python
# Proyectos de presupuesto medio (entre 40k y 80k)
rango_medio = proyectos[
    (proyectos['presupuesto'] >= 40000) & 
    (proyectos['presupuesto'] <= 80000)
]

print("Proyectos de presupuesto medio:")
print(rango_medio)
```

## Técnicas Avanzadas

### Filtrado con Funciones Personalizadas

```python
# Función para identificar proyectos urgentes
def es_urgente(row):
    return (row['estado'] == 'Retrasado' or 
            (row['duracion_dias'] > 45 and row['presupuesto'] > 70000))

# Aplicar la función
proyectos['urgente'] = proyectos.apply(es_urgente, axis=1)
proyectos_urgentes = proyectos[proyectos['urgente']]

print("Proyectos urgentes:")
print(proyectos_urgentes[['proyecto_id', 'cliente', 'estado', 'urgente']])
```

### Filtrado con Expresiones Regulares

```python
# Clientes cuyo nombre contiene "Empresa"
import re

# Usando str.contains()
filtro_regex = proyectos[proyectos['cliente'].str.contains('Empresa [AB]')]

print("Clientes Empresa A o B:")
print(filtro_regex)
```

### Filtrado por Múltiples Columnas Simultáneamente

```python
# Condiciones que involucran múltiples métricas
condiciones_complejas = (
    (proyectos['presupuesto'] / proyectos['duracion_dias'] > 1500) &  # Alto valor diario
    (proyectos['estado'] != 'Completado') &
    (proyectos['region'].isin(['Norte', 'Sur']))
)

proyectos_complejos = proyectos[condiciones_complejas]
print("Proyectos con alta rentabilidad diaria:")
print(proyectos_complejos)
```

## Ejercicios Prácticos

### Ejercicio 1: Filtrado Básico
```python
# TODO: Encuentra todos los proyectos que:
# 1. Tengan un presupuesto mayor a 60,000
# 2. Y estén en estado "En Progreso" o "Retrasado"

# Tu solución aquí:
```

### Ejercicio 2: Uso de isin()
```python
# TODO: Encuentra proyectos que:
# 1. Sean de las regiones Norte o Centro
# 2. Y pertenezcan a Empresa A o Empresa C

# Tu solución aquí:
```

### Ejercicio 3: Filtrado con Negación
```python
# TODO: Encuentra proyectos que:
# 1. NO estén completados
# 2. Y NO sean de la región Sur

# Tu solución aquí:
```

## Mejores Prácticas

!!! tip "Consejos para Filtrado Eficiente"
    1. **Usa paréntesis**: Siempre en condiciones múltiples
    2. **query() para legibilidad**: En filtros complejos
    3. **isin() para listas**: En lugar de múltiples OR
    4. **Variables intermedias**: Para condiciones complejas reutilizables
    5. **Documentación**: Comenta filtros complejos

### Ejemplo de Código Limpio

```python
# ❌ Mal - difícil de leer
resultado = df[(df['col1'] > 100) & (df['col2'].isin(['A', 'B'])) & 
               (df['col3'] != 'X') | (df['col4'] < 50)]

# ✅ Bien - legible y mantenible
condicion_valor = df['col1'] > 100
condicion_categoria = df['col2'].isin(['A', 'B'])
condicion_exclusion = df['col3'] != 'X'
condicion_limite = df['col4'] < 50

resultado = df[
    (condicion_valor & condicion_categoria & condicion_exclusion) |
    condicion_limite
]
```

## Resumen

El filtrado avanzado es una habilidad esencial que te permite:

- ✅ Extraer datos específicos con múltiples criterios
- ✅ Identificar patrones y anomalías en los datos
- ✅ Segmentar información para análisis específicos
- ✅ Preparar datos para análisis posteriores

**Próximo paso**: Continúa con [Selección Avanzada con loc e iloc](seleccion-avanzada.md) para dominar técnicas de acceso a datos más sofisticadas.