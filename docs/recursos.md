# Recursos y Referencias

## 📚 Recursos Principales

### Documentación Oficial

#### Pandas
- **[Pandas User Guide](https://pandas.pydata.org/docs/user_guide/)** - Guía completa oficial
- **[Pandas API Reference](https://pandas.pydata.org/docs/reference/)** - Referencia detallada de funciones
- **[10 Minutes to Pandas](https://pandas.pydata.org/docs/user_guide/10min.html)** - Tutorial rápido oficial
- **[Pandas Cookbook](https://pandas.pydata.org/docs/user_guide/cookbook.html)** - Recetas para tareas comunes

#### NumPy (complementario)
- **[NumPy User Guide](https://numpy.org/doc/stable/user/)** - Para operaciones numéricas avanzadas
- **[NumPy for Pandas Users](https://numpy.org/doc/stable/user/pandas.html)** - Integración específica

#### Scikit-learn (para imputación)
- **[Imputation Guide](https://scikit-learn.org/stable/modules/impute.html)** - Técnicas de imputación avanzadas
- **[Preprocessing](https://scikit-learn.org/stable/modules/preprocessing.html)** - Preprocesamiento de datos

### Cheat Sheets y Referencias Rápidas

#### Pandas Cheat Sheets
- **[Pandas Cheat Sheet - Official](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)** (PDF)
- **[DataCamp Pandas Cheat Sheet](https://www.datacamp.com/cheat-sheet/pandas-cheat-sheet-for-data-science-in-python)** 
- **[Pandas Cheat Sheet - GitHub](https://github.com/pandas-dev/pandas/blob/main/doc/cheatsheet/Pandas_Cheat_Sheet.pdf)**

#### Funciones Clave por Categoría

**Filtrado y Selección:**
```python
# Métodos esenciales
df.loc[], df.iloc[]           # Selección por etiquetas/posición
df.query()                    # Filtrado con sintaxis SQL-like
df.isin()                     # Filtrado por múltiples valores
df.between()                  # Filtrado por rango
```

**Transformación:**
```python
# Métodos de transformación
df.apply()                    # Aplicar funciones personalizadas
df.assign()                   # Crear múltiples columnas
df.pipe()                     # Encadenar operaciones
df.transform()                # Transformaciones por grupo
```

**Valores Faltantes:**
```python
# Detección y manejo
df.isna(), df.notna()         # Detectar valores faltantes
df.dropna()                   # Eliminar filas/columnas
df.fillna()                   # Llenar valores faltantes
df.interpolate()              # Interpolación
```

## 📖 Libros Recomendados

### Principiantes
1. **"Python for Data Analysis"** - Wes McKinney
   - Autor original de Pandas
   - Cobertura completa desde básico a avanzado
   - Ejemplos prácticos relevantes

2. **"Pandas in Action"** - Boris Paskhaver
   - Enfoque muy práctico
   - Casos de uso del mundo real
   - Excelente para consultoría

### Intermedio-Avanzado
3. **"Effective Pandas"** - Matt Harrison
   - Técnicas avanzadas y optimización
   - Mejores prácticas industriales
   - Patrones de código eficiente

4. **"Data Wrangling with Python"** - Jacqueline Kazil
   - Enfoque en limpieza de datos
   - Casos complejos de transformación
   - Integración con otras herramientas

### Análisis Específico
5. **"Hands-On Data Analysis with Pandas"** - Stefanie Molin
   - Proyectos end-to-end
   - Visualización integrada
   - Casos de estudio financieros

## 🎥 Cursos y Tutoriales Online

### Cursos Estructurados
- **[DataCamp - Pandas Foundations](https://www.datacamp.com/courses/pandas-foundations)**
- **[Coursera - Applied Data Science with Python](https://www.coursera.org/specializations/data-science-python)**
- **[edX - Introduction to Data Analysis using Pandas](https://www.edx.org/course/introduction-to-data-analysis-using-pandas)**

### Tutoriales YouTube
- **[Corey Schafer - Pandas Tutorials](https://www.youtube.com/playlist?list=PL-osiE80TeTsWmV9i9c58mdDCSskIFdDS)**
- **[Data School - Pandas Q&A](https://www.youtube.com/user/dataschool)**
- **[Keith Galli - Complete Pandas Tutorial](https://www.youtube.com/watch?v=vmEHCJofslg)**

### Plataformas Interactivas
- **[Kaggle Learn - Pandas](https://www.kaggle.com/learn/pandas)** - Gratuito
- **[Real Python - Pandas Tutorials](https://realpython.com/learning-paths/pandas-data-science/)**
- **[W3Schools - Pandas Tutorial](https://www.w3schools.com/python/pandas/)**

## 💻 Herramientas y Entornos

### Entornos de Desarrollo
```bash
# Jupyter Notebook/Lab
pip install jupyter jupyterlab

# VS Code con extensiones
# - Python
# - Jupyter
# - Pandas Profiling

# Google Colab (online)
# https://colab.research.google.com/
```

### Librerías Complementarias
```bash
# Análisis de datos
pip install pandas numpy matplotlib seaborn

# Imputación avanzada
pip install scikit-learn

# Visualización
pip install plotly altair

# Profiling de datos
pip install pandas-profiling ydata-profiling

# Procesamiento de Excel
pip install openpyxl xlrd
```

### Configuración Recomendada
```python
# Configuraciones útiles para Pandas
import pandas as pd

# Mostrar más columnas
pd.set_option('display.max_columns', None)

# Mostrar más filas
pd.set_option('display.max_rows', 100)

# Ancho de columnas
pd.set_option('display.max_colwidth', 50)

# Precisión decimal
pd.set_option('display.float_format', '{:.2f}'.format)
```

## 🗂️ Datasets de Práctica

### Datasets Específicos para Consultoría
1. **Northwind Database** - Datos de ventas clásicos
2. **HR Analytics** - Datos de recursos humanos
3. **Customer Segmentation** - Análisis de clientes
4. **Financial Data** - Datos financieros históricos

### Repositorios de Datos
- **[Kaggle Datasets](https://www.kaggle.com/datasets)** - Amplia variedad
- **[UCI ML Repository](https://archive.ics.uci.edu/ml/datasets.php)** - Datasets académicos
- **[Data.gov](https://www.data.gov/)** - Datos gubernamentales
- **[World Bank Open Data](https://data.worldbank.org/)** - Datos económicos globales

### Generadores de Datos Sintéticos
```python
# Para crear datos de práctica
from faker import Faker
import numpy as np

fake = Faker()

# Generar datos de empleados
empleados = pd.DataFrame({
    'nombre': [fake.name() for _ in range(100)],
    'email': [fake.email() for _ in range(100)],
    'salario': np.random.normal(50000, 15000, 100)
})
```

## 🔍 Herramientas de Análisis

### Análisis Exploratorio
```python
# Pandas Profiling - reporte automático
from ydata_profiling import ProfileReport

profile = ProfileReport(df, title="Pandas Profiling Report")
profile.to_file("reporte.html")
```

### Validación de Datos
```python
# Great Expectations - validación robusta
import great_expectations as ge

# Convertir DataFrame a Great Expectations
gdf = ge.from_pandas(df)

# Crear expectativas
gdf.expect_column_values_to_not_be_null('columna_importante')
gdf.expect_column_values_to_be_in_set('categoria', ['A', 'B', 'C'])
```

### Visualización Rápida
```python
# Pandas integrado con matplotlib
df.plot(kind='hist')          # Histograma
df.plot(kind='box')           # Box plot
df.plot(kind='scatter', x='col1', y='col2')  # Scatter plot

# Seaborn para análisis más avanzado
import seaborn as sns
sns.pairplot(df)              # Matriz de correlación visual
sns.heatmap(df.corr())        # Mapa de calor de correlaciones
```

## 🐛 Debugging y Solución de Problemas

### Errores Comunes y Soluciones

#### MemoryError
```python
# Leer en chunks para archivos grandes
chunk_size = 10000
for chunk in pd.read_csv('archivo_grande.csv', chunksize=chunk_size):
    process_chunk(chunk)
```

#### SettingWithCopyWarning
```python
# Usar .copy() para evitar el warning
df_nuevo = df[df['columna'] > 0].copy()
df_nuevo['nueva_columna'] = valor
```

#### Tipos de Datos Incorrectos
```python
# Verificar y convertir tipos
print(df.dtypes)
df['fecha'] = pd.to_datetime(df['fecha'])
df['categoria'] = df['categoria'].astype('category')
```

### Herramientas de Debug
```python
# Debug paso a paso
import pdb; pdb.set_trace()

# Información detallada
df.info(memory_usage='deep')
df.describe(include='all')

# Verificar valores únicos
df['columna'].value_counts()
```

## 📝 Mejores Prácticas - Resumen

### Código Limpio
```python
# ✅ Buenas prácticas
def procesar_datos(df, columna_objetivo):
    """Procesa datos con documentación clara."""
    # Validar entrada
    assert columna_objetivo in df.columns, f"Columna {columna_objetivo} no existe"
    
    # Copiar para no modificar original
    df_procesado = df.copy()
    
    # Operaciones claras y comentadas
    df_procesado[f'{columna_objetivo}_normalizado'] = (
        df_procesado[columna_objetivo] / df_procesado[columna_objetivo].max()
    )
    
    return df_procesado

# ❌ Evitar
df.loc[df.col1>0,'col2'] = df.col3*2  # Difícil de leer
```

### Análisis Reproducible
```python
# Semilla para reproducibilidad
np.random.seed(42)

# Versionado de datos
print(f"Pandas version: {pd.__version__}")
print(f"NumPy version: {np.__version__}")

# Logging para análisis complejos
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

## 🤝 Comunidad y Soporte

### Foros y Comunidades
- **[Stack Overflow - Pandas Tag](https://stackoverflow.com/questions/tagged/pandas)**
- **[Reddit - r/pandas](https://www.reddit.com/r/pandas/)**
- **[GitHub - Pandas Issues](https://github.com/pandas-dev/pandas/issues)**

### Contribuir
- **[Pandas Contributing Guide](https://pandas.pydata.org/docs/development/contributing.html)**
- **[Good First Issues](https://github.com/pandas-dev/pandas/labels/good%20first%20issue)**

### Eventos y Conferencias
- **PyCon** - Conferencia anual de Python
- **SciPy Conference** - Enfoque científico
- **PyData** - Eventos locales sobre datos

---

## 📞 Contacto y Soporte

Para preguntas específicas sobre este laboratorio:

- **Email**: instructor@meridian-consulting.com
- **Slack**: #pandas-avanzado
- **Horario de oficina**: Martes y Jueves, 14:00-16:00

¡Esperamos que estos recursos te ayuden a dominar Pandas y aplicarlo efectivamente en proyectos de consultoría! 🚀