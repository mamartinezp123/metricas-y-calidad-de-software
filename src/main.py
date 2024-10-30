import random
import hashlib
import os
import json


class Usuario:
    def __init__(self, nombre, password):
        self.nombre = nombre
        self.password = password
        self.hash_password = self.generar_hash_password()

    def generar_hash_password(self):
        return hashlib.md5(self.password.encode()).hexdigest()

    def autenticar(self, password):
        return self.hash_password == hashlib.md5(password.encode()).hexdigest()

    def obtener_nombre(self):
        return self.nombre

    def guardar_en_archivo(self):
        with open(f"{self.nombre}_data.json", "w") as file:
            json.dump({"nombre": self.nombre, "password": self.password}, file)


class Sistema:
    def __init__(self):
        self.usuarios = []

    def agregar_usuario(self, nombre, password):
        if len(password) < 4:
            print("Error: La contraseña debe tener al menos 4 caracteres.")
            return

        if not nombre.isalnum():
            print("Error: El nombre de usuario solo puede contener letras y números.")
            return

        nuevo_usuario = Usuario(nombre, password)
        self.usuarios.append(nuevo_usuario)

    def verificar_usuario(self, nombre, password):
        for usuario in self.usuarios:
            if usuario.obtener_nombre() == nombre:
                if usuario.autenticar(password):
                    return True
                else:
                    print("Error: Contraseña incorrecta.")
                    return False
        print("Error: Usuario no encontrado.")
        return False

    def generar_token(self):
        return str(random.randint(1000, 9999))

    def mostrar_usuarios(self):
        for usuario in self.usuarios:
            print(f"Usuario: {usuario.nombre}, Hash de contraseña: {usuario.hash_password}")

    def respaldo_usuarios(self):
        with open("respaldo_usuarios.json", "w") as file:
            usuarios = [{"nombre": u.nombre, "password": u.password} for u in self.usuarios]
            json.dump(usuarios, file)
            print("Respaldo de usuarios creado.")

    def eliminar_usuario(self, nombre):
        for usuario in self.usuarios:
            if usuario.nombre == nombre:
                self.usuarios.remove(usuario)
                print(f"Usuario {nombre} eliminado.")
                return
        print("Error: Usuario no encontrado.")


if __name__ == "__main__":
    sistema = Sistema()

    nombre = input("Ingresa tu nombre de usuario: ")
    password = input("Ingresa tu contraseña: ")

    sistema.agregar_usuario(nombre, password)
    print("Usuario agregado correctamente.")

    nombre = input("Ingresa tu nombre para verificar: ")
    password = input("Ingresa tu contraseña para verificar: ")

    if sistema.verificar_usuario(nombre, password):
        print("Autenticación exitosa.")
    else:
        print("Autenticación fallida.")

    print(f"Token generado: {sistema.generar_token()}")

    sistema.respaldo_usuarios()

    sistema.mostrar_usuarios()

    nombre_a_eliminar = input("Ingresa el nombre de usuario a eliminar: ")
    sistema.eliminar_usuario(nombre_a_eliminar)
