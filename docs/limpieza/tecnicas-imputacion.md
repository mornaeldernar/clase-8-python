# Técnicas Avanzadas de Imputación

## Introducción

La imputación es el proceso de llenar valores faltantes con estimaciones plausibles. Esta sección profundiza en técnicas específicas de imputación, desde métodos estadísticos básicos hasta algoritmos de machine learning avanzados. El objetivo es proporcionar herramientas prácticas para diferentes escenarios en consultoría.

## 🎯 Objetivos de esta Sección

- Dominar técnicas de imputación estadística y algorítmica
- Implementar imputación múltiple y métodos ensemble
- Evaluar la calidad de las imputaciones
- Aplicar técnicas específicas según el tipo de variable
- Desarrollar pipelines robustos de imputación

## Dataset de Demostración

```python
import pandas as pd
import numpy as np
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer, KNNImputer, SimpleImputer
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import BayesianRidge
import matplotlib.pyplot as plt
import seaborn as sns

# Dataset de proyectos de consultoría con valores faltantes estratégicos
np.random.seed(42)

# Generar datos base
n_proyectos = 500

proyectos_completos = pd.DataFrame({
    'proyecto_id': [f'P{i:04d}' for i in range(1, n_proyectos + 1)],
    'cliente_tamaño': np.random.choice(['Pequeño', 'Mediano', 'Grande', 'Enterprise'], n_proyectos, p=[0.3, 0.3, 0.25, 0.15]),
    'industria': np.random.choice(['Tech', 'Finance', 'Healthcare', 'Manufacturing', 'Retail'], n_proyectos),
    'region': np.random.choice(['Norte', 'Sur', 'Este', 'Oeste', 'Centro'], n_proyectos),
    'duracion_meses': np.random.gamma(3, 2, n_proyectos),  # Distribución gamma para duración
    'equipo_size': np.random.poisson(6, n_proyectos) + 2,  # Tamaño de equipo con mínimo 2
})

# Generar variables dependientes de manera realista
def generar_presupuesto(row):
    base = 50000
    # El presupuesto depende del tamaño del cliente, industria y duración
    multiplicador_tamaño = {'Pequeño': 0.5, 'Mediano': 1.0, 'Grande': 2.0, 'Enterprise': 4.0}
    multiplicador_industria = {'Tech': 1.5, 'Finance': 2.0, 'Healthcare': 1.8, 'Manufacturing': 1.2, 'Retail': 1.0}
    
    presupuesto = (base * 
                  multiplicador_tamaño[row['cliente_tamaño']] * 
                  multiplicador_industria[row['industria']] * 
                  row['duracion_meses'] * 
                  (1 + 0.1 * row['equipo_size']))
    
    return presupuesto * (1 + np.random.normal(0, 0.3))  # Agregar ruido

proyectos_completos['presupuesto'] = proyectos_completos.apply(generar_presupuesto, axis=1)

# Generar satisfacción del cliente (correlacionada con presupuesto y duración)
proyectos_completos['satisfaccion_cliente'] = np.clip(
    8 + np.random.normal(0, 1, n_proyectos) - 
    0.001 * (proyectos_completos['presupuesto'] - proyectos_completos['presupuesto'].mean()) +
    0.2 * (5 - proyectos_completos['duracion_meses']),  # Proyectos más largos = menor satisfacción
    1, 10
)

# Generar ROI (correlacionado con satisfacción y eficiencia)
proyectos_completos['roi'] = np.clip(
    proyectos_completos['satisfaccion_cliente'] * 2 + 
    np.random.normal(0, 3, n_proyectos) +
    np.where(proyectos_completos['cliente_tamaño'] == 'Enterprise', 5, 0),
    -10, 50
)

# Introducir valores faltantes de manera realística
proyectos_con_faltantes = proyectos_completos.copy()

# 1. Presupuesto faltante para proyectos pequeños (confidencialidad)
mask_pequeños = proyectos_con_faltantes['cliente_tamaño'] == 'Pequeño'
proyectos_con_faltantes.loc[mask_pequeños, 'presupuesto'] = np.where(
    np.random.random(mask_pequeños.sum()) < 0.4, np.nan, 
    proyectos_con_faltantes.loc[mask_pequeños, 'presupuesto']
)

# 2. Satisfacción faltante para proyectos largos (abandono de encuesta)
mask_largos = proyectos_con_faltantes['duracion_meses'] > 8
proyectos_con_faltantes.loc[mask_largos, 'satisfaccion_cliente'] = np.where(
    np.random.random(mask_largos.sum()) < 0.25, np.nan,
    proyectos_con_faltantes.loc[mask_largos, 'satisfaccion_cliente']
)

# 3. ROI faltante para ciertas industrias (datos no disponibles)
mask_industrias = proyectos_con_faltantes['industria'].isin(['Healthcare', 'Manufacturing'])
proyectos_con_faltantes.loc[mask_industrias, 'roi'] = np.where(
    np.random.random(mask_industrias.sum()) < 0.3, np.nan,
    proyectos_con_faltantes.loc[mask_industrias, 'roi']
)

# 4. Faltantes aleatorios adicionales
for col in ['duracion_meses', 'equipo_size']:
    random_missing = np.random.random(n_proyectos) < 0.05
    proyectos_con_faltantes.loc[random_missing, col] = np.nan

print("Dataset de proyectos con valores faltantes:")
print(proyectos_con_faltantes.isna().sum())
print(f"Forma del dataset: {proyectos_con_faltantes.shape}")
```

