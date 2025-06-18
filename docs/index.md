# Fundamentos de Pandas II: Transformación y Análisis de Datos

## Bienvenidos a la Sesión 08

Este laboratorio está diseñado para consultores, analistas de datos y cualquier persona en Meridian Consulting que haya completado la Sesión 7 o tenga conocimientos básicos de Pandas.

### 📋 Información del Laboratorio

- **Duración:** 2 horas
- **Nivel:** Intermedio
- **Requisitos previos:** Sesión 7 completada o conocimientos básicos de Pandas (Series, DataFrames, importación básica)

### 🎯 Objetivos de Aprendizaje

Al finalizar este laboratorio, serás capaz de:

1. **Aplicar** técnicas de filtrado y selección de datos avanzadas
2. **Crear y modificar** columnas en DataFrames de manera eficiente
3. **Identificar y manejar** datos faltantes utilizando diversas estrategias
4. **Limpiar y transformar** datos para prepararlos para el análisis
5. **Utilizar** funciones de Pandas para realizar análisis básicos y obtener insights
6. **Aplicar** estos conocimientos a casos prácticos relevantes para el sector de consultoría

### 🛠️ Preparación del Entorno

#### Verificación de Pandas

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print(f"Versión de Pandas: {pd.__version__}")
print(f"Versión de NumPy: {np.__version__}")

# Configuración para mejor visualización
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 50)
```

!!! warning "Requisito Importante"
    Asegúrate de haber completado la Sesión 7 o tener conocimientos equivalentes en:
    
    - Creación de Series y DataFrames
    - Importación de datos CSV y Excel
    - Selección básica de datos
    - Exploración inicial de datos

### 📚 Estructura del Laboratorio

| Tiempo | Tema | Descripción | Duración |
|--------|------|-------------|----------|
| 0:00-0:15 | **Repaso y Introducción** | Conceptos de la Sesión 7 y transformación de datos | 15 min |
| 0:15-0:45 | **Filtrado y Selección Avanzada** | Múltiples condiciones, `isin()`, `loc` e `iloc` avanzado | 30 min |
| 0:45-1:15 | **Creación y Modificación de Columnas** | Nuevas columnas, cálculos, función `apply()` | 30 min |
| 1:15-1:45 | **Manejo de Datos Faltantes** | Detección, eliminación e imputación | 30 min |
| 1:45-2:00 | **Aplicación Práctica Integrada** | Casos reales y resumen | 15 min |

### 💼 Casos de Uso Avanzados en Consultoría

En esta sesión trabajaremos con escenarios más complejos y realistas:

#### 🎯 **Análisis de Proyectos Complejo**
- Identificación de proyectos retrasados
- Cálculo de métricas de rendimiento
- Imputación de fechas faltantes

#### 📊 **Transformación de Datos de Ventas**
- Creación de métricas de rentabilidad
- Análisis de tendencias por cliente
- Manejo de datos inconsistentes

#### 👥 **Limpieza de Datos de Empleados**
- Estandarización de nombres y departamentos
- Imputación inteligente de salarios
- Cálculo de antigüedad y métricas HR

#### 📋 **Procesamiento de Encuestas**
- Manejo de respuestas faltantes
- Cálculo de índices de satisfacción
- Análisis de patrones de respuesta

#### 💰 **Análisis Integrado de Gastos**
- Conversión de tipos de datos
- Validación de presupuestos
- Detección de anomalías

### 🚀 Nuevas Capacidades que Desarrollarás

#### **Filtrado Avanzado**
```python
# Múltiples condiciones
df[(df['revenue'] > 10000) & (df['region'].isin(['North', 'South']))]

# Filtrado complejo con OR y NOT
df[~(df['status'] == 'cancelled') | (df['priority'] == 'high')]
```

#### **Transformación de Datos**
```python
# Creación de columnas calculadas
df['profit_margin'] = (df['revenue'] - df['cost']) / df['revenue'] * 100

