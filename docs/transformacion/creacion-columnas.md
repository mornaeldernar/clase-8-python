# Creación y Modificación de Columnas

## Introducción

La creación de nuevas columnas es una habilidad fundamental en el análisis de datos. En consultoría, frecuentemente necesitas calcular métricas derivadas, crear indicadores de rendimiento, o transformar datos existentes para generar insights más profundos.

## 🎯 Objetivos de esta Sección

- Crear nuevas columnas basadas en cálculos con columnas existentes
- Aplicar operaciones aritméticas y lógicas
- Utilizar funciones condicionales para generar variables categóricas
- Implementar transformaciones complejas con funciones personalizadas

## Datos de Ejemplo

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Dataset de ventas para análisis
ventas = pd.DataFrame({
    'venta_id': ['V001', 'V002', 'V003', 'V004', 'V005', 'V006', 'V007', 'V008'],
    'cliente': ['Empresa A', 'Empresa B', 'Empresa C', 'Empresa A', 'Empresa D', 'Empresa B', 'Empresa C', 'Empresa E'],
    'producto': ['Consultoría', 'Software', 'Consultoría', 'Training', 'Software', 'Consultoría', 'Training', 'Software'],
    'cantidad': [1, 2, 1, 3, 1, 2, 2, 1],
    'precio_unitario': [50000, 25000, 75000, 15000, 30000, 60000, 20000, 35000],
    'descuento_pct': [0, 5, 10, 0, 15, 8, 5, 12],
    'fecha_venta': ['2024-01-15', '2024-01-20', '2024-02-10', '2024-02-15', '2024-03-05', '2024-03-10', '2024-03-20', '2024-04-01'],
    'vendedor': ['Ana', 'Carlos', 'María', 'Ana', 'Pedro', 'Carlos', 'María', 'Pedro']
})

# Convertir fecha a datetime
ventas['fecha_venta'] = pd.to_datetime(ventas['fecha_venta'])
print(ventas.info())
print(ventas.head())
```

## Creación de Columnas Básicas

### Operaciones Aritméticas Simples

```python
# Calcular ingresos brutos
ventas['ingresos_brutos'] = ventas['cantidad'] * ventas['precio_unitario']

# Calcular descuento en valor absoluto
ventas['descuento_valor'] = ventas['ingresos_brutos'] * (ventas['descuento_pct'] / 100)

# Calcular ingresos netos
ventas['ingresos_netos'] = ventas['ingresos_brutos'] - ventas['descuento_valor']

print("Columnas de cálculo básico:")
print(ventas[['venta_id', 'ingresos_brutos', 'descuento_valor', 'ingresos_netos']])
```

### Operaciones con Múltiples Columnas

```python
# Calcular margen de beneficio (asumiendo costo del 60% del precio)
ventas['costo_estimado'] = ventas['ingresos_brutos'] * 0.60
ventas['beneficio_estimado'] = ventas['ingresos_netos'] - ventas['costo_estimado']
ventas['margen_beneficio_pct'] = (ventas['beneficio_estimado'] / ventas['ingresos_netos']) * 100

print("Análisis de rentabilidad:")
print(ventas[['venta_id', 'ingresos_netos', 'beneficio_estimado', 'margen_beneficio_pct']])
```

## Creación de Columnas Condicionales

### Usando np.where() para Condiciones Simples

```python
# Clasificar ventas por tamaño
ventas['categoria_venta'] = np.where(
    ventas['ingresos_netos'] > 50000, 
    'Grande', 
    'Pequeña'
)

# Clasificar descuentos
ventas['tipo_descuento'] = np.where(
    ventas['descuento_pct'] > 10, 
    'Alto', 
    'Normal'
)

print("Categorización básica:")
print(ventas[['venta_id', 'ingresos_netos', 'categoria_venta', 'descuento_pct', 'tipo_descuento']])
```

### Condiciones Múltiples con np.select()

```python
# Crear clasificación de ventas más detallada
condiciones = [
    ventas['ingresos_netos'] >= 75000,
    ventas['ingresos_netos'] >= 50000,
    ventas['ingresos_netos'] >= 25000
]

categorias = ['Premium', 'Alta', 'Media']