## Técnicas de Imputación Estadística

### Imputación por Medidas de Tendencia Central

```python
def imputacion_tendencia_central(df, metodo='media'):
    """Imputación usando medidas de tendencia central."""
    df_imputado = df.copy()
    columnas_numericas = df_imputado.select_dtypes(include=[np.number]).columns
    
    estadisticas = {}
    
    for col in columnas_numericas:
        if df_imputado[col].isna().any():
            if metodo == 'media':
                valor_imputacion = df_imputado[col].mean()
            elif metodo == 'mediana':
                valor_imputacion = df_imputado[col].median()
            elif metodo == 'moda':
                valor_imputacion = df_imputado[col].mode().iloc[0] if not df_imputado[col].mode().empty else 0
            
            # Guardar estadística para reporte
            estadisticas[col] = {
                'metodo': metodo,
                'valor_imputado': valor_imputacion,
                'n_imputados': df_imputado[col].isna().sum()
            }
            
            df_imputado[col].fillna(valor_imputacion, inplace=True)
    
    return df_imputado, estadisticas

# Comparar diferentes métodos
metodos = ['media', 'mediana']
resultados_tendencia = {}

for metodo in metodos:
    df_result, stats = imputacion_tendencia_central(proyectos_con_faltantes, metodo)
    resultados_tendencia[metodo] = {'dataframe': df_result, 'estadisticas': stats}
    
    print(f"\nIMPUTACIÓN POR {metodo.upper()}:")
    for col, stat in stats.items():
        print(f"  {col}: {stat['n_imputados']} valores → {stat['valor_imputado']:.2f}")
```

### Imputación por Regresión

