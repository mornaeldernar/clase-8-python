# Modificación de Datos Existentes

## Introducción

La modificación de datos existentes es una tarea común en el análisis de datos. En consultoría, frecuentemente necesitas corregir errores, estandarizar formatos, actualizar valores basados en nuevos criterios, o transformar datos para mejorar su calidad y utilidad.

## 🎯 Objetivos de esta Sección

- Modificar valores en columnas existentes de manera eficiente
- Aplicar transformaciones condicionales masivas
- Estandarizar formatos de datos
- Corregir inconsistencias en los datos
- Actualizar datos basados en reglas de negocio

## Datos de Ejemplo

```python
import pandas as pd
import numpy as np
import re

# Dataset con problemas comunes de calidad de datos
empleados_sucio = pd.DataFrame({
    'empleado_id': ['E001', 'E002', 'E003', 'E004', 'E005', 'E006'],
    'nombre': ['Ana García  ', 'carlos lopez', 'MARÍA RODRÍGUEZ', 'Juan Pérez', 'laura  martin', 'Pedro Sánchez'],
    'email': ['ana.garcia@company.com', 'CARLOS.LOPEZ@COMPANY.COM', 'maria.rodriguez@company.com', 
              'juan.perez@company.COM', 'laura.martin@company.com', 'pedro.sanchez@COMPANY.com'],
    'departamento': ['Consultoría', 'It', 'CONSULTORIA', 'Finanzas', 'IT', 'consultoría'],
    'salario': ['65,000', '70000', '62000', '75,000', '68000', '67000'],
    'fecha_ingreso': ['15/01/2020', '2021-03-10', '10-02-2022', '2019/12/05', '2023-01-15', '2020/08/20'],
    'telefono': ['91-555-0123', '91 555 0124', '915550125', '91.555.0126', '91-555-0127', '915550128'],
    'estado': ['activo', 'ACTIVO', 'Activo', 'inactivo', 'INACTIVO', 'Activo']
})

print("Datos originales con problemas de calidad:")
print(empleados_sucio)
```

## Limpieza y Estandarización de Texto

### Normalización de Nombres

```python
# Crear una copia para trabajar
empleados_limpio = empleados_sucio.copy()

# Limpiar espacios en blanco y estandarizar capitalización
empleados_limpio['nombre'] = empleados_limpio['nombre'].str.strip()  # Quitar espacios
empleados_limpio['nombre'] = empleados_limpio['nombre'].str.title()  # Capitalización correcta

print("Nombres después de limpieza:")
print(empleados_limpio[['empleado_id', 'nombre']])
```

### Estandarización de Emails

```python
# Convertir emails a minúsculas
empleados_limpio['email'] = empleados_limpio['email'].str.lower()

print("Emails estandarizados:")
print(empleados_limpio[['empleado_id', 'email']])
```

### Normalización de Departamentos

```python
# Crear diccionario de mapeo para departamentos
mapeo_departamentos = {
    'consultoría': 'Consultoría',
    'CONSULTORIA': 'Consultoría',
    'it': 'IT',
    'IT': 'IT',
    'finanzas': 'Finanzas'
}

# Aplicar mapeo después de normalizar
empleados_limpio['departamento_normalizado'] = (
    empleados_limpio['departamento']
    .str.lower()
    .str.strip()
    .replace({
        'consultoría': 'Consultoría',
        'consultoria': 'Consultoría',
        'it': 'IT',
        'finanzas': 'Finanzas'
    })
)

print("Departamentos normalizados:")
print(empleados_limpio[['departamento', 'departamento_normalizado']])
```

## Transformación de Tipos de Datos

### Conversión de Salarios

```python
# Limpiar formato de salarios y convertir a numérico
def limpiar_salario(salario_str):
    """Convierte string de salario a float, removiendo comas y espacios."""
    if isinstance(salario_str, str):
        # Remover comas y espacios
        salario_limpio = salario_str.replace(',', '').replace(' ', '')
        return float(salario_limpio)
    return float(salario_str)

empleados_limpio['salario_numerico'] = empleados_limpio['salario'].apply(limpiar_salario)

print("Salarios convertidos:")
print(empleados_limpio[['empleado_id', 'salario', 'salario_numerico']])
```

### Estandarización de Fechas

```python
# Función para normalizar diferentes formatos de fecha
def estandarizar_fecha(fecha_str):
    """Convierte diferentes formatos de fecha a datetime."""
    fecha_str = str(fecha_str).strip()
    
    # Intentar diferentes formatos
    formatos = ['%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y', '%Y/%m/%d']
    
    for formato in formatos:
        try:
            return pd.to_datetime(fecha_str, format=formato)
        except ValueError:
            continue
    
    # Si ningún formato funciona, usar parser automático
    try:
        return pd.to_datetime(fecha_str)
    except:
        return pd.NaT

empleados_limpio['fecha_ingreso_std'] = empleados_limpio['fecha_ingreso'].apply(estandarizar_fecha)

print("Fechas estandarizadas:")
print(empleados_limpio[['empleado_id', 'fecha_ingreso', 'fecha_ingreso_std']])
```