ventas['segmento_venta'] = np.select(condiciones, categorias, default='Básica')

print("Segmentación detallada:")
print(ventas[['venta_id', 'ingresos_netos', 'segmento_venta']])
```

### Usando pd.cut() para Rangos

```python
# Crear segmentos de ingresos usando rangos
bins = [0, 30000, 60000, 90000, np.inf]
labels = ['Bajo', 'Medio', 'Alto', 'Premium']

ventas['rango_ingresos'] = pd.cut(ventas['ingresos_netos'], bins=bins, labels=labels, include_lowest=True)

print("Segmentación por rangos:")
print(ventas[['venta_id', 'ingresos_netos', 'rango_ingresos']])
```

## Transformaciones de Fechas

### Extracción de Componentes de Fecha

```python
# Extraer componentes de fecha
ventas['año'] = ventas['fecha_venta'].dt.year
ventas['mes'] = ventas['fecha_venta'].dt.month
ventas['trimestre'] = ventas['fecha_venta'].dt.quarter
ventas['dia_semana'] = ventas['fecha_venta'].dt.day_name()

print("Componentes de fecha:")
print(ventas[['venta_id', 'fecha_venta', 'año', 'mes', 'trimestre', 'dia_semana']])
```

### Cálculos con Fechas

```python
# Calcular días desde la primera venta
fecha_inicio = ventas['fecha_venta'].min()
ventas['dias_desde_inicio'] = (ventas['fecha_venta'] - fecha_inicio).dt.days

# Calcular días hasta hoy
hoy = datetime.now()
ventas['dias_desde_venta'] = (hoy - ventas['fecha_venta']).dt.days

print("Cálculos temporales:")
print(ventas[['venta_id', 'fecha_venta', 'dias_desde_inicio', 'dias_desde_venta']])
```

## Transformaciones de Texto

### Manipulación Básica de Strings

```python
# Normalizar nombres de clientes
ventas['cliente_normalizado'] = ventas['cliente'].str.upper()

# Extraer primera palabra del cliente
ventas['empresa_tipo'] = ventas['cliente'].str.split().str[0]

# Crear código corto del producto
ventas['producto_codigo'] = ventas['producto'].str[:4].str.upper()

print("Transformaciones de texto:")
print(ventas[['cliente', 'cliente_normalizado', 'empresa_tipo', 'producto', 'producto_codigo']])
```

### Creación de Variables Dummy/Categóricas

```python
# Crear variables dummy para vendedores
vendedor_dummies = pd.get_dummies(ventas['vendedor'], prefix='vendedor')
ventas = pd.concat([ventas, vendedor_dummies], axis=1)

print("Variables dummy para vendedores:")
print(ventas[['vendedor', 'vendedor_Ana', 'vendedor_Carlos', 'vendedor_María', 'vendedor_Pedro']])
```

## Funciones Personalizadas y apply()

### Función Simple con apply()

```python
# Función para calcular comisión del vendedor
def calcular_comision(row):
    base = row['ingresos_netos'] * 0.05  # 5% base
    if row['segmento_venta'] == 'Premium':
        bonus = row['ingresos_netos'] * 0.02  # 2% bonus adicional
    elif row['segmento_venta'] == 'Alta':
        bonus = row['ingresos_netos'] * 0.01  # 1% bonus adicional
    else:
        bonus = 0
    return base + bonus

ventas['comision_vendedor'] = ventas.apply(calcular_comision, axis=1)

print("Comisiones calculadas:")
print(ventas[['venta_id', 'vendedor', 'segmento_venta', 'ingresos_netos', 'comision_vendedor']])
```

### Funciones Más Complejas

```python
# Función para evaluar calidad de la venta
def evaluar_calidad_venta(row):
    score = 0
    
    # Puntos por tamaño de venta
    if row['ingresos_netos'] > 50000:
        score += 3
    elif row['ingresos_netos'] > 25000:
        score += 2
    else:
        score += 1
    
    # Puntos por margen
    if row['margen_beneficio_pct'] > 35:
        score += 2
    elif row['margen_beneficio_pct'] > 25:
        score += 1
    
    # Penalización por descuento alto
    if row['descuento_pct'] > 10:
        score -= 1
    
    # Clasificar
    if score >= 5:
        return 'Excelente'
    elif score >= 3:
        return 'Buena'
    else:
        return 'Regular'