# Aplicación de funciones personalizadas
df['category'] = df['amount'].apply(lambda x: 'High' if x > 5000 else 'Low')
```

#### **Manejo de Datos Faltantes**
```python
# Detección inteligente
missing_summary = df.isnull().sum()

# Imputación estratégica
df['salary'] = df.groupby('department')['salary'].transform(
    lambda x: x.fillna(x.median())
)
```

### 📁 Estructura de Archivos Mejorada

```
sesion-08/
├── datos/                     # Datasets más complejos y realistas
│   ├── proyectos_completo.csv # Proyectos con datos faltantes
│   ├── ventas_detallado.csv   # Ventas con múltiples dimensiones
│   ├── empleados_sucio.csv    # Datos de empleados con inconsistencias
│   ├── encuestas_raw.xlsx     # Encuestas con respuestas faltantes
│   └── gastos_multi.xlsx      # Gastos con múltiples hojas
├── ejercicios/               # Ejercicios progresivos
├── soluciones/              # Soluciones completas
├── demos/                   # Scripts de demostración
└── docs/                   # Documentación completa
```

### 🎓 Metodología de Aprendizaje Avanzada

1. **Construcción sobre conocimientos previos**: Cada concepto se construye sobre la Sesión 7
2. **Práctica incremental**: Ejercicios que aumentan en complejidad gradualmente
3. **Casos reales**: Problemas basados en situaciones reales de consultoría
4. **Resolución de problemas**: Enfoque en la resolución práctica de problemas comunes

### 📊 Métricas de Progreso

Durante el laboratorio, desarrollarás competencias medibles:

- ✅ **Filtrado**: Capacidad de extraer subconjuntos complejos de datos
- ✅ **Transformación**: Creación de nuevas variables y métricas
- ✅ **Limpieza**: Identificación y corrección de problemas de calidad
- ✅ **Análisis**: Obtención de insights a partir de datos transformados

### 🔧 Herramientas y Técnicas Clave

| Técnica | Aplicación | Beneficio |
|---------|------------|-----------|
| `df.query()` | Filtrado con sintaxis SQL-like | Legibilidad mejorada |
| `df.assign()` | Creación de múltiples columnas | Código más limpio |
| `df.pipe()` | Encadenamiento de operaciones | Flujo de trabajo estructurado |
| `df.groupby().transform()` | Imputación por grupos | Precisión contextual |

### 💡 Consejos para el Éxito

!!! tip "Estrategias de Aprendizaje"
    - **Practica activamente**: Ejecuta cada ejemplo en tu entorno
    - **Experimenta**: Modifica los parámetros para ver diferentes resultados
    - **Conecta conceptos**: Relaciona cada técnica con casos de uso reales
    - **Documenta tu código**: Agrega comentarios explicativos
    - **Pregunta**: No dudes en consultar durante las demostraciones

!!! note "Preparación Recomendada"
    Antes de comenzar, ten listos:
    
    - Jupyter Notebook o VS Code configurado
    - Los archivos de datos descargados
    - Un cuaderno para tomar notas
    - Mentalidad de resolución de problemas

### 🔗 Enlaces de Referencia

- [Pandas User Guide - Data Cleaning](https://pandas.pydata.org/docs/user_guide/missing_data.html)
- [Pandas Cookbook - Advanced Operations](https://pandas.pydata.org/docs/user_guide/cookbook.html)
- [Real Python - Pandas Tutorials](https://realpython.com/learning-paths/pandas-data-science/)

### 🎯 Valor para Meridian Consulting

Al completar esta sesión, contribuirás a:

- **Mejora de la calidad de datos**: Procesos estandarizados de limpieza
- **Eficiencia en análisis**: Reducción del tiempo de preparación de datos
- **Consistencia metodológica**: Aplicación uniforme de técnicas
- **Capacidad analítica**: Generación de insights más profundos

---

¡Estás listo para llevar tus habilidades de Pandas al siguiente nivel! Comienza con [Filtrado Avanzado](conceptos/filtrado-avanzado.md) para empezar tu viaje hacia el dominio de la transformación de datos.