```python
def imputacion_regresion_simple(df, variable_objetivo, variables_predictoras):
    """Imputación usando regresión lineal simple."""
    from sklearn.linear_model import LinearRegression
    
    df_imputado = df.copy()
    
    # Identificar filas con y sin valores faltantes en la variable objetivo
    mask_completo = ~df_imputado[variable_objetivo].isna()
    mask_faltante = df_imputado[variable_objetivo].isna()
    
    if mask_faltante.sum() == 0:
        print(f"No hay valores faltantes en {variable_objetivo}")
        return df_imputado
    
    # Preparar datos para entrenamiento (solo filas completas)
    mask_entrenamiento = mask_completo & df_imputado[variables_predictoras].notna().all(axis=1)
    
    if mask_entrenamiento.sum() == 0:
        print(f"No hay suficientes datos completos para entrenar el modelo")
        return df_imputado
    
    X_train = df_imputado.loc[mask_entrenamiento, variables_predictoras]
    y_train = df_imputado.loc[mask_entrenamiento, variable_objetivo]
    
    # Entrenar modelo
    modelo = LinearRegression()
    modelo.fit(X_train, y_train)
    
    # Predecir valores faltantes
    mask_prediccion = mask_faltante & df_imputado[variables_predictoras].notna().all(axis=1)
    
    if mask_prediccion.sum() > 0:
        X_pred = df_imputado.loc[mask_prediccion, variables_predictoras]
        predicciones = modelo.predict(X_pred)
        df_imputado.loc[mask_prediccion, variable_objetivo] = predicciones
        
        print(f"Imputación por regresión - {variable_objetivo}:")
        print(f"  Valores imputados: {mask_prediccion.sum()}")
        print(f"  R² del modelo: {modelo.score(X_train, y_train):.3f}")
        print(f"  Coeficientes: {dict(zip(variables_predictoras, modelo.coef_))}")
    
    return df_imputado

# Ejemplo: Imputar presupuesto basado en otras variables
print("IMPUTACIÓN POR REGRESIÓN")
print("="*25)

df_regresion = imputacion_regresion_simple(
    proyectos_con_faltantes, 
    'presupuesto', 
    ['duracion_meses', 'equipo_size']
)
```

### Imputación Hot-Deck

```python
def imputacion_hot_deck(df, variable_objetivo, variables_estratificacion):
    """Imputación Hot-Deck: usar valores de registros similares."""
    df_imputado = df.copy()
    
    valores_imputados = 0
    
    # Para cada grupo estratificado
    for grupo, datos_grupo in df_imputado.groupby(variables_estratificacion):
        mask_faltantes = datos_grupo[variable_objetivo].isna()
        mask_disponibles = ~datos_grupo[variable_objetivo].isna()
        
        if mask_faltantes.any() and mask_disponibles.any():
            # Seleccionar aleatoriamente de valores disponibles en el grupo
            valores_disponibles = datos_grupo.loc[mask_disponibles, variable_objetivo].values
            n_faltantes = mask_faltantes.sum()
            
            # Muestreo con reemplazo de valores disponibles
            valores_imputacion = np.random.choice(valores_disponibles, n_faltantes, replace=True)
            
            # Asignar valores imputados
            indices_faltantes = datos_grupo[mask_faltantes].index
            df_imputado.loc[indices_faltantes, variable_objetivo] = valores_imputacion
            
            valores_imputados += n_faltantes
            print(f"Grupo {grupo}: {n_faltantes} valores imputados")
    
    print(f"\nTotal valores imputados con Hot-Deck: {valores_imputados}")
    return df_imputado

# Ejemplo: Imputar satisfacción por grupos de tamaño de cliente e industria
print("\nIMPUTACIÓN HOT-DECK")
print("="*20)

df_hotdeck = imputacion_hot_deck(
    proyectos_con_faltantes, 
    'satisfaccion_cliente', 
    ['cliente_tamaño', 'industria']
)
```

## Técnicas de Machine Learning

### Imputación K-Nearest Neighbors (KNN)

```python
def imputacion_knn_avanzada(df, n_neighbors=5, weights='distance'):
    """Imputación KNN con análisis detallado."""
    # Preparar datos numéricos
    columnas_numericas = df.select_dtypes(include=[np.number]).columns
    df_numerico = df[columnas_numericas].copy()
    
    # Aplicar KNN imputer
    imputer_knn = KNNImputer(n_neighbors=n_neighbors, weights=weights)
    datos_imputados = imputer_knn.fit_transform(df_numerico)
    
    # Crear DataFrame con resultados
    df_knn = pd.DataFrame(datos_imputados, columns=columnas_numericas, index=df.index)
    
    # Agregar columnas categóricas sin cambios
    columnas_categoricas = df.select_dtypes(exclude=[np.number]).columns
    for col in columnas_categoricas:
        df_knn[col] = df[col]
    
    # Análisis de imputaciones
    print(f"IMPUTACIÓN KNN (k={n_neighbors}, weights={weights})")
    print("="*40)
    
    for col in columnas_numericas:
        n_imputados = df[col].isna().sum()
        if n_imputados > 0:
            valores_originales = df[col].dropna()
            valores_imputados = df_knn.loc[df[col].isna(), col]
            
            print(f"\n{col}:")
            print(f"  Valores imputados: {n_imputados}")
            print(f"  Media original: {valores_originales.mean():.2f}")
            print(f"  Media imputada: {valores_imputados.mean():.2f}")
            print(f"  Std original: {valores_originales.std():.2f}")
            print(f"  Std imputada: {valores_imputados.std():.2f}")
    
    return df_knn

# Probar diferentes configuraciones de KNN
configuraciones_knn = [
    {'n_neighbors': 3, 'weights': 'uniform'},
    {'n_neighbors': 5, 'weights': 'distance'},
    {'n_neighbors': 10, 'weights': 'distance'}
]

resultados_knn = {}
for config in configuraciones_knn:
    nombre = f"KNN_k{config['n_neighbors']}_{config['weights']}"
    resultados_knn[nombre] = imputacion_knn_avanzada(proyectos_con_faltantes, **config)
```

