# Teclado.py
"""Módulo para leer datos del teclado con validaciones específicas, reciclado de 
   un proyecto de practicas de programación en Python que hice anteriormente.
   Contiene métodos para leer enteros, decimales, texto, DUI, correo electrónico, teléfono y fechas.
   Utiliza la clase Validaciones para realizar las validaciones necesarias.
"""
# Importamos la clase Validaciones que contiene las funciones de validación
from utils.Validaciones import Validaciones

# Creamos la clase Teclado que contendrá los métodos para leer diferentes tipos de datos
class Teclado:
    # Métodos estáticos para leer diferentes tipos de datos del teclado
    ### Método para leer un número entero con validaciones
    @staticmethod
    def read_integer(mensaje, min_digits=None, max_digits=None, min_value=None, max_value=None):
        """Lee un número entero del teclado con validaciones"""
        while True:
            entrada = input(f"{mensaje} ").strip()
            
            if not entrada:
                print(Validaciones.get_validation_message('empty'))
                continue
            
            if not Validaciones.validate_integer(entrada):
                print(Validaciones.get_validation_message('integer'))
                continue
            
            numero = int(entrada)
            num_str = str(abs(numero))
            
            if min_digits is not None or max_digits is not None:
                if not Validaciones.validate_length(num_str, min_digits, max_digits):
                    print(f"El número debe tener entre {min_digits or 'cualquier'} y {max_digits or 'cualquier'} dígitos.")
                    continue
            
            if min_value is not None or max_value is not None:
                if not Validaciones.validate_range(numero, min_value, max_value):
                    print(Validaciones.get_validation_message('range', min_value=min_value, max_value=max_value))
                    continue
            
            return numero

    ### Método para leer un número decimal con validaciones
    @staticmethod
    def read_double(mensaje, min_value=None, max_value=None):
        """Lee un número decimal del teclado con validaciones"""
        while True:
            entrada = input(f"{mensaje} ").strip()
            
            if not entrada:
                print(Validaciones.get_validation_message('empty'))
                continue
            
            if not Validaciones.validate_double(entrada):
                print(Validaciones.get_validation_message('double'))
                continue
            
            valor = float(entrada)
            
            if min_value is not None or max_value is not None:
                if not Validaciones.validate_range(valor, min_value, max_value):
                    print(Validaciones.get_validation_message('range', min_value=min_value, max_value=max_value))
                    continue
            
            return valor

    ### Método para leer texto con validaciones
    @staticmethod
    def read_text(mensaje, min_length=None, max_length=None):
        """Lee texto del teclado con validaciones de longitud"""
        while True:
            texto = input(f"{mensaje} ").strip()
            
            if not texto:
                print(Validaciones.get_validation_message('empty'))
                continue
            
            if not Validaciones.validate_length(texto, min_length, max_length):
                print(Validaciones.get_validation_message('length', min_length=min_length, max_length=max_length))
                continue
            
            return texto

    ### Métodos para leer datos específicos con validaciones
    ### Método para leer un DUI (Documento Único de Identidad) salvadoreño
    @staticmethod
    def read_dui(mensaje):
        """Lee un DUI con validación de formato salvadoreño"""
        while True:
            dui = input(f"{mensaje} ").strip()
            
            if not dui:
                print(Validaciones.get_validation_message('empty'))
                continue
            
            if not Validaciones.validate_dui(dui):
                print(Validaciones.get_validation_message('dui'))
                continue
            
            return dui

    ### Método para leer un correo electrónico con validación de formato
    @staticmethod
    def read_email(mensaje):
        """Lee un correo electrónico con validación de formato"""
        while True:
            email = input(f"{mensaje} ").strip()
            
            if not email:
                print(Validaciones.get_validation_message('empty'))
                continue
            
            if not Validaciones.validate_email(email):
                print(Validaciones.get_validation_message('email'))
                continue
            
            return email

    ### Método para leer un teléfono con validación de formato salvadoreño y la opción de validar prefijo estricto o no.
    @staticmethod
    def read_phone(mensaje, strict_prefix=True):
        """
        Lee un teléfono con validación de formato salvadoreño
        strict_prefix: Si True, valida que inicie con 6,7 (celular) o 2 (fijo)
        """
        while True:
            phone = input(f"{mensaje} ").strip()
            
            if not phone:
                print(Validaciones.get_validation_message('empty'))
                continue
            
            if not Validaciones.validate_phone(phone, strict_prefix):
                if strict_prefix:
                    print(Validaciones.get_validation_message('phone_strict'))
                else:
                    print(Validaciones.get_validation_message('phone'))
                continue
            
            return phone

    ### Método para leer un ISBN con validación de formato
    @staticmethod
    def read_isbn(mensaje):
        """Lee un ISBN-13 con validación de formato y dígito de control"""
        while True:
            isbn = input(f"{mensaje} ").strip()
            
            if not isbn:
                print(Validaciones.get_validation_message('empty'))
                continue
            
            if not Validaciones.validate_isbn(isbn):
                print(Validaciones.get_validation_message('isbn'))
                continue
            
            # Devolver ISBN limpio (sin guiones)
            return isbn.replace('-', '').replace(' ', '')

    ### Método para leer una fecha con validación de formato
    @staticmethod
    def read_date(mensaje, date_format="dd/mm/yyyy"):
        """
        Lee una fecha con validación de formato
        date_format: "dd/mm/yyyy", "mm/dd/yyyy", o "yyyy/mm/dd"
        """
        while True:
            date_str = input(f"{mensaje} (formato {date_format}) ").strip()
            
            if not date_str:
                print(Validaciones.get_validation_message('empty'))
                continue
            
            if not Validaciones.validate_date(date_str, date_format):
                print(Validaciones.get_validation_message('date', format=date_format))
                continue
            
            return date_str