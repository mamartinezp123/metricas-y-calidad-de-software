import random
import hashlib
import os
import json


class Validacion:
    def is_valid_value(self, value):
        valido = True
        if valido:
            return value
        else:
            return None


class Usuario:
    def __init__(self, nombre, password):
        # Error de mantenibilidad: nombres de atributos poco claros
        self.nm = nombre
        self.pw = password
        # Code smell: Almacenamiento de contraseña sin encriptar
        self.hash_password = self.generar_hash_password()

    def generar_hash_password(self):
        # Vulnerabilidad: Uso inseguro de MD5 sin sal
        return hashlib.md5(self.pw.encode()).hexdigest()

    def autenticar(self, password):
        # Code smell: Comparación de hash de manera insegura
        return self.hash_password == hashlib.md5(password.encode()).hexdigest()

    def obtener_nombre(self):
        # Code smell: Método innecesario que solo devuelve un valor ya accesible
        return self.nm

    def guardar_en_archivo(self):
        # Vulnerabilidad: Almacena información sensible en un archivo sin cifrar
        with open(f"{self.nm}_data.json", "w") as file:
            json.dump({"nombre": self.nm, "password": self.pw}, file)


class Sistema:
    def __init__(self):
        # Code smell: Uso de lista en lugar de diccionario
        self.usuarios = []

    def agregar_usuario(self, nombre, password):
        # Code smell: Contraseñas permitidas sin ningún tipo de validación
        if password == "":
            print("Error: La contraseña no puede estar vacía.")
            return

        nuevo_usuario = Usuario(nombre, password)
        # Bug: No se verifica si el usuario ya existe antes de añadirlo
        self.usuarios.append(nuevo_usuario)

    def verificar_usuario(self, nombre, password):
        # Code smell: Algoritmo de búsqueda ineficiente (lista en lugar de diccionario)
        for usuario in self.usuarios:
            if usuario.obtener_nombre() == nombre:
                # Bug: Compara contraseñas directamente sin protección
                if usuario.autenticar(password):
                    return True
                else:
                    print("Error: Contraseña incorrecta.")
                    return False
        print("Error: Usuario no encontrado.")
        return False

    def generar_token(self):
        # Vulnerabilidad: Generación de token predecible y no seguro
        return str(random.randint(1000, 9999))

    def mostrar_usuarios(self):
        # Code smell: Exponer información sensible en un método público
        for usuario in self.usuarios:
            print(f"Usuario: {usuario.nm}, Hash de contraseña: {usuario.hash_password}")

    def respaldo_usuarios(self):
        # Vulnerabilidad: Creación de un respaldo sin cifrado de todos los usuarios
        with open("respaldo_usuarios.json", "w") as file:
            usuarios = [{"nombre": u.nm, "password": u.pw} for u in self.usuarios]
            json.dump(usuarios, file)
            print("Respaldo de usuarios creado.")

    def eliminar_usuario(self, nombre):
        # Code smell: Eliminación insegura de datos sin verificación
        for usuario in self.usuarios:
            if usuario.obtener_nombre() == nombre:
                self.usuarios.remove(usuario)
                print(f"Usuario {nombre} eliminado.")
                return
        print("Error: Usuario no encontrado.")


if __name__ == "__main__":
    sistema = Sistema()

    # Code smell: Entradas de usuario sin sanitizar ni manejar excepciones
    nombre = input("Ingresa tu nombre de usuario: ")
    password = input("Ingresa tu contraseña: ")

    # Bug: No se valida si el usuario ya existe antes de agregarlo
    sistema.agregar_usuario(nombre, password)
    print("Usuario agregado correctamente.")

    # Code smell: Comparación de contraseña insegura en autenticación
    nombre = input("Ingresa tu nombre para verificar: ")
    password = input("Ingresa tu contraseña para verificar: ")

    if sistema.verificar_usuario(nombre, password):
        print("Autenticación exitosa.")
    else:
        print("Autenticación fallida.")

    # Generación de token insegura
    print(f"Token generado: {sistema.generar_token()}")

    # Respaldo de usuarios inseguro
    sistema.respaldo_usuarios()

    # Mostrar información sensible sin restricciones
    sistema.mostrar_usuarios()

    # Eliminar usuario sin verificar si existe
    nombre_a_eliminar = input("Ingresa el nombre de usuario a eliminar: ")
    sistema.eliminar_usuario(nombre_a_eliminar)