### Imputación Iterativa (MICE)

```python
def imputacion_iterativa_avanzada(df, max_iter=10, random_state=42):
    """Imputación iterativa con análisis de convergencia."""
    # Preparar datos numéricos
    columnas_numericas = df.select_dtypes(include=[np.number]).columns
    df_numerico = df[columnas_numericas].copy()
    
    # Configurar imputer iterativo
    imputer_iterativo = IterativeImputer(
        estimator=BayesianRidge(),
        max_iter=max_iter,
        random_state=random_state,
        verbose=1
    )
    
    # Realizar imputación
    print("IMPUTACIÓN ITERATIVA (MICE)")
    print("="*30)
    datos_imputados = imputer_iterativo.fit_transform(df_numerico)
    
    # Crear DataFrame resultado
    df_mice = pd.DataFrame(datos_imputados, columns=columnas_numericas, index=df.index)
    
    # Agregar columnas categóricas
    columnas_categoricas = df.select_dtypes(exclude=[np.number]).columns
    for col in columnas_categoricas:
        df_mice[col] = df[col]
    
    # Análisis de resultados
    print(f"\nConvergencia después de {max_iter} iteraciones")
    print("Estadísticas de imputación:")
    
    for col in columnas_numericas:
        n_imputados = df[col].isna().sum()
        if n_imputados > 0:
            valores_originales = df[col].dropna()
            valores_imputados = df_mice.loc[df[col].isna(), col]
            
            # Evaluar plausibilidad de imputaciones
            percentil_5_orig = valores_originales.quantile(0.05)
            percentil_95_orig = valores_originales.quantile(0.95)
            fuera_rango = ((valores_imputados < percentil_5_orig) | 
                          (valores_imputados > percentil_95_orig)).sum()
            
            print(f"\n{col}:")
            print(f"  Valores imputados: {n_imputados}")
            print(f"  Fuera de rango plausible: {fuera_rango} ({fuera_rango/n_imputados*100:.1f}%)")
    
    return df_mice

df_mice = imputacion_iterativa_avanzada(proyectos_con_faltantes)
```

### Imputación con Random Forest

