# Detección de Valores Faltantes

## Introducción

Los valores faltantes son una realidad común en el análisis de datos. En consultoría, es crucial identificar, entender y manejar adecuadamente estos valores para garantizar análisis precisos y decisiones bien fundamentadas. La detección temprana y correcta de valores faltantes es el primer paso para una limpieza de datos efectiva.

## 🎯 Objetivos de esta Sección

- Identificar diferentes tipos de valores faltantes en los datos
- Utilizar métodos de Pandas para detectar valores NaN, nulos y vacíos
- Analizar patrones de valores faltantes
- Cuantificar el impacto de los valores faltantes en el análisis
- Desarrollar estrategias para manejar valores faltantes en diferentes contextos

## Tipos de Valores Faltantes

### Dataset con Problemas Típicos

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Crear dataset con diferentes tipos de valores faltantes
np.random.seed(42)

# Datos de encuesta de satisfacción con valores faltantes realistas
encuesta_satisfaccion = pd.DataFrame({
    'cliente_id': [f'C{i:03d}' for i in range(1, 101)],
    'empresa': ['Empresa A'] * 30 + ['Empresa B'] * 25 + ['Empresa C'] * 20 + ['Empresa D'] * 15 + ['Empresa E'] * 10,
    'puntuacion_general': np.random.choice([1, 2, 3, 4, 5, np.nan], 100, p=[0.05, 0.10, 0.20, 0.35, 0.25, 0.05]),
    'recomendaria': np.random.choice(['Sí', 'No', 'Tal vez', np.nan, ''], 100, p=[0.60, 0.15, 0.15, 0.08, 0.02]),
    'tiempo_respuesta': np.random.choice([1, 2, 3, 4, 5, np.nan], 100, p=[0.30, 0.25, 0.20, 0.15, 0.05, 0.05]),
    'precio_satisfaccion': np.random.choice([1, 2, 3, 4, 5, np.nan], 100, p=[0.10, 0.15, 0.25, 0.30, 0.15, 0.05]),
    'comentarios': ['Excelente servicio', 'Buena experiencia', '', 'Muy satisfecho', 
                   np.nan, 'Regular', 'Podría mejorar', '', 'Perfecto', np.nan] * 10,
    'fecha_respuesta': pd.date_range('2024-01-01', periods=100, freq='D'),
    'canal_contacto': np.random.choice(['Email', 'Teléfono', 'Web', 'Presencial', np.nan, ''], 
                                     100, p=[0.30, 0.25, 0.20, 0.15, 0.08, 0.02]),
    'ingresos_anuales': np.random.choice([100000, 500000, 1000000, 5000000, np.nan, 0], 
                                       100, p=[0.20, 0.30, 0.25, 0.15, 0.08, 0.02])
})

print("Dataset de encuesta con valores faltantes:")
print(encuesta_satisfaccion.head(10))
print(f"\nForma del dataset: {encuesta_satisfaccion.shape}")
```

## Métodos Básicos de Detección

### Detección con isna() y isnull()

```python
# isna() e isnull() son equivalentes
print("Verificación de equivalencia:")
print("Son iguales:", encuesta_satisfaccion.isna().equals(encuesta_satisfaccion.isnull()))

# Conteo de valores faltantes por columna
valores_faltantes = encuesta_satisfaccion.isna().sum()
print("\nValores faltantes por columna:")
print(valores_faltantes)

# Porcentaje de valores faltantes
porcentaje_faltantes = (encuesta_satisfaccion.isna().sum() / len(encuesta_satisfaccion)) * 100
print("\nPorcentaje de valores faltantes por columna:")
print(porcentaje_faltantes.round(2))
```

### Detección de Valores Vacíos (Strings)

```python
# Función para detectar diferentes tipos de "vacío"
def detectar_valores_problematicos(df):
    """Detecta diferentes tipos de valores problemáticos."""
    resultado = {}
    
    for columna in df.columns:
        if df[columna].dtype == 'object':  # Columnas de texto
            # Valores NaN
            nan_count = df[columna].isna().sum()
            
            # Strings vacíos
            empty_string_count = (df[columna] == '').sum()
            
            # Strings solo con espacios
            whitespace_count = df[columna].str.strip().eq('').sum() - empty_string_count
            
            # Valores que parecen nulos pero son strings
            null_like_count = df[columna].str.lower().isin(['null', 'none', 'na', 'n/a']).sum()
            
            resultado[columna] = {
                'NaN': nan_count,
                'Vacío': empty_string_count,
                'Solo espacios': whitespace_count,
                'Null-like': null_like_count,
                'Total problemáticos': nan_count + empty_string_count + whitespace_count + null_like_count
            }
        else:
            # Para columnas numéricas, solo NaN
            nan_count = df[columna].isna().sum()
            resultado[columna] = {
                'NaN': nan_count,
                'Total problemáticos': nan_count
            }
    
    return pd.DataFrame(resultado).T

