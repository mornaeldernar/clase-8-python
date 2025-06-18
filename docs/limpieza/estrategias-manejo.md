# Estrategias de Manejo de Valores Faltantes

## Introducción

Una vez identificados los valores faltantes, el siguiente paso crucial es decidir cómo manejarlos. No existe una solución única; la estrategia óptima depende del contexto del negocio, el tipo de datos, el porcentaje de valores faltantes, y el tipo de análisis que se realizará. Esta sección cubre las principales estrategias y cuándo aplicar cada una.

## 🎯 Objetivos de esta Sección

- Comprender las diferentes estrategias para manejar valores faltantes
- Aplicar criterios para seleccionar la estrategia más apropiada
- Implementar técnicas de eliminación y preservación de datos
- Evaluar el impacto de cada estrategia en el análisis
- Desarrollar un marco de decisión para casos complejos

## Estrategias Principales

### 1. Eliminación (Deletion)
### 2. Imputación (Imputation)
### 3. Marcado como Categoría Especial
### 4. Modelado Explícito

## Dataset de Trabajo

```python
import pandas as pd
import numpy as np
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer, KNNImputer

# Dataset de empleados con diferentes tipos de valores faltantes
np.random.seed(42)

empleados = pd.DataFrame({
    'empleado_id': [f'E{i:03d}' for i in range(1, 201)],
    'nombre': [f'Empleado {i}' for i in range(1, 201)],
    'departamento': np.random.choice(['IT', 'Ventas', 'Marketing', 'RRHH', 'Finanzas'], 200),
    'salario': np.random.normal(50000, 15000, 200),
    'antiguedad': np.random.randint(1, 15, 200),
    'evaluacion': np.random.normal(7.5, 1.5, 200),
    'bonificacion': np.random.normal(5000, 2000, 200),
    'ciudad': np.random.choice(['Madrid', 'Barcelona', 'Valencia', 'Sevilla'], 200),
    'nivel_educacion': np.random.choice(['Bachillerato', 'Grado', 'Máster', 'Doctorado'], 200),
    'fecha_ingreso': pd.date_range('2010-01-01', '2023-12-31', periods=200)
})

# Introducir valores faltantes de manera realista
# 1. Salarios faltantes para empleados nuevos (política de confidencialidad)
empleados.loc[empleados['antiguedad'] < 2, 'salario'] = np.where(
    np.random.random(sum(empleados['antiguedad'] < 2)) < 0.3, np.nan, 
    empleados.loc[empleados['antiguedad'] < 2, 'salario']
)

# 2. Evaluaciones faltantes para algunos empleados
missing_eval_mask = np.random.random(200) < 0.15
empleados.loc[missing_eval_mask, 'evaluacion'] = np.nan

# 3. Bonificaciones faltantes (no todos los departamentos las tienen)
dept_no_bonus = ['RRHH']
empleados.loc[empleados['departamento'].isin(dept_no_bonus), 'bonificacion'] = np.nan

# 4. Algunas bonificaciones faltantes aleatoriamente
random_bonus_missing = np.random.random(200) < 0.1
empleados.loc[random_bonus_missing, 'bonificacion'] = np.nan

# 5. Nivel educación faltante para empleados antiguos (datos no registrados)
empleados.loc[empleados['antiguedad'] > 10, 'nivel_educacion'] = np.where(
    np.random.random(sum(empleados['antiguedad'] > 10)) < 0.25, np.nan,
    empleados.loc[empleados['antiguedad'] > 10, 'nivel_educacion']
)

print("Dataset con valores faltantes introducidos:")
print(empleados.isna().sum())
print(f"\nForma del dataset: {empleados.shape}")
```

## Estrategia 1: Eliminación de Datos

### Eliminación de Filas (Listwise Deletion)