```python
def imputacion_random_forest(df):
    """Imputación usando Random Forest para cada variable."""
    df_rf = df.copy()
    columnas_numericas = df_rf.select_dtypes(include=[np.number]).columns
    
    print("IMPUTACIÓN CON RANDOM FOREST")
    print("="*32)
    
    for col_objetivo in columnas_numericas:
        if df_rf[col_objetivo].isna().any():
            print(f"\nImputando {col_objetivo}...")
            
            # Preparar variables predictoras (excluir la objetivo)
            cols_predictoras = [c for c in columnas_numericas if c != col_objetivo]
            
            # Dividir en datos completos e incompletos
            mask_completo = ~df_rf[col_objetivo].isna()
            mask_faltante = df_rf[col_objetivo].isna()
            
            # Filtrar filas con predictoras completas
            mask_entrenamiento = mask_completo & df_rf[cols_predictoras].notna().all(axis=1)
            mask_prediccion = mask_faltante & df_rf[cols_predictoras].notna().all(axis=1)
            
            if mask_entrenamiento.sum() > 0 and mask_prediccion.sum() > 0:
                # Entrenar modelo
                X_train = df_rf.loc[mask_entrenamiento, cols_predictoras]
                y_train = df_rf.loc[mask_entrenamiento, col_objetivo]
                
                rf = RandomForestRegressor(n_estimators=100, random_state=42)
                rf.fit(X_train, y_train)
                
                # Predecir valores faltantes
                X_pred = df_rf.loc[mask_prediccion, cols_predictoras]
                predicciones = rf.predict(X_pred)
                
                df_rf.loc[mask_prediccion, col_objetivo] = predicciones
                
                # Mostrar importancia de características
                importancias = dict(zip(cols_predictoras, rf.feature_importances_))
                importancias_ordenadas = sorted(importancias.items(), key=lambda x: x[1], reverse=True)
                
                print(f"  Valores imputados: {mask_prediccion.sum()}")
                print(f"  Score R²: {rf.score(X_train, y_train):.3f}")
                print(f"  Variables más importantes: {importancias_ordenadas[:3]}")
    
    return df_rf

df_rf = imputacion_random_forest(proyectos_con_faltantes)
```

## Imputación Múltiple

```python
def imputacion_multiple(df, n_imputaciones=5, metodo='mice'):
    """Realiza imputación múltiple y combina resultados."""
    imputaciones = []
    
    print(f"IMPUTACIÓN MÚLTIPLE ({n_imputaciones} imputaciones)")
    print("="*50)
    
    for i in range(n_imputaciones):
        print(f"Generando imputación {i+1}/{n_imputaciones}...")
        
        if metodo == 'mice':
            # Usar semilla diferente para cada imputación
            imputer = IterativeImputer(random_state=42+i, max_iter=5, verbose=0)
        elif metodo == 'knn':
            imputer = KNNImputer(n_neighbors=5)
        
        # Solo variables numéricas
        columnas_numericas = df.select_dtypes(include=[np.number]).columns
        df_numerico = df[columnas_numericas]
        
        datos_imputados = imputer.fit_transform(df_numerico)
        df_imputado = pd.DataFrame(datos_imputados, columns=columnas_numericas, index=df.index)
        
        # Agregar columnas categóricas
        for col in df.select_dtypes(exclude=[np.number]).columns:
            df_imputado[col] = df[col]
        
        imputaciones.append(df_imputado)
    
    # Combinar imputaciones (promedio para numéricas, moda para categóricas)
    df_combinado = df.copy()
    
    for col in df.columns:
        if df[col].isna().any():
            if col in columnas_numericas:
                # Promedio de las imputaciones
                valores_imputados = np.mean([imp.loc[df[col].isna(), col] for imp in imputaciones], axis=0)
                df_combinado.loc[df[col].isna(), col] = valores_imputados
            else:
                # Moda para categóricas (usar primera imputación por simplicidad)
                df_combinado.loc[df[col].isna(), col] = imputaciones[0].loc[df[col].isna(), col]
    
    # Análisis de variabilidad entre imputaciones
    print("\nAnálisis de variabilidad entre imputaciones:")
    for col in columnas_numericas:
        if df[col].isna().any():
            # Calcular desviación estándar de las imputaciones
            matriz_imputaciones = np.array([imp.loc[df[col].isna(), col] for imp in imputaciones])
            std_imputaciones = np.std(matriz_imputaciones, axis=0)
            std_promedio = np.mean(std_imputaciones)
            
            print(f"  {col}: Std promedio entre imputaciones = {std_promedio:.3f}")
    
    return df_combinado, imputaciones

df_multiple, lista_imputaciones = imputacion_multiple(proyectos_con_faltantes, n_imputaciones=3)
```

## Evaluación de Calidad de Imputación