### Normalización de Teléfonos

```python
# Función para estandarizar números de teléfono
def estandarizar_telefono(telefono):
    """Estandariza formato de teléfono a XX-XXX-XXXX."""
    # Remover todo excepto dígitos
    digitos = re.sub(r'\D', '', str(telefono))
    
    # Formatear si tiene 9 dígitos (agregando código de área)
    if len(digitos) == 9:
        return f"91-{digitos[2:5]}-{digitos[5:]}"
    elif len(digitos) == 11 and digitos.startswith('91'):
        return f"91-{digitos[2:5]}-{digitos[5:]}"
    else:
        return telefono  # Devolver original si no se puede formatear

empleados_limpio['telefono_std'] = empleados_limpio['telefono'].apply(estandarizar_telefono)

print("Teléfonos estandarizados:")
print(empleados_limpio[['empleado_id', 'telefono', 'telefono_std']])
```

## Modificaciones Condicionales

### Usando loc para Modificaciones Específicas

```python
# Estandarizar estados usando loc
empleados_limpio['estado_std'] = empleados_limpio['estado'].str.lower()

# Mapear a valores estándar
empleados_limpio.loc[empleados_limpio['estado_std'] == 'activo', 'estado_std'] = 'Activo'
empleados_limpio.loc[empleados_limpio['estado_std'] == 'inactivo', 'estado_std'] = 'Inactivo'

print("Estados estandarizados:")
print(empleados_limpio[['empleado_id', 'estado', 'estado_std']])
```

### Modificaciones Basadas en Multiple Condiciones

```python
# Crear columna de categoría salarial basada en departamento
def categorizar_salario_por_dept(row):
    if row['departamento_normalizado'] == 'Consultoría':
        if row['salario_numerico'] >= 65000:
            return 'Senior'
        else:
            return 'Junior'
    elif row['departamento_normalizado'] == 'IT':
        if row['salario_numerico'] >= 68000:
            return 'Senior'
        else:
            return 'Junior'
    else:  # Finanzas
        if row['salario_numerico'] >= 70000:
            return 'Senior'
        else:
            return 'Junior'

empleados_limpio['categoria_salarial'] = empleados_limpio.apply(categorizar_salario_por_dept, axis=1)

print("Categorización salarial por departamento:")
print(empleados_limpio[['empleado_id', 'departamento_normalizado', 'salario_numerico', 'categoria_salarial']])
```

## Corrección de Datos Basada en Reglas

### Validación y Corrección de Emails

```python
# Función para validar formato de email
def es_email_valido(email):
    """Verifica si un email tiene formato válido."""
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(patron, email))

# Identificar emails inválidos
empleados_limpio['email_valido'] = empleados_limpio['email'].apply(es_email_valido)

# Corregir emails problemáticos (ejemplo: falta de dominio completo)
def corregir_email(email):
    """Intenta corregir problemas comunes en emails."""
    if es_email_valido(email):
        return email
    
    # Corrección común: agregar .com si falta
    if '@company' in email and not '.com' in email:
        return email + '.com'
    
    return email

empleados_limpio['email_corregido'] = empleados_limpio['email'].apply(corregir_email)

print("Validación y corrección de emails:")
print(empleados_limpio[['empleado_id', 'email', 'email_valido', 'email_corregido']])
```

### Detección y Corrección de Outliers

```python
# Detectar salarios que parecen outliers
q1 = empleados_limpio['salario_numerico'].quantile(0.25)
q3 = empleados_limpio['salario_numerico'].quantile(0.75)
iqr = q3 - q1
limite_inferior = q1 - 1.5 * iqr
limite_superior = q3 + 1.5 * iqr

# Marcar outliers
empleados_limpio['salario_outlier'] = (
    (empleados_limpio['salario_numerico'] < limite_inferior) |
    (empleados_limpio['salario_numerico'] > limite_superior)
)

print(f"Límites de salario: {limite_inferior:.0f} - {limite_superior:.0f}")
print("Detección de outliers salariales:")
print(empleados_limpio[['empleado_id', 'salario_numerico', 'salario_outlier']])
```

## Modificaciones en Lote

### Usando replace() para Múltiples Reemplazos