ventas['calidad_venta'] = ventas.apply(evaluar_calidad_venta, axis=1)

print("Evaluación de calidad de ventas:")
print(ventas[['venta_id', 'ingresos_netos', 'margen_beneficio_pct', 'descuento_pct', 'calidad_venta']])
```

## Transformaciones Avanzadas

### Cálculos por Grupos

```python
# Calcular participación de cada venta en el total del cliente
ventas['total_cliente'] = ventas.groupby('cliente')['ingresos_netos'].transform('sum')
ventas['participacion_cliente_pct'] = (ventas['ingresos_netos'] / ventas['total_cliente']) * 100

# Ranking de ventas por vendedor
ventas['ranking_vendedor'] = ventas.groupby('vendedor')['ingresos_netos'].rank(ascending=False)

print("Análisis por grupos:")
print(ventas[['venta_id', 'cliente', 'vendedor', 'ingresos_netos', 'participacion_cliente_pct', 'ranking_vendedor']])
```

### Ventanas Móviles y Acumulados

```python
# Ordenar por fecha para cálculos secuenciales
ventas_ordenadas = ventas.sort_values('fecha_venta')

# Ingresos acumulados
ventas_ordenadas['ingresos_acumulados'] = ventas_ordenadas['ingresos_netos'].cumsum()

# Promedio móvil de 3 ventas
ventas_ordenadas['promedio_movil_3'] = ventas_ordenadas['ingresos_netos'].rolling(window=3).mean()

print("Análisis temporal:")
print(ventas_ordenadas[['venta_id', 'fecha_venta', 'ingresos_netos', 'ingresos_acumulados', 'promedio_movil_3']])
```

## Casos Prácticos de Consultoría

### Caso 1: Análisis de Rendimiento de Vendedores

```python
# Crear métricas comprehensivas de vendedores
metricas_vendedor = ventas.groupby('vendedor').agg({
    'venta_id': 'count',
    'ingresos_netos': ['sum', 'mean'],
    'comision_vendedor': 'sum',
    'margen_beneficio_pct': 'mean'
}).round(2)

# Aplanar columnas multiníve
metricas_vendedor.columns = ['num_ventas', 'ingresos_totales', 'ingreso_promedio', 'comision_total', 'margen_promedio']
metricas_vendedor.reset_index(inplace=True)

# Calcular eficiencia (ingresos por venta)
metricas_vendedor['eficiencia'] = metricas_vendedor['ingresos_totales'] / metricas_vendedor['num_ventas']

print("Métricas de rendimiento por vendedor:")
print(metricas_vendedor)
```

### Caso 2: Segmentación de Clientes

```python
# Análisis RFM simplificado (Recency, Frequency, Monetary)
hoy = datetime.now()

rfm_clientes = ventas.groupby('cliente').agg({
    'fecha_venta': lambda x: (hoy - x.max()).days,  # Recency
    'venta_id': 'count',  # Frequency
    'ingresos_netos': 'sum'  # Monetary
}).round(2)

rfm_clientes.columns = ['dias_ultima_compra', 'num_compras', 'valor_total']

# Crear scores RFM simplificados
rfm_clientes['score_recency'] = pd.cut(rfm_clientes['dias_ultima_compra'], bins=3, labels=[3, 2, 1])
rfm_clientes['score_frequency'] = pd.cut(rfm_clientes['num_compras'], bins=3, labels=[1, 2, 3])
rfm_clientes['score_monetary'] = pd.cut(rfm_clientes['valor_total'], bins=3, labels=[1, 2, 3])

# Score compuesto
rfm_clientes['rfm_score'] = (
    rfm_clientes['score_recency'].astype(int) + 
    rfm_clientes['score_frequency'].astype(int) + 
    rfm_clientes['score_monetary'].astype(int)
)