problemas_detectados = detectar_valores_problematicos(encuesta_satisfaccion)
print("Análisis detallado de valores problemáticos:")
print(problemas_detectados)
```

## Análisis de Patrones de Valores Faltantes

### Matriz de Valores Faltantes

```python
# Crear matriz de valores faltantes
def crear_matriz_faltantes(df):
    """Crea una matriz visual de valores faltantes."""
    # Preparar datos para visualización
    missing_data = df.isna()
    
    # Calcular estadísticas
    missing_counts = missing_data.sum()
    missing_percent = (missing_counts / len(df)) * 100
    
    # Crear DataFrame resumen
    missing_summary = pd.DataFrame({
        'Columna': missing_counts.index,
        'Valores_Faltantes': missing_counts.values,
        'Porcentaje': missing_percent.values,
        'Valores_Presentes': len(df) - missing_counts.values
    })
    
    return missing_summary.sort_values('Porcentaje', ascending=False)

matriz_faltantes = crear_matriz_faltantes(encuesta_satisfaccion)
print("Resumen de valores faltantes:")
print(matriz_faltantes)
```

### Análisis de Correlación entre Valores Faltantes

```python
# Analizar si los valores faltantes están correlacionados entre columnas
def analizar_correlacion_faltantes(df):
    """Analiza correlaciones entre patrones de valores faltantes."""
    # Crear matriz binaria de valores faltantes
    missing_matrix = df.isna().astype(int)
    
    # Calcular correlación
    correlacion_faltantes = missing_matrix.corr()
    
    # Encontrar correlaciones altas (>0.3) excluyendo diagonal
    correlaciones_altas = []
    for i in range(len(correlacion_faltantes.columns)):
        for j in range(i+1, len(correlacion_faltantes.columns)):
            corr_val = correlacion_faltantes.iloc[i, j]
            if abs(corr_val) > 0.3:
                correlaciones_altas.append({
                    'Columna_1': correlacion_faltantes.columns[i],
                    'Columna_2': correlacion_faltantes.columns[j],
                    'Correlacion': corr_val
                })
    
    return pd.DataFrame(correlaciones_altas)

correlaciones_faltantes = analizar_correlacion_faltantes(encuesta_satisfaccion)
print("Correlaciones altas entre valores faltantes:")
print(correlaciones_faltantes)
```

### Patrones de Combinaciones Faltantes

```python
# Analizar combinaciones comunes de valores faltantes
def analizar_patrones_combinados(df):
    """Identifica patrones comunes de valores faltantes."""
    # Crear patrón de faltantes para cada fila
    patron_faltantes = df.isna().apply(lambda row: ''.join(['1' if x else '0' for x in row]), axis=1)
    
    # Contar patrones
    conteo_patrones = patron_faltantes.value_counts()
    
    # Crear interpretación legible
    patrones_interpretados = []
    for patron, count in conteo_patrones.head(10).items():
        columnas_faltantes = [col for i, col in enumerate(df.columns) if patron[i] == '1']
        patrones_interpretados.append({
            'Patrón': patron,
            'Frecuencia': count,
            'Porcentaje': (count / len(df)) * 100,
            'Columnas_Faltantes': ', '.join(columnas_faltantes) if columnas_faltantes else 'Ninguna'
        })
    
    return pd.DataFrame(patrones_interpretados)

patrones_combinados = analizar_patrones_combinados(encuesta_satisfaccion)
print("Patrones más comunes de valores faltantes:")
print(patrones_combinados)
```

## Análisis por Segmentos

### Valores Faltantes por Grupos

```python
# Analizar valores faltantes por empresa
def analizar_faltantes_por_grupo(df, columna_grupo):
    """Analiza patrones de valores faltantes por grupo."""
    resultado = {}
    
    for grupo in df[columna_grupo].unique():
        if pd.notna(grupo):  # Ignorar grupos con valor faltante
            subset = df[df[columna_grupo] == grupo]
            faltantes_grupo = subset.isna().sum()
            porcentaje_grupo = (faltantes_grupo / len(subset)) * 100
            
            resultado[grupo] = porcentaje_grupo
    
    return pd.DataFrame(resultado).T