```python
# Análisis del impacto de eliminar filas completas
def analizar_impacto_eliminacion_filas(df):
    """Analiza el impacto de eliminar filas con valores faltantes."""
    original_count = len(df)
    
    # Eliminar filas con ANY valor faltante
    df_any_na = df.dropna()
    perdida_any = ((original_count - len(df_any_na)) / original_count) * 100
    
    # Eliminar filas con valores faltantes en columnas críticas
    columnas_criticas = ['salario', 'evaluacion']  # Columnas esenciales para análisis
    df_criticas = df.dropna(subset=columnas_criticas)
    perdida_criticas = ((original_count - len(df_criticas)) / original_count) * 100
    
    # Análisis de sesgo potencial
    def analizar_sesgo(df_original, df_filtrado, columna):
        if columna in df_original.columns and df_original[columna].dtype in ['int64', 'float64']:
            media_original = df_original[columna].mean()
            media_filtrada = df_filtrado[columna].mean()
            diferencia = abs(media_filtrada - media_original) / media_original * 100
            return diferencia
        return None
    
    sesgo_antiguedad = analizar_sesgo(df, df_any_na, 'antiguedad')
    
    resultado = {
        'Eliminación ANY NA': {
            'Registros_Perdidos': original_count - len(df_any_na),
            'Porcentaje_Perdido': perdida_any,
            'Registros_Restantes': len(df_any_na)
        },
        'Eliminación Columnas Críticas': {
            'Registros_Perdidos': original_count - len(df_criticas),
            'Porcentaje_Perdido': perdida_criticas,
            'Registros_Restantes': len(df_criticas)
        },
        'Análisis_Sesgo': {
            'Cambio_Media_Antigüedad': f"{sesgo_antiguedad:.2f}%" if sesgo_antiguedad else "N/A"
        }
    }
    
    return resultado, df_any_na, df_criticas

impacto_eliminacion, df_sin_na, df_criticas_sin_na = analizar_impacto_eliminacion_filas(empleados)

print("IMPACTO DE ELIMINACIÓN DE FILAS")
print("="*40)
for estrategia, datos in impacto_eliminacion.items():
    print(f"\n{estrategia}:")
    for metrica, valor in datos.items():
        print(f"  {metrica}: {valor}")
```

### Eliminación de Columnas

```python
def evaluar_eliminacion_columnas(df, umbral_faltantes=0.5):
    """Evalúa qué columnas deberían eliminarse por exceso de valores faltantes."""
    porcentaje_faltantes = df.isna().sum() / len(df)
    
    columnas_eliminar = porcentaje_faltantes[porcentaje_faltantes > umbral_faltantes].index.tolist()
    columnas_conservar = porcentaje_faltantes[porcentaje_faltantes <= umbral_faltantes].index.tolist()
    
    print(f"EVALUACIÓN DE ELIMINACIÓN DE COLUMNAS (umbral: {umbral_faltantes*100}%)")
    print("="*60)
    print(f"Columnas a eliminar: {columnas_eliminar}")
    print(f"Columnas a conservar: {columnas_conservar}")
    
    if columnas_eliminar:
        df_sin_columnas = df[columnas_conservar]
        registros_completos_nuevo = df_sin_columnas.dropna().shape[0]
        mejora = registros_completos_nuevo - df.dropna().shape[0]
        
        print(f"\nImpacto de eliminar columnas problemáticas:")
        print(f"  Registros completos originales: {df.dropna().shape[0]}")
        print(f"  Registros completos después: {registros_completos_nuevo}")
        print(f"  Mejora: +{mejora} registros ({mejora/len(df)*100:.1f}%)")
        
        return df_sin_columnas
    else:
        print("No hay columnas que excedan el umbral de eliminación.")
        return df

# Evaluar diferentes umbrales
for umbral in [0.3, 0.5, 0.7]:
    print(f"\n{'='*20} UMBRAL {umbral*100}% {'='*20}")
    df_evaluado = evaluar_eliminacion_columnas(empleados, umbral)
```

## Estrategia 2: Imputación de Valores

### Imputación Simple

```python
def imputacion_simple(df):
    """Aplica diferentes métodos de imputación simple."""
    df_imputado = df.copy()
    
    # 1. Media para variables numéricas
    columnas_numericas = df_imputado.select_dtypes(include=[np.number]).columns
    for col in columnas_numericas:
        if df_imputado[col].isna().any():
            media = df_imputado[col].mean()
            df_imputado[col].fillna(media, inplace=True)
            print(f"Imputación por media - {col}: {media:.2f}")
    
    # 2. Moda para variables categóricas
    columnas_categoricas = df_imputado.select_dtypes(include=['object']).columns
    for col in columnas_categoricas:
        if df_imputado[col].isna().any():
            moda = df_imputado[col].mode()[0] if not df_imputado[col].mode().empty else 'Desconocido'
            df_imputado[col].fillna(moda, inplace=True)
            print(f"Imputación por moda - {col}: {moda}")
    
    return df_imputado

print("IMPUTACIÓN SIMPLE")
print("="*20)
empleados_imputacion_simple = imputacion_simple(empleados)
print(f"\nValores faltantes después de imputación simple:")
print(empleados_imputacion_simple.isna().sum())
```

