#!/usr/bin/env python3
"""
Demo 01: Filtrado y Selección Avanzada de Datos
==================================================

Este demo muestra técnicas avanzadas de filtrado y selección en Pandas,
diseñadas específicamente para casos de uso en consultoría.

Objetivos:
- Dominar filtros complejos con múltiples condiciones
- Utilizar operadores lógicos efectivamente
- Aplicar métodos de selección avanzada (loc, iloc, query)
- Combinar técnicas para análisis de datos eficiente

Autor: Equipo Meridian Consulting
Fecha: 2025
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURACIÓN INICIAL
# ============================================================================

def configurar_pandas():
    """Configura Pandas para mejor visualización."""
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', 50)
    print("✓ Pandas configurado para visualización óptima")

# ============================================================================
# GENERACIÓN DE DATOS DE EJEMPLO
# ============================================================================

def crear_datos_demo():
    """Crea un dataset de proyectos para demostración."""
    np.random.seed(42)
    
    # Generar datos realistas de proyectos de consultoría
    n_proyectos = 50
    
    proyectos = pd.DataFrame({
        'proyecto_id': [f'P{i:03d}' for i in range(1, n_proyectos + 1)],
        'cliente': np.random.choice(['Tech Corp', 'Finance Ltd', 'Health Systems', 'Retail Plus', 'Manufacturing Co'], n_proyectos),
        'tipo_proyecto': np.random.choice(['Estratégico', 'Operacional', 'Digital', 'Compliance', 'Innovación'], n_proyectos),
        'region': np.random.choice(['Norte', 'Sur', 'Este', 'Oeste', 'Centro'], n_proyectos),
        'presupuesto': np.random.normal(150000, 50000, n_proyectos),
        'gastado': np.random.normal(140000, 60000, n_proyectos),
        'equipo_size': np.random.randint(3, 12, n_proyectos),
        'duracion_meses': np.random.gamma(3, 2, n_proyectos),
        'satisfaccion': np.random.normal(7.5, 1.5, n_proyectos),
        'estado': np.random.choice(['Planificación', 'En Progreso', 'Completado', 'En Pausa'], n_proyectos, p=[0.2, 0.4, 0.3, 0.1]),
        'prioridad': np.random.choice(['Alta', 'Media', 'Baja'], n_proyectos, p=[0.3, 0.5, 0.2]),
        'fecha_inicio': pd.date_range('2024-01-01', periods=n_proyectos, freq='W')
    })
    
    # Asegurar que los valores sean realistas
    proyectos['presupuesto'] = np.abs(proyectos['presupuesto'])
    proyectos['gastado'] = np.abs(proyectos['gastado'])
    proyectos['satisfaccion'] = np.clip(proyectos['satisfaccion'], 1, 10)
    
    print(f"✓ Dataset creado: {len(proyectos)} proyectos")
    print(f"  Columnas: {list(proyectos.columns)}")
    return proyectos

# ============================================================================
# DEMO 1: FILTROS BÁSICOS VS AVANZADOS
# ============================================================================

def demo_filtros_basicos_vs_avanzados(df):
    """Compara filtros básicos con técnicas avanzadas."""
    print("\n" + "="*60)
    print("DEMO 1: FILTROS BÁSICOS VS AVANZADOS")
    print("="*60)
    
    # Filtro básico
    print("\n1. FILTRO BÁSICO:")
    print("-" * 20)
    filtro_basico = df[df['presupuesto'] > 150000]
    print(f"Proyectos con presupuesto > 150K: {len(filtro_basico)}")
    
    # Filtros múltiples - método tradicional
    print("\n2. MÚLTIPLES CONDICIONES (método tradicional):")
    print("-" * 50)
    filtro_multiple = df[
        (df['presupuesto'] > 150000) & 
        (df['estado'] == 'En Progreso') & 
        (df['satisfaccion'] >= 7.0)
    ]
    print(f"Proyectos grandes, en progreso y satisfactorios: {len(filtro_multiple)}")
    
    # Usando query() - más legible
    print("\n3. USANDO QUERY() - MÁS LEGIBLE:")
    print("-" * 35)
    filtro_query = df.query('presupuesto > 150000 and estado == "En Progreso" and satisfaccion >= 7.0')
    print(f"Mismo filtro con query(): {len(filtro_query)}")
    print("✓ Ambos métodos producen el mismo resultado")
    
    # Mostrar algunos resultados
    print("\nPrimeros 3 proyectos que cumplen los criterios:")
    print(filtro_multiple[['proyecto_id', 'cliente', 'presupuesto', 'estado', 'satisfaccion']].head(3))

# ============================================================================
# DEMO 2: OPERADORES LÓGICOS AVANZADOS
# ============================================================================

def demo_operadores_logicos(df):
    """Demuestra uso avanzado de operadores lógicos."""
    print("\n" + "="*60)
    print("DEMO 2: OPERADORES LÓGICOS AVANZADOS")
    print("="*60)
    
    # Operador OR
    print("\n1. OPERADOR OR (|):")
    print("-" * 20)
    filtro_or = df[(df['prioridad'] == 'Alta') | (df['presupuesto'] > 200000)]
    print(f"Proyectos de alta prioridad O alto presupuesto: {len(filtro_or)}")
    
    # Operador NOT
    print("\n2. OPERADOR NOT (~):")
    print("-" * 20)
    filtro_not = df[~(df['estado'] == 'Completado')]
    print(f"Proyectos NO completados: {len(filtro_not)}")
    
    # Combinación compleja
    print("\n3. COMBINACIÓN COMPLEJA:")
    print("-" * 25)
    filtro_complejo = df[
        ((df['tipo_proyecto'] == 'Estratégico') | (df['tipo_proyecto'] == 'Digital')) &
        (df['equipo_size'] >= 5) &
        ~(df['estado'] == 'En Pausa')
    ]
    print(f"Proyectos estratégicos/digitales, equipos grandes, activos: {len(filtro_complejo)}")
    
    # Usando isin() para múltiples valores
    print("\n4. USANDO ISIN() PARA MÚLTIPLES VALUES:")
    print("-" * 40)
    tipos_importantes = ['Estratégico', 'Digital', 'Innovación']
    filtro_isin = df[df['tipo_proyecto'].isin(tipos_importantes)]
    print(f"Proyectos de tipos importantes: {len(filtro_isin)}")
    print(f"Tipos incluidos: {tipos_importantes}")

# ============================================================================
# DEMO 3: SELECCIÓN AVANZADA CON LOC E ILOC
# ============================================================================

def demo_seleccion_avanzada(df):
    """Demuestra técnicas avanzadas de selección."""
    print("\n" + "="*60)
    print("DEMO 3: SELECCIÓN AVANZADA CON LOC E ILOC")
    print("="*60)
    
    # Configurar índice para demostración
    df_indexed = df.set_index('proyecto_id')
    
    # Selección específica con loc
    print("\n1. SELECCIÓN ESPECÍFICA CON LOC:")
    print("-" * 35)
    proyectos_especificos = ['P001', 'P005', 'P010']
    columnas_interes = ['cliente', 'presupuesto', 'estado', 'satisfaccion']
    
    seleccion_loc = df_indexed.loc[proyectos_especificos, columnas_interes]
    print("Proyectos específicos con columnas de interés:")
    print(seleccion_loc)
    
    # Selección condicional con loc
    print("\n2. SELECCIÓN CONDICIONAL CON LOC:")
    print("-" * 38)
    seleccion_condicional = df_indexed.loc[
        df_indexed['presupuesto'] > 180000, 
        ['cliente', 'tipo_proyecto', 'presupuesto', 'satisfaccion']
    ]
    print(f"Proyectos de alto presupuesto (>180K): {len(seleccion_condicional)}")
    print(seleccion_condicional.head())
    
    # Selección por posición con iloc
    print("\n3. SELECCIÓN POR POSICIÓN CON ILOC:")
    print("-" * 38)
    # Primeros 5 proyectos, columnas 1-4
    seleccion_iloc = df.iloc[0:5, 1:5]
    print("Primeros 5 proyectos, columnas 1-4:")
    print(seleccion_iloc)
    
    # Selección aleatoria
    print("\n4. SELECCIÓN ALEATORIA:")
    print("-" * 25)
    indices_aleatorios = np.random.choice(len(df), 3, replace=False)
    seleccion_aleatoria = df.iloc[indices_aleatorios, [0, 1, 4, 8]]
    print("3 proyectos aleatorios:")
    print(seleccion_aleatoria)

# ============================================================================
# DEMO 4: FILTRADO POR RANGOS Y PATRONES
# ============================================================================

def demo_filtrado_rangos_patrones(df):
    """Demuestra filtrado por rangos y patrones de texto."""
    print("\n" + "="*60)
    print("DEMO 4: FILTRADO POR RANGOS Y PATRONES")
    print("="*60)
    
    # Filtrado por rangos usando between()
    print("\n1. FILTRADO POR RANGOS CON BETWEEN():")
    print("-" * 40)
    rango_presupuesto = df[df['presupuesto'].between(120000, 180000)]
    print(f"Proyectos con presupuesto entre 120K-180K: {len(rango_presupuesto)}")
    
    # Filtrado por percentiles
    print("\n2. FILTRADO POR PERCENTILES:")
    print("-" * 30)
    p25 = df['presupuesto'].quantile(0.25)
    p75 = df['presupuesto'].quantile(0.75)
    proyectos_top_quartile = df[df['presupuesto'] >= p75]
    print(f"Percentil 75 de presupuesto: ${p75:,.0f}")
    print(f"Proyectos en quartil superior: {len(proyectos_top_quartile)}")
    
    # Filtrado por patrones de texto
    print("\n3. FILTRADO POR PATRONES DE TEXTO:")
    print("-" * 38)
    # Clientes que contienen "Tech" o "Corp"
    filtro_texto = df[df['cliente'].str.contains('Tech|Corp', case=False, na=False)]
    print(f"Clientes con 'Tech' o 'Corp' en el nombre: {len(filtro_texto)}")
    print("Clientes encontrados:")
    print(filtro_texto['cliente'].unique())
    
    # Proyectos que empiezan con fechas específicas
    print("\n4. FILTRADO POR FECHAS:")
    print("-" * 25)
    # Proyectos que iniciaron en el primer trimestre
    primer_trimestre = df[df['fecha_inicio'].dt.quarter == 1]
    print(f"Proyectos iniciados en Q1: {len(primer_trimestre)}")

# ============================================================================
# DEMO 5: CASOS PRÁCTICOS DE CONSULTORÍA
# ============================================================================

def demo_casos_practicos(df):
    """Casos prácticos específicos de consultoría."""
    print("\n" + "="*60)
    print("DEMO 5: CASOS PRÁCTICOS DE CONSULTORÍA")
    print("="*60)
    
    # Caso 1: Identificar proyectos de riesgo
    print("\n1. IDENTIFICACIÓN DE PROYECTOS DE RIESGO:")
    print("-" * 45)
    proyectos_riesgo = df[
        ((df['gastado'] / df['presupuesto']) > 1.1) |  # Sobrecosto >10%
        (df['satisfaccion'] < 6.0) |                   # Baja satisfacción
        ((df['estado'] == 'En Progreso') & (df['duracion_meses'] > 8))  # Muy largos
    ]
    print(f"Proyectos identificados como de riesgo: {len(proyectos_riesgo)}")
    
    if len(proyectos_riesgo) > 0:
        print("\nRazones de riesgo por proyecto:")
        for idx, row in proyectos_riesgo.head().iterrows():
            razones = []
            sobrecosto = (row['gastado'] / row['presupuesto']) > 1.1
            baja_satisfaccion = row['satisfaccion'] < 6.0
            muy_largo = (row['estado'] == 'En Progreso') and (row['duracion_meses'] > 8)
            
            if sobrecosto:
                razones.append("Sobrecosto")
            if baja_satisfaccion:
                razones.append("Baja satisfacción")
            if muy_largo:
                razones.append("Duración excesiva")
            
            print(f"  {row['proyecto_id']}: {', '.join(razones)}")
    
    # Caso 2: Análisis de portafolio por cliente
    print("\n2. ANÁLISIS DE PORTAFOLIO POR CLIENTE:")
    print("-" * 40)
    # Clientes con múltiples proyectos activos
    proyectos_activos = df[df['estado'].isin(['En Progreso', 'Planificación'])]
    portafolio_cliente = proyectos_activos.groupby('cliente').agg({
        'proyecto_id': 'count',
        'presupuesto': 'sum',
        'satisfaccion': 'mean'
    }).round(2)
    portafolio_cliente.columns = ['Num_Proyectos', 'Presupuesto_Total', 'Satisfaccion_Promedio']
    
    # Filtrar clientes con múltiples proyectos
    clientes_multiples = portafolio_cliente[portafolio_cliente['Num_Proyectos'] > 1]
    print("Clientes con múltiples proyectos activos:")
    print(clientes_multiples)
    
    # Caso 3: Oportunidades de crecimiento
    print("\n3. IDENTIFICACIÓN DE OPORTUNIDADES:")
    print("-" * 40)
    # Clientes satisfechos con proyectos pequeños
    oportunidades = df[
        (df['satisfaccion'] >= 8.0) &
        (df['presupuesto'] < df['presupuesto'].median()) &
        (df['estado'] == 'Completado')
    ]
    print(f"Clientes satisfechos con proyectos pequeños (oportunidades de upsell): {len(oportunidades)}")
    
    if len(oportunidades) > 0:
        print("\nTop oportunidades:")
        oportunidades_resumen = oportunidades.groupby('cliente').agg({
            'satisfaccion': 'mean',
            'presupuesto': 'mean',
            'proyecto_id': 'count'
        }).round(2).sort_values('satisfaccion', ascending=False)
        print(oportunidades_resumen.head())

# ============================================================================
# DEMO 6: OPTIMIZACIÓN Y MEJORES PRÁCTICAS
# ============================================================================

def demo_optimizacion(df):
    """Demuestra técnicas de optimización para filtrado."""
    print("\n" + "="*60)
    print("DEMO 6: OPTIMIZACIÓN Y MEJORES PRÁCTICAS")
    print("="*60)
    
    import time
    
    # Comparar rendimiento de diferentes métodos
    print("\n1. COMPARACIÓN DE RENDIMIENTO:")
    print("-" * 35)
    
    # Crear dataset más grande para la comparación
    df_grande = pd.concat([df] * 100, ignore_index=True)
    print(f"Dataset expandido: {len(df_grande)} filas")
    
    # Método 1: Filtrado tradicional
    start_time = time.time()
    resultado1 = df_grande[(df_grande['presupuesto'] > 150000) & (df_grande['estado'] == 'En Progreso')]
    tiempo1 = time.time() - start_time
    
    # Método 2: Query
    start_time = time.time()
    resultado2 = df_grande.query('presupuesto > 150000 and estado == "En Progreso"')
    tiempo2 = time.time() - start_time
    
    print(f"Filtrado tradicional: {tiempo1:.4f} segundos")
    print(f"Método query():      {tiempo2:.4f} segundos")
    print(f"Diferencia:          {abs(tiempo1-tiempo2):.4f} segundos")
    print(f"Resultados iguales:  {len(resultado1) == len(resultado2)}")
    
    # Mejores prácticas
    print("\n2. MEJORES PRÁCTICAS:")
    print("-" * 25)
    
    mejores_practicas = [
        "✓ Usar paréntesis en condiciones múltiples",
        "✓ Preferir query() para filtros complejos legibles",
        "✓ Usar isin() para múltiples valores en lugar de OR múltiples",
        "✓ Considerar el orden de las condiciones (más selectivas primero)",
        "✓ Usar copy() cuando modifiques subconjuntos",
        "✓ Aprovechar índices para selecciones frecuentes"
    ]
    
    for practica in mejores_practicas:
        print(f"  {practica}")
    
    # Ejemplo de código optimizado
    print("\n3. EJEMPLO DE CÓDIGO OPTIMIZADO:")
    print("-" * 35)
    
    def filtrar_proyectos_riesgo_optimizado(df):
        """Función optimizada para filtrar proyectos de riesgo."""
        # Condiciones organizadas por selectividad
        condiciones = (
            (df['estado'].isin(['En Progreso', 'Planificación'])) &  # Más selectivo primero
            (df['satisfaccion'] < 7.0) &
            (df['presupuesto'] > 100000)
        )
        return df[condiciones].copy()  # copy() para evitar warnings
    
    proyectos_riesgo_opt = filtrar_proyectos_riesgo_optimizado(df)
    print(f"Proyectos de riesgo identificados: {len(proyectos_riesgo_opt)}")

# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Función principal que ejecuta todas las demostraciones."""
    print("🚀 DEMO: FILTRADO Y SELECCIÓN AVANZADA EN PANDAS")
    print("=" * 60)
    print("Meridian Consulting - Sesión 08")
    print("Fundamentos de Pandas II: Transformación y Análisis de Datos")
    
    # Configuración inicial
    configurar_pandas()
    
    # Crear datos de demostración
    df = crear_datos_demo()
    
    # Mostrar información básica del dataset
    print(f"\n📊 INFORMACIÓN DEL DATASET:")
    print(f"   Filas: {len(df)}")
    print(f"   Columnas: {len(df.columns)}")
    print(f"   Tipos de datos: {df.dtypes.nunique()} únicos")
    
    # Ejecutar todas las demostraciones
    demo_filtros_basicos_vs_avanzados(df)
    demo_operadores_logicos(df)
    demo_seleccion_avanzada(df)
    demo_filtrado_rangos_patrones(df)
    demo_casos_practicos(df)
    demo_optimizacion(df)
    
    # Resumen final
    print("\n" + "="*60)
    print("🎯 RESUMEN DE TÉCNICAS DEMOSTRADAS")
    print("="*60)
    
    tecnicas = [
        "1. Filtros múltiples con operadores lógicos (&, |, ~)",
        "2. Método query() para sintaxis legible tipo SQL",
        "3. Selección precisa con loc e iloc",
        "4. Filtrado por rangos con between()",
        "5. Búsqueda de patrones de texto con str.contains()",
        "6. Filtrado por fechas y componentes temporales",
        "7. Análisis de casos prácticos de consultoría",
        "8. Optimización y mejores prácticas"
    ]
    
    for tecnica in tecnicas:
        print(f"   ✓ {tecnica}")
    
    print(f"\n🏆 ¡Demo completado exitosamente!")
    print(f"   Próximo paso: Aplicar estas técnicas en ejercicios prácticos")

if __name__ == "__main__":
    main()