print("Análisis RFM de clientes:")
print(rfm_clientes)
```

### Caso 3: Indicadores de Alerta Temprana

```python
# Crear banderas de alerta para el negocio
def crear_alertas(df):
    df = df.copy()
    
    # Alerta: ventas con descuentos muy altos
    df['alerta_descuento'] = df['descuento_pct'] > 15
    
    # Alerta: margen muy bajo
    df['alerta_margen'] = df['margen_beneficio_pct'] < 20
    
    # Alerta: venta demasiado pequeña para el cliente
    promedio_cliente = df.groupby('cliente')['ingresos_netos'].transform('mean')
    df['alerta_venta_pequeña'] = df['ingresos_netos'] < (promedio_cliente * 0.5)
    
    # Contador total de alertas
    df['total_alertas'] = (
        df['alerta_descuento'].astype(int) + 
        df['alerta_margen'].astype(int) + 
        df['alerta_venta_pequeña'].astype(int)
    )
    
    return df

ventas_con_alertas = crear_alertas(ventas)

print("Ventas con alertas:")
alertas_ventas = ventas_con_alertas[ventas_con_alertas['total_alertas'] > 0]
print(alertas_ventas[['venta_id', 'cliente', 'alerta_descuento', 'alerta_margen', 'alerta_venta_pequeña', 'total_alertas']])
```

## Ejercicios Prácticos

### Ejercicio 1: Métricas Básicas
```python
# TODO: Crear las siguientes columnas:
# 1. 'precio_con_descuento': precio unitario después del descuento
# 2. 'categoria_precio': 'Alto' si precio_unitario > 40000, sino 'Normal'
# 3. 'mes_texto': nombre del mes de la venta

# Tu solución aquí:
```

### Ejercicio 2: Análisis Temporal
```python
# TODO: Crear columnas que muestren:
# 1. 'trimestre_texto': 'Q1', 'Q2', etc.
# 2. 'es_primer_semestre': True si la venta fue en los primeros 6 meses
# 3. 'semanas_desde_inicio': semanas transcurridas desde la primera venta

# Tu solución aquí:
```

### Ejercicio 3: Función Personalizada
```python
# TODO: Crear una función que evalúe el 'potencial_cliente':
# - 'Alto': si tiene más de 1 compra Y valor total > 50000
# - 'Medio': si tiene 1 compra Y valor > 30000, O más compras con valor total <= 50000
# - 'Bajo': otros casos

# Tu solución aquí:
```

## Mejores Prácticas

!!! tip "Consejos para Creación Eficiente de Columnas"
    1. **Nombres descriptivos**: Usa nombres que expliquen claramente el contenido
    2. **Funciones reutilizables**: Crea funciones para lógica compleja repetitiva
    3. **Validación**: Verifica los resultados con datos conocidos
    4. **Documentación**: Comenta la lógica de cálculos complejos
    5. **Eficiencia**: Usa operaciones vectorizadas cuando sea posible

### Ejemplo de Código Limpio

```python
# ❌ Mal - nombres confusos, lógica repetitiva
df['col1'] = df['a'] * df['b']
df['col2'] = np.where(df['col1'] > 1000, 'high', 'low')

# ✅ Bien - nombres claros, funciones reutilizables
def calcular_ingresos_totales(cantidad, precio):
    """Calcula ingresos totales multiplicando cantidad por precio."""
    return cantidad * precio

def categorizar_por_umbral(valores, umbral, etiqueta_alta='Alto', etiqueta_baja='Bajo'):
    """Categoriza valores usando un umbral específico."""
    return np.where(valores > umbral, etiqueta_alta, etiqueta_baja)

df['ingresos_totales'] = calcular_ingresos_totales(df['cantidad'], df['precio_unitario'])
df['categoria_ingresos'] = categorizar_por_umbral(df['ingresos_totales'], 1000, 'Alto', 'Bajo')
```

## Resumen

La creación y modificación de columnas te permite:

- ✅ Generar métricas de negocio relevantes
- ✅ Crear variables categóricas para análisis
- ✅ Transformar datos para facilitar interpretación
- ✅ Desarrollar indicadores de rendimiento
- ✅ Preparar datos para análisis avanzados

**Próximo paso**: Continúa con [Modificación de Datos](modificacion-datos.md) para aprender técnicas de actualización y corrección de datos existentes.