### Imputación por Grupos

```python
def imputacion_por_grupos(df):
    """Realiza imputación considerando grupos lógicos."""
    df_imputado = df.copy()
    
    # Imputar salario por departamento y antiguedad
    def imputar_salario_inteligente(grupo):
        if 'salario' in grupo.columns and grupo['salario'].isna().any():
            # Usar mediana del grupo, si no hay datos, usar mediana general
            mediana_grupo = grupo['salario'].median()
            if pd.isna(mediana_grupo):
                mediana_grupo = df['salario'].median()
            grupo['salario'].fillna(mediana_grupo, inplace=True)
        return grupo
    
    # Agrupar por departamento y nivel de antiguedad
    df_imputado['grupo_antiguedad'] = pd.cut(df_imputado['antiguedad'], 
                                           bins=[0, 3, 7, 15], 
                                           labels=['Junior', 'Senior', 'Veterano'])
    
    df_imputado = df_imputado.groupby(['departamento', 'grupo_antiguedad']).apply(imputar_salario_inteligente)
    
    # Imputar evaluación por departamento
    for dept in df_imputado['departamento'].unique():
        mask = df_imputado['departamento'] == dept
        if df_imputado.loc[mask, 'evaluacion'].isna().any():
            mediana_eval = df_imputado.loc[mask, 'evaluacion'].median()
            if pd.isna(mediana_eval):
                mediana_eval = df_imputado['evaluacion'].median()
            df_imputado.loc[mask, 'evaluacion'] = df_imputado.loc[mask, 'evaluacion'].fillna(mediana_eval)
            print(f"Imputación evaluación {dept}: {mediana_eval:.2f}")
    
    # Limpiar columna temporal
    df_imputado.drop('grupo_antiguedad', axis=1, inplace=True)
    
    return df_imputado

print("\nIMPUTACIÓN POR GRUPOS")
print("="*25)
empleados_imputacion_grupos = imputacion_por_grupos(empleados)
print(f"\nValores faltantes después de imputación por grupos:")
print(empleados_imputacion_grupos.isna().sum())
```

### Imputación Avanzada

```python
def imputacion_avanzada(df):
    """Aplica técnicas avanzadas de imputación."""
    df_numerico = df.select_dtypes(include=[np.number])
    df_categorico = df.select_dtypes(include=['object'])
    
    # 1. Imputación iterativa para variables numéricas
    print("Aplicando imputación iterativa...")
    iterative_imputer = IterativeImputer(random_state=42, max_iter=10)
    df_numerico_imputado = pd.DataFrame(
        iterative_imputer.fit_transform(df_numerico),
        columns=df_numerico.columns,
        index=df_numerico.index
    )
    
    # 2. Imputación KNN para una comparación
    print("Aplicando imputación KNN...")
    knn_imputer = KNNImputer(n_neighbors=5)
    df_numerico_knn = pd.DataFrame(
        knn_imputer.fit_transform(df_numerico),
        columns=df_numerico.columns,
        index=df_numerico.index
    )
    
    # 3. Para categóricas, usar la estrategia de grupos anterior
    df_categorico_imputado = df_categorico.copy()
    for col in df_categorico_imputado.columns:
        if df_categorico_imputado[col].isna().any():
            moda = df_categorico_imputado[col].mode()[0] if not df_categorico_imputado[col].mode().empty else 'Desconocido'
            df_categorico_imputado[col].fillna(moda, inplace=True)
    
    # Combinar resultados
    df_final_iterativo = pd.concat([df_categorico_imputado, df_numerico_imputado], axis=1)
    df_final_knn = pd.concat([df_categorico_imputado, df_numerico_knn], axis=1)
    
    return df_final_iterativo, df_final_knn

print("\nIMPUTACIÓN AVANZADA")
print("="*20)
empleados_iterativo, empleados_knn = imputacion_avanzada(empleados)

print("Valores faltantes después de imputación iterativa:")
print(empleados_iterativo.isna().sum())
print("\nValores faltantes después de imputación KNN:")
print(empleados_knn.isna().sum())
```

## Estrategia 3: Marcado como Categoría Especial