```python
def evaluar_calidad_imputacion(df_original, df_imputado, df_verdadero=None):
    """Evalúa la calidad de las imputaciones realizadas."""
    evaluacion = {}
    
    print("EVALUACIÓN DE CALIDAD DE IMPUTACIÓN")
    print("="*40)
    
    columnas_numericas = df_original.select_dtypes(include=[np.number]).columns
    
    for col in columnas_numericas:
        if df_original[col].isna().any():
            evaluacion[col] = {}
            
            # Datos originales (sin faltantes)
            valores_reales = df_original[col].dropna()
            
            # Valores imputados
            mask_imputados = df_original[col].isna()
            valores_imputados = df_imputado.loc[mask_imputados, col]
            
            # 1. Distribución estadística
            evaluacion[col]['diferencia_media'] = abs(valores_imputados.mean() - valores_reales.mean())
            evaluacion[col]['diferencia_std'] = abs(valores_imputados.std() - valores_reales.std())
            
            # 2. Test de Kolmogorov-Smirnov (distribución similar)
            from scipy.stats import ks_2samp
            ks_stat, ks_pvalue = ks_2samp(valores_reales, valores_imputados)
            evaluacion[col]['ks_statistic'] = ks_stat
            evaluacion[col]['ks_pvalue'] = ks_pvalue
            
            # 3. Rango plausible
            q5, q95 = valores_reales.quantile([0.05, 0.95])
            fuera_rango = ((valores_imputados < q5) | (valores_imputados > q95)).sum()
            evaluacion[col]['pct_fuera_rango'] = fuera_rango / len(valores_imputados) * 100
            
            # 4. Si tenemos valores verdaderos, calcular error
            if df_verdadero is not None and col in df_verdadero.columns:
                valores_verdaderos = df_verdadero.loc[mask_imputados, col]
                mse = np.mean((valores_imputados - valores_verdaderos) ** 2)
                mae = np.mean(abs(valores_imputados - valores_verdaderos))
                evaluacion[col]['mse'] = mse
                evaluacion[col]['mae'] = mae
            
            print(f"\n{col}:")
            print(f"  Diferencia de media: {evaluacion[col]['diferencia_media']:.3f}")
            print(f"  Diferencia de std: {evaluacion[col]['diferencia_std']:.3f}")
            print(f"  KS p-value: {evaluacion[col]['ks_pvalue']:.3f}")
            print(f"  % fuera de rango: {evaluacion[col]['pct_fuera_rango']:.1f}%")
            
            if 'mse' in evaluacion[col]:
                print(f"  MSE: {evaluacion[col]['mse']:.3f}")
                print(f"  MAE: {evaluacion[col]['mae']:.3f}")
    
    return evaluacion

# Evaluar diferentes métodos
metodos_comparar = {
    'Media': resultados_tendencia['media']['dataframe'],
    'KNN': resultados_knn['KNN_k5_distance'],
    'MICE': df_mice,
    'Random Forest': df_rf,
    'Múltiple': df_multiple
}

print("\nCOMPARACIÓN DE MÉTODOS DE IMPUTACIÓN")
print("="*45)

evaluaciones = {}
for nombre, df_metodo in metodos_comparar.items():
    print(f"\n--- {nombre} ---")
    evaluaciones[nombre] = evaluar_calidad_imputacion(
        proyectos_con_faltantes, 
        df_metodo, 
        proyectos_completos  # Usamos los datos originales como "verdad"
    )
```

## Casos Prácticos Especializados

### Caso 1: Imputación de Series Temporales