faltantes_por_empresa = analizar_faltantes_por_grupo(encuesta_satisfaccion, 'empresa')
print("Porcentaje de valores faltantes por empresa:")
print(faltantes_por_empresa.round(2))
```

### Detección de Valores Atípicos como "Faltantes"

```python
# Detectar valores que podrían ser errores y deberían tratarse como faltantes
def detectar_valores_atipicos_como_faltantes(df):
    """Identifica valores que podrían ser errores de entrada."""
    problemas_detectados = {}
    
    for columna in df.columns:
        problemas = []
        
        if df[columna].dtype in ['int64', 'float64']:
            # Valores extremos (outliers severos)
            Q1 = df[columna].quantile(0.25)
            Q3 = df[columna].quantile(0.75)
            IQR = Q3 - Q1
            limite_inferior = Q1 - 3 * IQR
            limite_superior = Q3 + 3 * IQR
            
            outliers = df[(df[columna] < limite_inferior) | (df[columna] > limite_superior)][columna]
            if len(outliers) > 0:
                problemas.append(f"Outliers extremos: {len(outliers)} valores")
            
            # Valores negativos donde no deberían existir
            if 'ingresos' in columna.lower() or 'puntuacion' in columna.lower():
                negativos = df[df[columna] < 0][columna]
                if len(negativos) > 0:
                    problemas.append(f"Valores negativos: {len(negativos)} valores")
            
            # Valores de 0 que podrían ser faltantes
            if 'ingresos' in columna.lower():
                ceros = df[df[columna] == 0][columna]
                if len(ceros) > 0:
                    problemas.append(f"Valores cero (posibles faltantes): {len(ceros)} valores")
        
        elif df[columna].dtype == 'object':
            # Valores inconsistentes en texto
            valores_unicos = df[columna].value_counts()
            
            # Detectar variaciones menores que podrían ser errores
            for valor in valores_unicos.index:
                if pd.notna(valor) and len(str(valor)) > 0:
                    similares = [v for v in valores_unicos.index 
                               if pd.notna(v) and v != valor and 
                               str(v).lower().strip() == str(valor).lower().strip()]
                    if similares:
                        problemas.append(f"Posibles duplicados: '{valor}' y similares")
                        break
        
        if problemas:
            problemas_detectados[columna] = problemas
    
    return problemas_detectados

valores_atipicos = detectar_valores_atipicos_como_faltantes(encuesta_satisfaccion)
print("Valores que podrían considerarse como faltantes:")
for columna, problemas in valores_atipicos.items():
    print(f"\n{columna}:")
    for problema in problemas:
        print(f"  - {problema}")
```

## Impacto de Valores Faltantes en el Análisis

### Evaluación del Impacto

```python
def evaluar_impacto_faltantes(df):
    """Evalúa el impacto potencial de los valores faltantes."""
    impacto = {}
    
    total_filas = len(df)
    
    # Filas completamente completas
    filas_completas = df.dropna().shape[0]
    porcentaje_completas = (filas_completas / total_filas) * 100
    
    # Columnas más críticas (con más del 20% de faltantes)
    columnas_criticas = []
    for col in df.columns:
        pct_faltante = (df[col].isna().sum() / total_filas) * 100
        if pct_faltante > 20:
            columnas_criticas.append(col)
    
    # Impacto en análisis común
    impacto_correlacion = "Alto" if len(columnas_criticas) > 2 else "Medio" if len(columnas_criticas) > 0 else "Bajo"
    
    impacto = {
        'Total_Filas': total_filas,
        'Filas_Completas': filas_completas,
        'Porcentaje_Completas': porcentaje_completas,
        'Filas_Con_Faltantes': total_filas - filas_completas,
        'Columnas_Criticas': len(columnas_criticas),
        'Nombres_Columnas_Criticas': columnas_criticas,
        'Impacto_Estimado_Correlacion': impacto_correlacion
    }
    
    return impacto

impacto_analisis = evaluar_impacto_faltantes(encuesta_satisfaccion)
print("Evaluación de impacto de valores faltantes:")
for clave, valor in impacto_analisis.items():
    print(f"{clave}: {valor}")
