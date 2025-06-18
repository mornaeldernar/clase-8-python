import pandas as pd
import re
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
contactos_limpios = contactos_sucios.copy()
def limpiar_nombre(nombre):
    return nombre.strip().title()
contactos_limpios['nombre'] = contactos_limpios['nombre'].apply(limpiar_nombre)

def formatear_telefono(telefono):
    digitos = re.sub(r'\D', '', telefono)  # Eliminar no dígitos
    if len(digitos) == 9:
        return f"{digitos[:2]}-{digitos[2:5]}-{digitos[5:]}"
    return telefono  # Si no es válido, devolver original
    
contactos_limpios['telefono'] = contactos_limpios['telefono'].apply(formatear_telefono)

def normalizar_email(email):
    email = email.strip().lower()
    if not email.endswith('.com'):
        email += '.com'
    return email
contactos_limpios['email'] = contactos_limpios['email'].apply(normalizar_email)
print("Dataset limpio:")
print(contactos_limpios)