```python
def imputacion_series_temporales(df_ts, columna_fecha, columna_valor):
    """Imputación especializada para series temporales."""
    df_ts = df_ts.copy()
    df_ts[columna_fecha] = pd.to_datetime(df_ts[columna_fecha])
    df_ts = df_ts.sort_values(columna_fecha)
    
    print("IMPUTACIÓN DE SERIES TEMPORALES")
    print("="*35)
    
    # 1. Interpolación lineal
    df_ts[f'{columna_valor}_interpolado'] = df_ts[columna_valor].interpolate(method='linear')
    
    # 2. Interpolación por spline
    df_ts[f'{columna_valor}_spline'] = df_ts[columna_valor].interpolate(method='spline', order=2)
    
    # 3. Forward fill y backward fill
    df_ts[f'{columna_valor}_ffill'] = df_ts[columna_valor].fillna(method='ffill')
    df_ts[f'{columna_valor}_bfill'] = df_ts[columna_valor].fillna(method='bfill')
    
    # 4. Media móvil
    ventana = min(7, len(df_ts) // 4)  # Ventana adaptativa
    df_ts[f'{columna_valor}_media_movil'] = df_ts[columna_valor].fillna(
        df_ts[columna_valor].rolling(window=ventana, center=True).mean()
    )
    
    return df_ts

# Crear ejemplo de serie temporal con faltantes
fechas_ts = pd.date_range('2023-01-01', '2023-12-31', freq='D')
ventas_ts = pd.DataFrame({
    'fecha': fechas_ts,
    'ventas': np.random.normal(1000, 200, len(fechas_ts))
})

# Introducir faltantes aleatorios
mask_faltantes = np.random.random(len(ventas_ts)) < 0.1
ventas_ts.loc[mask_faltantes, 'ventas'] = np.nan

ventas_imputadas = imputacion_series_temporales(ventas_ts, 'fecha', 'ventas')
print(f"Serie temporal: {len(ventas_ts)} puntos, {mask_faltantes.sum()} faltantes")
```

### Caso 2: Imputación Multimodal

```python
def imputacion_multimodal(df, variables_relacionadas):
    """Imputación considerando múltiples variables relacionadas simultáneamente."""
    df_multi = df.copy()
    
    print("IMPUTACIÓN MULTIMODAL")
    print("="*25)
    
    # Identificar patrones de faltantes
    patron_faltantes = df[variables_relacionadas].isna()
    patrones_unicos = patron_faltantes.drop_duplicates()
    
    print(f"Patrones de faltantes encontrados: {len(patrones_unicos)}")
    
    for idx, patron in patrones_unicos.iterrows():
        # Identificar filas con este patrón
        mask_patron = (patron_faltantes == patron).all(axis=1)
        n_filas = mask_patron.sum()
        
        if n_filas > 0:
            variables_faltantes = patron[patron].index.tolist()
            variables_disponibles = patron[~patron].index.tolist()
            
            print(f"\nPatrón: {variables_faltantes} faltantes, {variables_disponibles} disponibles")
            print(f"Afecta a {n_filas} filas")
            
            if variables_disponibles and variables_faltantes:
                # Usar regresión múltiple para imputar
                filas_completas = ~df[variables_relacionadas].isna().any(axis=1)
                
                if filas_completas.sum() > 10:  # Suficientes datos para entrenar
                    X_train = df.loc[filas_completas, variables_disponibles]
                    
                    for var_objetivo in variables_faltantes:
                        y_train = df.loc[filas_completas, var_objetivo]
                        
                        # Entrenar modelo
                        from sklearn.linear_model import LinearRegression
                        modelo = LinearRegression()
                        modelo.fit(X_train, y_train)
                        
                        # Predecir para filas con este patrón
                        X_pred = df_multi.loc[mask_patron, variables_disponibles]
                        if not X_pred.empty:
                            predicciones = modelo.predict(X_pred)
                            df_multi.loc[mask_patron, var_objetivo] = predicciones
                            
                            print(f"  {var_objetivo}: {len(predicciones)} valores imputados")
    
    return df_multi

# Aplicar imputación multimodal
variables_proyecto = ['presupuesto', 'duracion_meses', 'satisfaccion_cliente', 'roi']
df_multimodal = imputacion_multimodal(proyectos_con_faltantes, variables_proyecto)
```

## Ejercicios Prácticos

### Ejercicio 1: Comparación de Métodos
```python
# TODO: Implementa y compara los siguientes métodos de imputación:
# 1. Imputación por mediana agrupada por industria
# 2. KNN con k=3 vs k=10
# 3. Random Forest vs Gradient Boosting
# 4. Evalúa cuál preserva mejor las correlaciones originales

# Tu solución aquí:
```