```

## Casos Prácticos en Consultoría

### Caso 1: Análisis de Encuesta con Valores Faltantes Sistemáticos

```python
def analizar_sesgo_no_respuesta(df):
    """Analiza posible sesgo por no respuesta en encuestas."""
    # Crear flag de respuesta completa
    df['respuesta_completa'] = ~df[['puntuacion_general', 'recomendaria', 'tiempo_respuesta']].isna().any(axis=1)
    
    # Analizar características de quienes no responden completamente
    analisis_sesgo = {}
    
    # Por empresa
    sesgo_empresa = df.groupby('empresa')['respuesta_completa'].agg(['count', 'sum', 'mean'])
    sesgo_empresa.columns = ['Total_Respuestas', 'Respuestas_Completas', 'Tasa_Completitud']
    
    print("Análisis de sesgo por empresa:")
    print(sesgo_empresa)
    
    # Identificar si ciertas preguntas se saltan juntas
    preguntas_opinion = ['puntuacion_general', 'recomendaria', 'tiempo_respuesta', 'precio_satisfaccion']
    patron_saltos = df[preguntas_opinion].isna().sum()
    
    print("\nPatrón de saltos por pregunta:")
    print(patron_saltos.sort_values(ascending=False))
    
    return sesgo_empresa

sesgo_respuesta = analizar_sesgo_no_respuesta(encuesta_satisfaccion)
```

### Caso 2: Detección de Problemas de Calidad de Datos

```python
def detectar_problemas_calidad(df):
    """Detecta problemas sistemáticos de calidad de datos."""
    problemas = []
    
    # 1. Columnas con demasiados faltantes
    umbral_critico = 0.3  # 30%
    for col in df.columns:
        pct_faltante = df[col].isna().sum() / len(df)
        if pct_faltante > umbral_critico:
            problemas.append({
                'Tipo': 'Demasiados faltantes',
                'Columna': col,
                'Severidad': 'Alta',
                'Descripcion': f'{pct_faltante:.1%} de valores faltantes',
                'Recomendacion': 'Revisar proceso de recolección'
            })
    
    # 2. Patrones sospechosos de faltantes
    for col in df.select_dtypes(include=['object']).columns:
        if df[col].dtype == 'object':
            # Demasiados valores vacíos
            empty_count = (df[col] == '').sum()
            if empty_count > len(df) * 0.1:  # 10%
                problemas.append({
                    'Tipo': 'Valores vacíos',
                    'Columna': col,
                    'Severidad': 'Media',
                    'Descripcion': f'{empty_count} valores vacíos detectados',
                    'Recomendacion': 'Validar formularios de entrada'
                })
    
    # 3. Valores inconsistentes que podrían ser errores
    for col in df.select_dtypes(include=['number']).columns:
        if col != 'cliente_id':  # Excluir IDs
            # Verificar rango lógico
            if 'puntuacion' in col.lower():
                fuera_rango = df[(df[col] < 1) | (df[col] > 5)][col].dropna()
                if len(fuera_rango) > 0:
                    problemas.append({
                        'Tipo': 'Valores fuera de rango',
                        'Columna': col,
                        'Severidad': 'Alta',
                        'Descripcion': f'{len(fuera_rango)} valores fuera del rango 1-5',
                        'Recomendacion': 'Implementar validación en origen'
                    })
    
    return pd.DataFrame(problemas)

problemas_calidad = detectar_problemas_calidad(encuesta_satisfaccion)
print("Problemas de calidad detectados:")
print(problemas_calidad)
```

### Caso 3: Reporte Ejecutivo de Calidad de Datos

```python
def generar_reporte_calidad_ejecutivo(df):
    """Genera reporte ejecutivo sobre calidad de datos."""
    reporte = {}
    
    # Métricas generales
    total_registros = len(df)
    total_campos = len(df.columns)
    
    # Completitud general
    valores_totales = df.size
    valores_faltantes = df.isna().sum().sum()
    completitud_general = ((valores_totales - valores_faltantes) / valores_totales) * 100
    
    # Registros utilizables para análisis
    registros_completos = df.dropna().shape[0]
    registros_parciales = total_registros - registros_completos
    
    # Campos problemáticos
    umbral_problema = 0.15  # 15%
    campos_problematicos = 0
    for col in df.columns:
        if (df[col].isna().sum() / total_registros) > umbral_problema:
            campos_problematicos += 1
    
    # Score de calidad general
    score_completitud = min(completitud_general, 100)
    score_utilizabilidad = (registros_completos / total_registros) * 100
    score_consistencia = max(0, 100 - (campos_problematicos / total_campos) * 100)
    
    score_general = (score_completitud + score_utilizabilidad + score_consistencia) / 3
    
    reporte = {
        'Resumen_General': {
            'Total_Registros': total_registros,
            'Total_Campos': total_campos,
            'Completitud_General': f"{completitud_general:.1f}%",
            'Score_Calidad': f"{score_general:.1f}/100"
        },
        'Utilizabilidad_Datos': {
            'Registros_Completos': registros_completos,
            'Registros_Parciales': registros_parciales,
            'Porcentaje_Utilizable': f"{(registros_completos/total_registros)*100:.1f}%"
        },
        'Areas_Problematicas': {
            'Campos_Problematicos': campos_problematicos,
            'Impacto_Estimado': 'Alto' if campos_problematicos > 3 else 'Medio' if campos_problematicos > 1 else 'Bajo'
        }
    }
    
    return reporte