```python
def marcar_como_categoria_especial(df):
    """Trata valores faltantes como una categoría especial."""
    df_marcado = df.copy()
    
    # Para variables categóricas, crear categoría "No Disponible"
    columnas_categoricas = df_marcado.select_dtypes(include=['object']).columns
    for col in columnas_categoricas:
        if df_marcado[col].isna().any():
            df_marcado[col].fillna('No_Disponible', inplace=True)
            print(f"Marcado como 'No_Disponible' - {col}: {(df[col].isna().sum())} valores")
    
    # Para variables numéricas, crear flag indicador y usar valor centinela
    columnas_numericas = df_marcado.select_dtypes(include=[np.number]).columns
    for col in columnas_numericas:
        if df_marcado[col].isna().any():
            # Crear columna indicadora
            df_marcado[f'{col}_faltante'] = df_marcado[col].isna().astype(int)
            
            # Usar valor centinela (ej: -999 o valor fuera del rango normal)
            valor_centinela = -999
            df_marcado[col].fillna(valor_centinela, inplace=True)
            print(f"Marcado con centinela {valor_centinela} - {col}: {(df[col].isna().sum())} valores")
    
    return df_marcado

print("\nMARCADO COMO CATEGORÍA ESPECIAL")
print("="*35)
empleados_marcado = marcar_como_categoria_especial(empleados)
print(f"\nNuevas columnas indicadoras creadas:")
nuevas_columnas = [col for col in empleados_marcado.columns if col.endswith('_faltante')]
print(nuevas_columnas)
```

## Evaluación de Estrategias

```python
def evaluar_estrategias_imputacion(df_original, estrategias_dict):
    """Evalúa diferentes estrategias de imputación."""
    evaluacion = {}
    
    # Métricas base del dataset original
    registros_originales = len(df_original)
    
    for nombre_estrategia, df_estrategia in estrategias_dict.items():
        evaluacion[nombre_estrategia] = {}
        
        # 1. Completitud
        evaluacion[nombre_estrategia]['Registros_Completos'] = len(df_estrategia.dropna())
        evaluacion[nombre_estrategia]['Porcentaje_Completitud'] = (
            len(df_estrategia.dropna()) / len(df_estrategia) * 100
        )
        
        # 2. Preservación de datos
        evaluacion[nombre_estrategia]['Registros_Preservados'] = len(df_estrategia)
        evaluacion[nombre_estrategia]['Porcentaje_Preservado'] = (
            len(df_estrategia) / registros_originales * 100
        )
        
        # 3. Distribución de variables clave (ejemplo: salario)
        if 'salario' in df_estrategia.columns:
            media_original = df_original['salario'].mean()
            std_original = df_original['salario'].std()
            media_estrategia = df_estrategia['salario'].mean()
            std_estrategia = df_estrategia['salario'].std()
            
            evaluacion[nombre_estrategia]['Cambio_Media_Salario'] = (
                abs(media_estrategia - media_original) / media_original * 100
            )
            evaluacion[nombre_estrategia]['Cambio_Std_Salario'] = (
                abs(std_estrategia - std_original) / std_original * 100
            )
    
    return evaluacion

# Preparar diccionario de estrategias para evaluación
estrategias = {
    'Eliminación_Completa': empleados.dropna(),
    'Eliminación_Críticas': empleados.dropna(subset=['salario', 'evaluacion']),
    'Imputación_Simple': empleados_imputacion_simple,
    'Imputación_Grupos': empleados_imputacion_grupos,
    'Imputación_Iterativa': empleados_iterativo,
    'Imputación_KNN': empleados_knn,
    'Marcado_Especial': empleados_marcado
}

evaluacion_resultados = evaluar_estrategias_imputacion(empleados, estrategias)

print("\nEVALUACIÓN DE ESTRATEGIAS")
print("="*30)
df_evaluacion = pd.DataFrame(evaluacion_resultados).T
print(df_evaluacion.round(2))
```

## Marco de Decisión