### Ejercicio 2: Imputación Robusta
```python
# TODO: Desarrolla un método de imputación que:
# 1. Detecte outliers antes de imputar
# 2. Use diferentes estrategias según el % de faltantes por variable
# 3. Valide la plausibilidad de las imputaciones
# 4. Genere un reporte de confianza para cada valor imputado

# Tu solución aquí:
```

### Ejercicio 3: Pipeline de Imputación
```python
# TODO: Crea un pipeline completo que:
# 1. Analice patrones de faltantes
# 2. Seleccione automáticamente la mejor estrategia por variable
# 3. Aplique imputación múltiple si es necesario
# 4. Valide los resultados y genere métricas de calidad

# Tu solución aquí:
```

## Mejores Prácticas

!!! tip "Guía para Imputación Efectiva"
    1. **Entiende el mecanismo**: ¿Por qué faltan los datos?
    2. **Preserva relaciones**: Mantén correlaciones y distribuciones
    3. **Valida resultados**: Compara distribuciones antes/después
    4. **Documenta decisiones**: Registra qué método usaste y por qué
    5. **Considera incertidumbre**: Usa imputación múltiple cuando sea apropiado

### Checklist de Imputación

```python
def checklist_imputacion(df_original, df_imputado):
    """Checklist para validar calidad de imputación."""
    checks = {}
    
    # 1. Completitud
    checks['completitud'] = df_imputado.isna().sum().sum() == 0
    
    # 2. Preservación de distribuciones
    columnas_numericas = df_original.select_dtypes(include=[np.number]).columns
    diferencias_media = []
    
    for col in columnas_numericas:
        if not df_original[col].isna().all():
            media_orig = df_original[col].mean()
            media_imput = df_imputado[col].mean()
            diferencia_pct = abs(media_imput - media_orig) / media_orig * 100
            diferencias_media.append(diferencia_pct)
    
    checks['preservacion_media'] = np.mean(diferencias_media) < 10  # <10% cambio
    
    # 3. Valores plausibles
    valores_extremos = 0
    for col in columnas_numericas:
        if df_original[col].isna().any():
            valores_orig = df_original[col].dropna()
            q1, q99 = valores_orig.quantile([0.01, 0.99])
            
            mask_imputados = df_original[col].isna()
            valores_imputados = df_imputado.loc[mask_imputados, col]
            
            extremos = ((valores_imputados < q1) | (valores_imputados > q99)).sum()
            valores_extremos += extremos
    
    checks['valores_plausibles'] = valores_extremos == 0
    
    # 4. Correlaciones preservadas
    if len(columnas_numericas) > 1:
        corr_orig = df_original[columnas_numericas].corr()
        corr_imput = df_imputado[columnas_numericas].corr()
        
        # Calcular diferencia promedio en correlaciones
        mask_triangular = np.triu(np.ones_like(corr_orig), k=1).astype(bool)
        diff_corr = abs(corr_orig.values[mask_triangular] - corr_imput.values[mask_triangular])
        checks['correlaciones_preservadas'] = np.mean(diff_corr) < 0.1
    
    print("CHECKLIST DE CALIDAD DE IMPUTACIÓN")
    print("="*40)
    for check, passed in checks.items():
        status = "✓" if passed else "✗"
        print(f"{status} {check.replace('_', ' ').title()}")
    
    score_calidad = sum(checks.values()) / len(checks) * 100
    print(f"\nScore de Calidad: {score_calidad:.0f}%")
    
    return checks

# Evaluar la mejor imputación
mejor_metodo = df_mice  # Por ejemplo
checks_calidad = checklist_imputacion(proyectos_con_faltantes, mejor_metodo)
```

## Resumen

Las técnicas avanzadas de imputación te permiten:

- ✅ Preservar información valiosa en lugar de eliminar datos
- ✅ Mantener relaciones estadísticas entre variables
- ✅ Adaptar la estrategia al tipo de dato y contexto
- ✅ Cuantificar la incertidumbre de las estimaciones
- ✅ Crear datasets completos para análisis robustos

**Próximo paso**: Continúa con los [Ejercicios Prácticos](../ejercicios/ejercicio-1-proyectos.md) para aplicar todos los conceptos aprendidos en casos reales de consultoría.