reporte_ejecutivo = generar_reporte_calidad_ejecutivo(encuesta_satisfaccion)
print("REPORTE EJECUTIVO - CALIDAD DE DATOS")
print("="*50)
for seccion, datos in reporte_ejecutivo.items():
    print(f"\n{seccion.replace('_', ' ').upper()}:")
    for clave, valor in datos.items():
        print(f"  {clave.replace('_', ' ')}: {valor}")
```

## Ejercicios Prácticos

### Ejercicio 1: Análisis Básico de Faltantes
```python
# TODO: Para el dataset de encuesta_satisfaccion:
# 1. Identifica la columna con mayor porcentaje de valores faltantes
# 2. Cuenta cuántas filas tienen exactamente 2 valores faltantes
# 3. Encuentra qué porcentaje de registros está completo

# Tu solución aquí:
```

### Ejercicio 2: Detección de Patrones
```python
# TODO: Analiza si existe correlación entre:
# 1. Falta de puntuación general y falta de recomendación
# 2. Empresa del cliente y probabilidad de respuesta incompleta
# 3. Valores faltantes en preguntas de satisfacción vs datos demográficos

# Tu solución aquí:
```

### Ejercicio 3: Evaluación de Impacto
```python
# TODO: Calcula el impacto de eliminar filas con valores faltantes:
# 1. ¿Cuántos registros quedarían si eliminas filas con ANY valor faltante?
# 2. ¿Cuántos quedarían si solo eliminas filas con >50% de faltantes?
# 3. ¿Qué columnas podrías eliminar para maximizar registros completos?

# Tu solución aquí:
```

## Mejores Prácticas

!!! tip "Consejos para Detección Efectiva"
    1. **Análisis sistemático**: Examina todos los tipos de "vacío" (NaN, '', espacios)
    2. **Contexto del negocio**: Entiende por qué faltan ciertos valores
    3. **Patrones temporales**: Verifica si los faltantes correlacionan con fechas
    4. **Documentación**: Registra hallazgos para referencia futura
    5. **Validación**: Confirma que valores extraños son realmente errores

### Checklist de Detección

```python
def checklist_deteccion_faltantes(df):
    """Checklist comprehensivo para detección de valores faltantes."""
    checklist = {
        '1. Conteo básico de NaN': df.isna().sum().sum() > 0,
        '2. Strings vacíos detectados': (df.select_dtypes(include=['object']).eq('').sum().sum() > 0),
        '3. Patrones de correlación analizados': True,  # Asumir que se ejecutó
        '4. Análisis por grupos realizado': True,       # Asumir que se ejecutó
        '5. Impacto en análisis evaluado': True,        # Asumir que se ejecutó
        '6. Outliers como faltantes considerados': True, # Asumir que se ejecutó
        '7. Reporte de calidad generado': True          # Asumir que se ejecutó
    }
    
    print("CHECKLIST DE DETECCIÓN DE VALORES FALTANTES")
    print("="*50)
    for item, completado in checklist.items():
        status = "✓" if completado else "✗"
        print(f"{status} {item}")
    
    return all(checklist.values())

checklist_completo = checklist_deteccion_faltantes(encuesta_satisfaccion)
print(f"\nChecklist completo: {'Sí' if checklist_completo else 'No'}")
```

## Resumen

La detección efectiva de valores faltantes te permite:

- ✅ Identificar problemas de calidad de datos tempranamente
- ✅ Entender patrones y causas de valores faltantes
- ✅ Evaluar el impacto en análisis posteriores
- ✅ Tomar decisiones informadas sobre estrategias de limpieza
- ✅ Desarrollar procesos robustos de validación de datos

**Próximo paso**: Continúa con [Estrategias de Manejo](estrategias-manejo.md) para aprender diferentes enfoques para tratar valores faltantes.