```python
def recomendar_estrategia(df, contexto_negocio=None):
    """Recomienda estrategia basada en características de los datos y contexto."""
    
    # Análisis de características de los datos
    total_registros = len(df)
    porcentaje_completos = len(df.dropna()) / total_registros * 100
    columnas_con_faltantes = df.isna().any().sum()
    max_faltantes_columna = (df.isna().sum() / total_registros * 100).max()
    
    recomendaciones = []
    
    # Reglas de decisión
    if porcentaje_completos > 90:
        recomendaciones.append({
            'Estrategia': 'Eliminación de Filas',
            'Razón': 'Alto porcentaje de registros completos (>90%)',
            'Prioridad': 'Alta'
        })
    
    if max_faltantes_columna > 50:
        recomendaciones.append({
            'Estrategia': 'Eliminación de Columnas',
            'Razón': f'Columna con >50% faltantes ({max_faltantes_columna:.1f}%)',
            'Prioridad': 'Alta'
        })
    
    if 20 <= porcentaje_completos <= 80:
        recomendaciones.append({
            'Estrategia': 'Imputación por Grupos',
            'Razón': 'Nivel moderado de faltantes, posible estructura en datos',
            'Prioridad': 'Media'
        })
    
    if total_registros > 1000 and porcentaje_completos < 70:
        recomendaciones.append({
            'Estrategia': 'Imputación Avanzada (KNN/Iterativa)',
            'Razón': 'Dataset grande con muchos faltantes',
            'Prioridad': 'Media'
        })
    
    if contexto_negocio and 'regulatorio' in contexto_negocio.lower():
        recomendaciones.append({
            'Estrategia': 'Marcado como Categoría Especial',
            'Razón': 'Contexto regulatorio requiere trazabilidad',
            'Prioridad': 'Alta'
        })
    
    # Si no hay recomendaciones específicas
    if not recomendaciones:
        recomendaciones.append({
            'Estrategia': 'Imputación Simple',
            'Razón': 'Estrategia segura por defecto',
            'Prioridad': 'Baja'
        })
    
    return recomendaciones

print("\nRECOMENDACIONES DE ESTRATEGIA")
print("="*35)
recomendaciones = recomendar_estrategia(empleados, "Análisis de RRHH para reporte regulatorio")

for i, rec in enumerate(recomendaciones, 1):
    print(f"{i}. {rec['Estrategia']} (Prioridad: {rec['Prioridad']})")
    print(f"   Razón: {rec['Razón']}")
```

## Casos Prácticos

### Caso 1: Dataset de Ventas con Faltantes Estacionales

```python
def caso_ventas_estacionales():
    """Manejo de faltantes en datos de ventas con patrones estacionales."""
    # Simular datos de ventas con faltantes estacionales
    fechas = pd.date_range('2020-01-01', '2023-12-31', freq='D')
    ventas_data = {
        'fecha': fechas,
        'ventas': np.random.normal(1000, 200, len(fechas)),
        'region': np.random.choice(['Norte', 'Sur', 'Este', 'Oeste'], len(fechas)),
        'producto': np.random.choice(['A', 'B', 'C'], len(fechas))
    }
    
    df_ventas = pd.DataFrame(ventas_data)
    
    # Introducir faltantes estacionales (ej: menos datos en diciembre)
    mask_diciembre = df_ventas['fecha'].dt.month == 12
    faltantes_diciembre = np.random.random(mask_diciembre.sum()) < 0.3
    df_ventas.loc[mask_diciembre, 'ventas'] = np.where(faltantes_diciembre, np.nan, 
                                                      df_ventas.loc[mask_diciembre, 'ventas'])
    
    print("CASO: Ventas con Faltantes Estacionales")
    print("="*40)
    print(f"Total registros: {len(df_ventas)}")
    print(f"Faltantes por mes:")
    faltantes_por_mes = df_ventas.groupby(df_ventas['fecha'].dt.month)['ventas'].apply(lambda x: x.isna().sum())
    print(faltantes_por_mes)
    
    # Estrategia recomendada: Imputación con suavizado estacional
    df_ventas['mes'] = df_ventas['fecha'].dt.month
    df_ventas['año'] = df_ventas['fecha'].dt.year
    
    # Imputar usando promedio del mismo mes en otros años
    for region in df_ventas['region'].unique():
        for producto in df_ventas['producto'].unique():
            for mes in df_ventas['mes'].unique():
                mask = (df_ventas['region'] == region) & \
                       (df_ventas['producto'] == producto) & \
                       (df_ventas['mes'] == mes)
                
                if df_ventas.loc[mask, 'ventas'].isna().any():
                    promedio_historico = df_ventas.loc[mask, 'ventas'].mean()
                    if not pd.isna(promedio_historico):
                        df_ventas.loc[mask, 'ventas'].fillna(promedio_historico, inplace=True)
    
    print(f"\nDespués de imputación estacional:")
    print(f"Valores faltantes restantes: {df_ventas['ventas'].isna().sum()}")
    
    return df_ventas

df_ventas_caso = caso_ventas_estacionales()
```

## Ejercicios Prácticos