```python
# Crear dataset con abreviaciones inconsistentes
datos_proyectos = pd.DataFrame({
    'proyecto_id': ['P001', 'P002', 'P003', 'P004'],
    'estado': ['IP', 'En Progreso', 'COMPLETADO', 'comp'],
    'prioridad': ['H', 'Alta', 'MEDIA', 'm'],
    'tipo': ['Cons', 'Consultoría', 'TRAINING', 'train']
})

# Diccionarios de mapeo para estandarización
mapeo_estado = {
    'IP': 'En Progreso',
    'En Progreso': 'En Progreso',
    'COMPLETADO': 'Completado',
    'comp': 'Completado'
}

mapeo_prioridad = {
    'H': 'Alta',
    'Alta': 'Alta',
    'MEDIA': 'Media',
    'm': 'Media'
}

mapeo_tipo = {
    'Cons': 'Consultoría',
    'Consultoría': 'Consultoría',
    'TRAINING': 'Training',
    'train': 'Training'
}

# Aplicar mapeos
datos_proyectos['estado_std'] = datos_proyectos['estado'].replace(mapeo_estado)
datos_proyectos['prioridad_std'] = datos_proyectos['prioridad'].replace(mapeo_prioridad)
datos_proyectos['tipo_std'] = datos_proyectos['tipo'].replace(mapeo_tipo)

print("Estandarización de datos de proyectos:")
print(datos_proyectos)
```

### Usando map() para Transformaciones Complejas

```python
# Crear códigos únicos para empleados basados en múltiples campos
def generar_codigo_empleado(row):
    """Genera código único: DEPT_YYYY_NNN"""
    dept_codigo = {
        'Consultoría': 'CONS',
        'IT': 'TECH',
        'Finanzas': 'FIN'
    }
    
    año_ingreso = row['fecha_ingreso_std'].year if pd.notna(row['fecha_ingreso_std']) else 2020
    dept = dept_codigo.get(row['departamento_normalizado'], 'UNK')
    numero = row.name + 1  # Usar índice + 1 como número
    
    return f"{dept}_{año_ingreso}_{numero:03d}"

empleados_limpio['codigo_empleado'] = empleados_limpio.apply(generar_codigo_empleado, axis=1)

print("Códigos de empleado generados:")
print(empleados_limpio[['empleado_id', 'departamento_normalizado', 'fecha_ingreso_std', 'codigo_empleado']])
```

## Casos Prácticos de Consultoría

### Caso 1: Estandarización de Datos de Cliente

```python
# Simular datos de clientes con inconsistencias
clientes_raw = pd.DataFrame({
    'cliente_id': ['C001', 'C002', 'C003', 'C004'],
    'nombre_empresa': ['Empresa A S.A.', 'EMPRESA B SA', 'empresa c s.a.', 'Empresa D S.A'],
    'industria': ['Tecnología', 'TECH', 'Finanzas', 'fin'],
    'tamaño': ['Grande', 'G', 'Mediana', 'P'],
    'ingresos': ['1.5M', '2,000,000', '500K', '100,000']
})

def estandarizar_datos_cliente(df):
    """Estandariza datos de cliente para consistencia."""
    df = df.copy()
    
    # Estandarizar nombres de empresa
    df['nombre_empresa'] = (df['nombre_empresa']
                           .str.title()
                           .str.replace(' S.A.', ' S.A.')
                           .str.replace(' Sa', ' S.A.')
                           .str.replace(' SA', ' S.A.'))
    
    # Mapear industrias
    mapeo_industria = {
        'Tecnología': 'Tecnología',
        'TECH': 'Tecnología',
        'Finanzas': 'Finanzas',
        'fin': 'Finanzas'
    }
    df['industria'] = df['industria'].replace(mapeo_industria)
    
    # Mapear tamaños
    mapeo_tamaño = {
        'Grande': 'Grande',
        'G': 'Grande',
        'Mediana': 'Mediana',
        'M': 'Mediana',
        'Pequeña': 'Pequeña',
        'P': 'Pequeña'
    }
    df['tamaño'] = df['tamaño'].replace(mapeo_tamaño)
    
    # Convertir ingresos a formato numérico
    def convertir_ingresos(ingreso_str):
        ingreso_str = str(ingreso_str).upper().replace(',', '')
        if 'M' in ingreso_str:
            return float(ingreso_str.replace('M', '')) * 1000000
        elif 'K' in ingreso_str:
            return float(ingreso_str.replace('K', '')) * 1000
        else:
            return float(ingreso_str)
    
    df['ingresos_numericos'] = df['ingresos'].apply(convertir_ingresos)
    
    return df

clientes_limpio = estandarizar_datos_cliente(clientes_raw)

print("Datos de clientes estandarizados:")
print(clientes_limpio)
```

### Caso 2: Actualización Masiva Basada en Nuevas Reglas

