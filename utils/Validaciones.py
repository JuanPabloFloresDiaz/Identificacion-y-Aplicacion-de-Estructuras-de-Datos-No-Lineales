"""Módulo para realizar las validaciones necesarias en la entrada de datos.
   Contiene métodos para validar enteros, decimales, texto, DUI, correo electrónico, teléfono y fechas.
   Utiliza métodos estáticos para realizar las validaciones sin necesidad de instanciar la clase.
"""
# Validaciones.py
### Clase Validaciones que contiene métodos estáticos para validar diferentes tipos de datos
class Validaciones:
    # Método para validar la longitud de una cadena
    @staticmethod
    def validate_length(input_str, min_length=None, max_length=None):
        """Valida la longitud de una cadena"""
        if min_length is not None and len(input_str) < min_length:
            return False
        if max_length is not None and len(input_str) > max_length:
            return False
        return True
    # Método para validar un rango numérico
    @staticmethod
    def validate_range(value, min_value=None, max_value=None):
        """Valida que un valor numérico esté dentro de un rango"""
        if min_value is not None and value < min_value:
            return False
        if max_value is not None and value > max_value:
            return False
        return True
    # Métodos para validar diferentes tipos de datos
    ### Método para validar un número entero
    @staticmethod
    def validate_integer(input_str):
        """Valida que la entrada sea un número entero válido"""
        return input_str.lstrip('-').isdigit()
    ### Método para validar un número decimal
    @staticmethod
    def validate_double(input_str):
        """Valida que la entrada sea un número decimal válido"""
        try:
            float(input_str)
            return True
        except ValueError:
            return False
    ### Método para validar el formato de un DUI salvadoreño
    @staticmethod
    def validate_dui(dui):
        """Valida formato de DUI salvadoreño (00000000-0)"""
        if len(dui) != 10:
            return False
        if dui[8] != '-':
            return False
        return dui[:8].isdigit() and dui[9].isdigit()
    ### Método para validar el formato de un correo electrónico
    @staticmethod
    def validate_email(email):
        """Valida formato básico de correo electrónico"""
        if '@' not in email:
            return False
        parts = email.split('@')
        if len(parts) != 2:
            return False
        local, domain = parts
        if not local or not domain:
            return False
        if '.' not in domain:
            return False
        domain_parts = domain.split('.')
        if len(domain_parts) < 2:
            return False
        for part in domain_parts:
            if not part:
                return False
        return True
    ### Método para validar el formato de un teléfono salvadoreño
    @staticmethod
    def validate_phone(phone, strict_prefix=True):
        """
        Valida formato de teléfono salvadoreño (0000-0000)
        Si strict_prefix=True, valida que inicie con 6,7 (celular) o 2 (fijo)
        """
        if len(phone) != 9:
            return False
        if phone[4] != '-':
            return False
        if not (phone[:4].isdigit() and phone[5:].isdigit()):
            return False
        
        if strict_prefix:
            first_digit = phone[0]
            if first_digit not in ['2', '6', '7']:
                return False
        
        return True
    ### Método para validar el formato de un ISBN de 13 dígitos
    @staticmethod
    def validate_isbn(isbn):
        """
        Valida formato de ISBN-13 (13 dígitos numéricos)
        Puede incluir o no guiones separadores
        Ejemplos válidos: 9781234567897, 978-1-234-56789-7
        """
        # Remover guiones y espacios para validación
        isbn_clean = isbn.replace('-', '').replace(' ', '')
        
        # Verificar que tenga exactamente 13 dígitos
        if len(isbn_clean) != 13:
            return False
        
        # Verificar que todos sean dígitos
        if not isbn_clean.isdigit():
            return False
        
        # Verificar que comience con 978 o 979 (prefijos válidos para ISBN-13)
        if not (isbn_clean.startswith('978') or isbn_clean.startswith('979')):
            return False
        
        # Validar dígito de control usando el algoritmo ISBN-13
        return Validaciones._validate_isbn13_checksum(isbn_clean)
    
    ### Método privado para validar el dígito de control del ISBN-13
    @staticmethod
    def _validate_isbn13_checksum(isbn):
        """Valida el dígito de control del ISBN-13 usando el algoritmo estándar"""
        try:
            # Calcular suma ponderada de los primeros 12 dígitos
            total = 0
            for i in range(12):
                digit = int(isbn[i])
                # Los dígitos en posiciones impares se multiplican por 1, los pares por 3
                multiplier = 1 if i % 2 == 0 else 3
                total += digit * multiplier
            
            # Calcular dígito de control
            check_digit = (10 - (total % 10)) % 10
            
            # Comparar con el último dígito del ISBN
            return check_digit == int(isbn[12])
        
        except (ValueError, IndexError):
            return False

    ### Método para validar el formato de una fecha
    @staticmethod
    def validate_date(date_str, date_format="dd/mm/yyyy"):
        """
        Valida formato de fecha sin usar librerías externas
        Soporta formatos: dd/mm/yyyy, mm/dd/yyyy, yyyy/mm/dd
        """
        try:
            if date_format == "dd/mm/yyyy":
                if len(date_str) != 10 or date_str[2] != '/' or date_str[5] != '/':
                    return False
                day, month, year = date_str.split('/')
                day, month, year = int(day), int(month), int(year)
                
            elif date_format == "mm/dd/yyyy":
                if len(date_str) != 10 or date_str[2] != '/' or date_str[5] != '/':
                    return False
                month, day, year = date_str.split('/')
                day, month, year = int(day), int(month), int(year)
                
            elif date_format == "yyyy/mm/dd":
                if len(date_str) != 10 or date_str[4] != '/' or date_str[7] != '/':
                    return False
                year, month, day = date_str.split('/')
                day, month, year = int(day), int(month), int(year)
            else:
                return False

            # Validar rangos básicos
            if not (1 <= month <= 12):
                return False
            if not (1 <= day <= 31):
                return False
            if year < 1900 or year > 2100:
                return False

            # Validar días por mes
            days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            
            # Verificar año bisiesto
            if Validaciones._is_leap_year(year):
                days_in_month[1] = 29
            
            if day > days_in_month[month - 1]:
                return False

            return True
        except (ValueError, IndexError):
            return False
    ### Método para determinar si un año es bisiesto
    @staticmethod
    def _is_leap_year(year):
        """Determina si un año es bisiesto"""
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
    ### Método para obtener mensajes de error específicos
    @staticmethod
    def get_validation_message(validation_type, **kwargs):
        """Retorna mensajes de error específicos para cada tipo de validación"""
        messages = {
            'length': f"El texto debe tener entre {kwargs.get('min_length', 'N/A')} y {kwargs.get('max_length', 'N/A')} caracteres.",
            'range': f"El valor debe estar entre {kwargs.get('min_value', 'N/A')} y {kwargs.get('max_value', 'N/A')}.",
            'integer': "Eso no es un número entero válido. Intenta de nuevo.",
            'double': "Eso no es un número decimal válido. Intenta de nuevo.",
            'dui': "El DUI debe tener el formato 00000000-0 (8 números, un guión y un número).",
            'email': "El correo electrónico debe tener un formato válido (ejemplo@dominio.com).",
            'phone': "El teléfono debe tener el formato 0000-0000.",
            'phone_strict': "El teléfono debe iniciar con 6 o 7 (celular) o 2 (fijo) y tener el formato 0000-0000.",
            'isbn': "El ISBN debe tener 13 dígitos, comenzar con 978 o 979, y tener un dígito de control válido. Ejemplo: 9781234567897",
            'date': f"La fecha debe tener el formato {kwargs.get('format', 'dd/mm/yyyy')} y ser válida.",
            'empty': "El campo no puede estar vacío."
        }
        return messages.get(validation_type, "Entrada inválida. Intenta de nuevo.")