### Ejercicio 1: Análisis de Impacto
```python
# TODO: Para el dataset de empleados:
# 1. Compara el impacto de eliminar filas vs imputar por media en el análisis de correlación
# 2. ¿Cambia significativamente la correlación entre salario y evaluación?
# 3. ¿Qué estrategia preserva mejor las relaciones originales?

# Tu solución aquí:
```

### Ejercicio 2: Estrategia Híbrida
```python
# TODO: Desarrolla una estrategia híbrida que:
# 1. Elimine columnas con >40% de faltantes
# 2. Use imputación por grupos para variables numéricas
# 3. Marque como categoría especial las variables categóricas
# 4. Evalúe el resultado final

# Tu solución aquí:
```

### Ejercicio 3: Validación de Estrategia
```python
# TODO: Implementa una función que:
# 1. Divida el dataset en train/test
# 2. Aplique diferentes estrategias al conjunto train
# 3. Evalúe qué tan bien predice el conjunto test
# 4. Recomiende la mejor estrategia basada en performance

# Tu solución aquí:
```

## Mejores Prácticas

!!! tip "Guía para Selección de Estrategias"
    1. **Analiza el mecanismo**: ¿Por qué faltan los datos? (MCAR, MAR, MNAR)
    2. **Considera el contexto**: Requisitos del negocio y regulatorios
    3. **Evalúa el impacto**: Mide cómo cada estrategia afecta el análisis
    4. **Documenta decisiones**: Mantén registro de por qué elegiste cada estrategia
    5. **Valida resultados**: Verifica que la estrategia no introduce sesgos

### Plantilla de Decisión

```python
def plantilla_decision_faltantes(df, columna_objetivo=None):
    """Plantilla estructurada para decidir estrategia de manejo."""
    
    print("PLANTILLA DE DECISIÓN PARA VALORES FALTANTES")
    print("="*50)
    
    # 1. Caracterización del problema
    total_registros = len(df)
    faltantes_por_columna = df.isna().sum()
    porcentaje_faltantes = (faltantes_por_columna / total_registros * 100).round(2)
    
    print("1. CARACTERIZACIÓN DEL PROBLEMA:")
    print(f"   - Registros totales: {total_registros}")
    print(f"   - Columnas con faltantes: {(faltantes_por_columna > 0).sum()}")
    print(f"   - Máximo % faltantes: {porcentaje_faltantes.max()}%")
    
    # 2. Análisis de criticidad
    columnas_criticas = porcentaje_faltantes[porcentaje_faltantes > 30].index.tolist()
    columnas_moderadas = porcentaje_faltantes[(porcentaje_faltantes > 10) & (porcentaje_faltantes <= 30)].index.tolist()
    
    print("\n2. ANÁLISIS DE CRITICIDAD:")
    print(f"   - Columnas críticas (>30%): {columnas_criticas}")
    print(f"   - Columnas moderadas (10-30%): {columnas_moderadas}")
    
    # 3. Recomendaciones
    print("\n3. RECOMENDACIONES:")
    if columnas_criticas:
        print("   - Considerar eliminación de columnas críticas")
    if len(df.dropna()) / total_registros > 0.8:
        print("   - Eliminación de filas es viable (>80% completos)")
    else:
        print("   - Imputación recomendada para preservar datos")
    
    # 4. Estrategia sugerida
    if columna_objetivo:
        faltantes_objetivo = df[columna_objetivo].isna().sum()
        print(f"\n4. ANÁLISIS VARIABLE OBJETIVO ({columna_objetivo}):")
        print(f"   - Faltantes en objetivo: {faltantes_objetivo} ({faltantes_objetivo/total_registros*100:.1f}%)")
        
        if faltantes_objetivo > total_registros * 0.1:
            print("   - ADVERTENCIA: Variable objetivo con muchos faltantes")

# Aplicar plantilla
plantilla_decision_faltantes(empleados, 'salario')
```

## Resumen

Las estrategias de manejo de valores faltantes te permiten:

- ✅ Preservar la máxima cantidad de información útil
- ✅ Mantener la validez estadística de los análisis
- ✅ Adaptar el enfoque al contexto específico del negocio
- ✅ Minimizar sesgos introducidos por el manejo de faltantes
- ✅ Documentar y justificar decisiones metodológicas

**Próximo paso**: Continúa con [Técnicas de Imputación](tecnicas-imputacion.md) para profundizar en métodos específicos de imputación de valores.