```python
# Simular cambio en política salarial
def aplicar_nueva_politica_salarial(df):
    """Aplica nueva política salarial basada en desempeño y mercado."""
    df = df.copy()
    
    # Aumentos base por departamento (simulado)
    aumentos_base = {
        'Consultoría': 1.05,  # 5%
        'IT': 1.08,          # 8%
        'Finanzas': 1.03     # 3%
    }
    
    # Aplicar aumento base
    df['salario_nuevo'] = df.apply(
        lambda row: row['salario_numerico'] * aumentos_base.get(row['departamento_normalizado'], 1.0),
        axis=1
    )
    
    # Bonus adicional para empleados senior
    df.loc[df['categoria_salarial'] == 'Senior', 'salario_nuevo'] *= 1.02
    
    # Redondear a múltiplos de 1000
    df['salario_nuevo'] = (df['salario_nuevo'] / 1000).round() * 1000
    
    # Calcular aumento porcentual
    df['aumento_pct'] = ((df['salario_nuevo'] - df['salario_numerico']) / df['salario_numerico']) * 100
    
    return df

empleados_actualizados = aplicar_nueva_politica_salarial(empleados_limpio)

print("Aplicación de nueva política salarial:")
print(empleados_actualizados[['empleado_id', 'departamento_normalizado', 'categoria_salarial', 
                               'salario_numerico', 'salario_nuevo', 'aumento_pct']])
```

## Ejercicios Prácticos

### Ejercicio 1: Limpieza de Datos de Contacto
```python
# TODO: Dado el siguiente dataset sucio, limpia y estandariza:
contactos_sucios = pd.DataFrame({
    'nombre': ['  juan perez  ', 'ANA GARCIA', 'carlos LOPEZ'],
    'telefono': ['91 555 1234', '915551235', '91-555-1236'],
    'email': ['juan@COMPANY.COM', 'ana.garcia@company', 'carlos.lopez@company.com']
})

# 1. Estandarizar nombres (Title Case, sin espacios extra)
# 2. Formatear teléfonos como XX-XXX-XXXX
# 3. Normalizar emails (minúsculas, agregar .com si falta)

# Tu solución aquí:
```

### Ejercicio 2: Corrección de Datos Inconsistentes
```python
# TODO: Corregir inconsistencias en este dataset:
ventas_inconsistentes = pd.DataFrame({
    'region': ['Norte', 'N', 'NORTE', 'Sur', 's', 'SUR'],
    'estado': ['completado', 'PENDIENTE', 'Comp', 'pend', 'COMPLETADO', 'Pendiente'],
    'monto': ['1,500', '2500', '1.200', '3,000', '800', '2.800']
})

# 1. Estandarizar regiones (Norte, Sur)
# 2. Estandarizar estados (Completado, Pendiente)
# 3. Convertir montos a números

# Tu solución aquí:
```

## Mejores Prácticas

!!! tip "Consejos para Modificación Eficiente"
    1. **Haz una copia**: Siempre trabaja con copias para preservar datos originales
    2. **Funciones reutilizables**: Crea funciones para transformaciones complejas
    3. **Validación**: Verifica resultados después de cada modificación
    4. **Logging**: Documenta qué cambios se realizaron y por qué
    5. **Backup**: Mantén versiones de respaldo antes de modificaciones masivas

### Plantilla para Modificaciones Seguras

```python
def modificar_datos_seguro(df, funciones_modificacion, validaciones=None):
    """
    Aplica modificaciones de manera segura con validación.
    
    Args:
        df: DataFrame original
        funciones_modificacion: Lista de funciones a aplicar
        validaciones: Lista de funciones de validación
    
    Returns:
        DataFrame modificado
    """
    # Crear copia
    df_modificado = df.copy()
    
    # Aplicar modificaciones
    for funcion in funciones_modificacion:
        try:
            df_modificado = funcion(df_modificado)
            print(f"✓ Aplicada: {funcion.__name__}")
        except Exception as e:
            print(f"✗ Error en {funcion.__name__}: {e}")
            return df  # Retornar original en caso de error
    
    # Ejecutar validaciones si se proporcionan
    if validaciones:
        for validacion in validaciones:
            if not validacion(df_modificado):
                print(f"✗ Validación fallida: {validacion.__name__}")
                return df
    
    print("✓ Todas las modificaciones aplicadas exitosamente")
    return df_modificado

# Ejemplo de uso:
# resultado = modificar_datos_seguro(
#     empleados_sucio,
#     [limpiar_nombres, estandarizar_emails, convertir_salarios],
#     [validar_emails, validar_salarios_positivos]
# )
```

## Resumen

La modificación eficiente de datos te permite:

- ✅ Corregir inconsistencias y errores en los datos
- ✅ Estandarizar formatos para análisis consistente
- ✅ Aplicar nuevas reglas de negocio masivamente
- ✅ Mejorar la calidad general del dataset
- ✅ Preparar datos para análisis y reportes

**Próximo paso**: Continúa con [Función apply()](funcion-apply.md) para dominar transformaciones más complejas y personalizadas.